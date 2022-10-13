from sqlalchemy import join, or_, tuple_, select , and_

from .crud_base import CRUDBase
from src.chat.model import chat, chat_columns
from src.user.model import user
from src.user.schema import UserSchema
from src.database import database

class CRUDChat(CRUDBase):
    
    async def read(self, params: dict, current_user: UserSchema):
        initial_user = user.alias("initial_user")
        join_models = (user, initial_user)
        join_condition = join(self.model, user, self.model.c.user_id==user.c.id) \
                        .join(initial_user, self.model.c.user_iniciator_id==initial_user.c.id)
        query_condition = or_(
                self.model.c.user_id==current_user.id, 
                self.model.c.user_iniciator_id==current_user.id
            )
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


    async def read_one_by_companion(self, current_user: UserSchema, user_id: int):
        initial_user = user.alias("initial_user")
        join_models = (user, initial_user)
        join_condition = join(self.model, user, self.model.c.user_id==user.c.id) \
                        .join(initial_user, self.model.c.user_iniciator_id==initial_user.c.id)
        query_condition = or_(
            and_(self.model.c.user_id==current_user.id, self.model.c.user_iniciator_id==user_id),
            and_(self.model.c.user_id==user_id, self.model.c.user_iniciator_id==current_user.id)
        )
        return await self.read_one_by_condition(
            join_models=join_models,
            join_condition=join_condition,
            query_condition=query_condition
        )



crud_chat = CRUDChat(chat)
