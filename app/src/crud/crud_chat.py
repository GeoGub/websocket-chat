

from .crud_base import CRUDBase
from src.chat.model import chat


class CRUDChat(CRUDBase):
    
    async def read(self, params: dict):
        join_condition = None
        return await super().read(params, join_condition)

    async def read_by_companion(self):
        pass


crud_chat = CRUDChat(chat)
