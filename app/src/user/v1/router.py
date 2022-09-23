from fastapi import APIRouter, Depends

from src.crud import delete_user, read_users, create_user, read_user
from src.database import database
from src.sample_schemas import Params
from src.user.schema import UserListSchema, UserInput, UserSchema

user_router = APIRouter(prefix='/users')

@user_router.get('/', response_model=UserListSchema)
async def get_users(params: Params = Depends()):
    users, total = await read_users(database)
    response = UserListSchema(items=users, total=total)
    return response

@user_router.post('/')
async def post_user(user: UserInput):
    response = await create_user(database, user)
    return response

@user_router.get('/{id:int}', response_model=UserSchema)
async def get_user(id:int):
    user = await read_user(database, id)
    return user

@user_router.delete('/{id:int}')
async def del_user(id: int):
    response = await delete_user(database, id)
    return response
