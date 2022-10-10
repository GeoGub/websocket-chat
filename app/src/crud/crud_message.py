from databases import Database
from sqlalchemy import select, func, insert
from fastapi import HTTPException

from http import HTTPStatus

from src.message.schema import MessageInput
from .crud_base import CRUDBase
from src.message.model import message
from src.user.model import user
from src.sample_schemas import Params


class CRUDMessage(CRUDBase):
    async def read(self, db: Database, params: Params):
        query = select(self.model.join(user)).limit(params.limit).offset(params.limit*params.offset)        
        if params.dir == "asc":
            query = query.order_by(self.model.c.id.asc())
        else:
            query = query.order_by(self.model.c.id.desc())
        messages = await db.fetch_all(query)
        total = await db.execute(select(func.count()).select_from(self.model))
        return messages, total

    async def create(self, db: Database, value: MessageInput):
        status_code, message_id = await super().create(db, value)
        data = await self.read_by_id(db, message_id, user)
        return status_code, data
        
            
        

crud_message = CRUDMessage(message)
