from databases import Database
from sqlalchemy import func, select, delete, insert

from src.user.model import user
from src.user.schema import UserInput

async def read_users(db: Database):
    users = await db.fetch_all(select(user))
    total = await db.execute(select(func.count()).select_from(user))
    return users, total

async def create_user(db: Database, value: UserInput):
    transaction = await db.transaction()
    try:
        await db.execute(insert(user, value.dict()))
    except Exception as e:
        await transaction.rollback()
        return {'msg': 'Exception'}
    else:
        await transaction.commit()
        return {'msg': 'all right'}

async def read_user(db: Database, id: int):
    query = select(user).where(user.c.id==id)
    return await db.fetch_one(query)

async def delete_user(db: Database, id: int):
    query = delete(user).where(user.c.id==id).returning(user.c.id)
    user_id = await db.execute(query)
    if user_id:
        return 200
    return 401
