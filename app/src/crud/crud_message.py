from databases import Database
from sqlalchemy import join, or_
from fastapi import HTTPException

from http import HTTPStatus

from src.message.schema import MessageInput, MessageSchema
from src.user.schema import UserSchema
from .crud_base import CRUDBase
from src.message.model import message
from src.user.model import user
from src.sample_schemas import Params
from src.database import database as db


class CRUDMessage(CRUDBase):
    
    async def read(self, params: dict):
        join_condition = join(self.model, user, self.model.c.sender_id==user.c.id)
        messages, total = await super().read(params, user, join_condition)
        return messages, total

    async def create(self, value: dict):
        status_code, message_id = await super().create(value)
        join_condition = join(self.model, user, self.model.c.sender_id==user.c.id)
        data = await self.read_by_id(message_id, user, join_condition)
        return status_code, data


crud_message = CRUDMessage(message)
