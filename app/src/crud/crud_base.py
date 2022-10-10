from databases import Database
from pydantic import BaseModel
from fastapi import HTTPException
from sqlalchemy import select, func, insert, delete, Table

from http import HTTPStatus

from src.sample_schemas import Params

class CRUDBase:
    def __init__(self, model) -> None:
        self.model = model
        self.BAD_REQUEST = HTTPException(status_code=HTTPStatus.BAD_REQUEST.value, 
                                         detail=HTTPStatus.BAD_REQUEST.phrase)
        self.NOT_FOUND = HTTPException(status_code=HTTPStatus.NOT_FOUND.value, 
                                       detail=HTTPStatus.NOT_FOUND.phrase)

    async def read(self, db: Database, params: Params):
        query = select(self.model).limit(params.limit).offset(params.limit*params.offset)
        if params.dir == "asc":
            query = query.order_by(self.model.c.id.asc())
        else:
            query = query.order_by(self.model.c.id.desc())
        items = await db.fetch_all(query)
        total = await db.execute(select(func.count()).select_from(self.model))
        return items, total

    async def create(self, db: Database, value: BaseModel):
        query = insert(self.model, value.dict()).returning(self.model.c.id)
        transaction = await db.transaction()
        try:
            item_id = await db.execute(query)
        except Exception as e:
            await transaction.rollback()
            raise self.BAD_REQUEST
        else:
            await transaction.commit()
        return HTTPStatus.CREATED.value, item_id

    async def read_by_id(self, db: Database, id: int, join_model: Table | None = None):
        query = select(self.model) if join_model is None else select(self.model.join(join_model))
        query = query.where(self.model.c.id==id)
        item_by_id = await db.fetch_one(query)
        if not item_by_id:
            raise self.NOT_FOUND
        return item_by_id

    
    async def delete(self, db: Database, id: int):
        query = delete(self.model).where(self.model.c.id==id).returning(self.model.c.id)
        item = await db.execute(query)
        if not item:
            raise self.NOT_FOUND