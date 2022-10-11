from databases import Database
from sqlalchemy import select, or_

from src.user.schema import UserSchema
from .crud_base import CRUDBase
from src.user.model import user, user_columns
from src.database import database as db



class CRUDUser(CRUDBase):
    
    async def read_one_by_condition(self, **kwargs) -> UserSchema:
        query_condition = tuple(user_columns[key] == kwargs[key] for key in kwargs.keys())
        return await super().read_one_by_condition(query_condition)


crud_user = CRUDUser(user)
