from databases import Database
from pydantic import BaseModel
from fastapi import HTTPException
from sqlalchemy import select, func, insert, delete

from http import HTTPStatus

from src.sample_schemas import Params

class CRUDBase:
    def __init__(self, model) -> None:
        self.model = model

    async def read(self, db: Database, params: Params):
        query = select(self.model).limit(params.limit).offset(params.limit*params.offset)
        users = await db.fetch_all(query)
        total = await db.execute(select(func.count()).select_from(self.model))
        return users, total

    async def create(self, db: Database, value: BaseModel):
        transaction = await db.transaction()
        try:
            await db.execute(insert(self.model, value.dict()))
        except Exception as e:
            await transaction.rollback()
            raise HTTPException(status_code=HTTPStatus.BAD_REQUEST.value, 
                                detail=HTTPStatus.BAD_REQUEST.phrase)
        else:
            await transaction.commit()
        return HTTPStatus.CREATED.value

    async def read_by_id(self, db: Database, id: int):
        query = select(self.model).where(self.model.c.id==id)
        user_by_id = await db.fetch_one(query)
        if not user_by_id:
            raise HTTPException(status_code=HTTPStatus.NOT_FOUND.value, 
                                detail=HTTPStatus.NOT_FOUND.phrase)
        return user_by_id

    async def delete(self, db: Database, id: int):
        query = delete(self.model).where(self.model.c.id==id).returning(self.model.c.id)
        user_id = await db.execute(query)
        if not user_id:
            raise HTTPException(status_code=HTTPStatus.BAD_REQUEST.value, 
                                detail=HTTPStatus.BAD_REQUEST.phrase)