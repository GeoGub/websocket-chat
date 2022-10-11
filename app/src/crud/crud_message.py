from sqlalchemy import join, or_

from .crud_base import CRUDBase
from src.message.model import message
from src.user.model import user


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
