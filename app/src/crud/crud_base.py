from databases import Database
from pydantic import BaseModel
from fastapi import HTTPException
from sqlalchemy import select, func, insert, delete, Table, Column, tuple_, or_
from sqlalchemy.sql.selectable import Join
from sqlalchemy.sql.elements import BinaryExpression, Tuple, BooleanClauseList, UnaryExpression

from http import HTTPStatus

from src.sample_schemas import Params
from src.database import database as db

class CRUDBase:
    def __init__(self, model) -> None:
        self.model = model
        self.BAD_REQUEST = HTTPException(status_code=HTTPStatus.BAD_REQUEST.value, 
                                         detail=HTTPStatus.BAD_REQUEST.phrase)
        self.NOT_FOUND = HTTPException(status_code=HTTPStatus.NOT_FOUND.value, 
                                       detail=HTTPStatus.NOT_FOUND.phrase)

    async def read(self, 
                   params: dict,
                   order: UnaryExpression,
                   join_models: tuple[Table] = tuple(),
                   join_condition: Join | tuple = tuple(),
                   query_condition: BinaryExpression | BooleanClauseList = or_(),
                   ) -> tuple[list, int]:
        query = select(self.model, *join_models). \
                    select_from(join_condition). \
                    where(query_condition). \
                    limit(params["limit"]). \
                    offset(params["limit"]*params["offset"]). \
                    order_by(order if order is not None else self.model.c.id.desc())
        items = await db.fetch_all(query)
        total = await db.execute(select(func.count()).select_from(self.model))
        return items, total

    async def create(self, value: dict):
        query = insert(self.model, value).returning(self.model.c.id)
        transaction = await db.transaction()
        try:
            item_id = await db.execute(query)
        except Exception as e:
            await transaction.rollback()
            raise self.BAD_REQUEST
        else:
            await transaction.commit()
        return HTTPStatus.CREATED.value, item_id

    async def read_one_by_condition(self, 
                                    query_condition: Tuple[BinaryExpression] = Tuple(), 
                                    join_model: Table | None = None, 
                                    join_condition: Join | None = None):
        query = select(self.model) \
                if join_condition is None else \
                select(self.model, join_model).select_from(join_condition)
        query = query.where(*query_condition)
        item = await db.fetch_one(query)
        if not item:
            raise self.NOT_FOUND
        return item

    
    async def delete(self, id: int):
        query = delete(self.model).where(self.model.c.id==id).returning(self.model.c.id)
        item = await db.execute(query)
        if not item:
            raise self.NOT_FOUND