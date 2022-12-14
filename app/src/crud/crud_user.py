from databases import Database
from sqlalchemy import select

from .crud_base import CRUDBase
from src.user.model import user



class CRUDUser(CRUDBase):
    async def read_user_by_username(self, db: Database, username: str):
        query = select(self.model).where(self.model.c.username==username)
        user_by_username = await db.fetch_one(query)
        if user_by_username:
            return user_by_username

crud_user = CRUDUser(user)
