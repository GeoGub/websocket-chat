

from .crud_base import CRUDBase
from src.chat.model import chat


class CRUDChat(CRUDBase):
    
    async def read(self, params: dict):
        join_condition = None
        return await super().read(params, join_condition)


crud_chat = CRUDChat(chat)
