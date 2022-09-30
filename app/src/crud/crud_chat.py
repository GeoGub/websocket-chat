from databases import Database
from fastapi import Depends
from sqlalchemy import select, or_

from .crud_base import CRUDBase
from src.user.model import user
from src.user.schema import UserSchema
from src.chat.model import chat



class CRUDChat(CRUDBase):
    async def read(self, db: Database, current_user: UserSchema):
        initiator, recipient = user.alias("initiator"), user.alias("recipient")
        query = select(self.model, initiator, recipient).select_from(
            self.model.join(initiator, self.model.c.initiator_id==initiator.c.id) \
                      .join(recipient, self.model.c.recipient_id==recipient.c.id)
        ).where(or_(self.model.c.initiator_id==current_user.id, self.model.c.recipient_id==current_user.id))
        chats = await db.fetch_all(query)
        return chats

crud_chat = CRUDChat(chat)