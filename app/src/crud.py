from databases import Database
from sqlalchemy import func, select, delete, insert
from fastapi import HTTPException

from http import HTTPStatus

from src.sample_schemas import Params
from src.user.model import user
from src.user.schema import UserInput

async def read_users(db: Database, params: Params):
    query = select(user).limit(params.limit).offset(params.limit*params.offset)
    users = await db.fetch_all(query)
    total = await db.execute(select(func.count()).select_from(user))
    return users, total

async def create_user(db: Database, value: UserInput):
    transaction = await db.transaction()
    try:
        await db.execute(insert(user, value.dict()))
    except Exception as e:
        await transaction.rollback()
        raise HTTPException(status_code=HTTPStatus.BAD_REQUEST.value, 
                            detail=HTTPStatus.BAD_REQUEST.phrase)
    else:
        await transaction.commit()
    return HTTPStatus.CREATED.value

async def read_user(db: Database, id: int):
    query = select(user).where(user.c.id==id)
    user_by_id = await db.fetch_one(query)
    if not user_by_id:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND.value, 
                            detail=HTTPStatus.NOT_FOUND.phrase)
    return user_by_id

async def delete_user(db: Database, id: int):
    query = delete(user).where(user.c.id==id).returning(user.c.id)
    user_id = await db.execute(query)
    if not user_id:
        raise HTTPException(status_code=HTTPStatus.BAD_REQUEST.value, 
                            detail=HTTPStatus.BAD_REQUEST.phrase)
    return HTTPStatus.OK.value

async def read_messages(db: Database):
    pass
