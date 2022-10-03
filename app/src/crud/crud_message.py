from databases import Database

from .crud_base import CRUDBase
from src.message.model import message


class CRUDMessage(CRUDBase):
    pass
    # async def read(self, db: Database):
    #     pass

crud_message = CRUDMessage(message)