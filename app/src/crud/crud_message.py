from sqlalchemy import join, or_

from src.user.schema import UserSchema
from .crud_base import CRUDBase
from src.message.model import message
from src.user.model import user


class CRUDMessage(CRUDBase):

    async def read(self, params: dict, chat_id: int):
        sender = user.alias("sender")
        join_models = (user, sender)
        join_condition = join(self.model, user, self.model.c.rel==user.c.id) \
                        .join(sender, self.model.c.sender_id==sender.c.id)
        query_condition = self.model.c.chat_id==chat_id
        order = self.model.c.id.asc() \
                if params["dir"] == "asc" else \
                self.model.c.id.desc()
        return await super().read(
            params=params,
            order=order,
            join_models=join_models,
            join_condition=join_condition,
            query_condition=query_condition
        )

    async def create(self, value: dict):
        status_code, message_id = await super().create(value)
        query_condition = [self.model.c.id==message_id]
        join_condition = join(self.model, user, self.model.c.sender_id==user.c.id)
        data = await self.read_one_by_condition(query_condition, tuple(user), join_condition)
        return status_code, data


crud_message = CRUDMessage(message)
