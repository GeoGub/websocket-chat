from fastapi import APIRouter, Depends, Response

from src import crud
from src.database import database
from src.sample_schemas import Params, BadRequest
from src.user.schema import UserListSchema, UserInput, UserSchema

user_router = APIRouter(prefix='/users')

@user_router.get('/', response_model=UserListSchema)
async def get_users(params: Params = Depends()):
    users, total = await crud.read_users(database, params)
    response = UserListSchema(items=users, total=total)
    return response

@user_router.post('/', status_code=201, responses={400: {"model": BadRequest}})
async def post_user(user: UserInput, response: Response):
    response.status_code = await crud.create_user(database, user)
    return response

@user_router.get('/{id:int}', response_model=UserSchema, 
                              responses={404: {"model": BadRequest}})
async def get_user(id:int):
    response = await crud.read_user(database, id)
    return response

@user_router.delete('/{id:int}', status_code=200, 
                    responses={400: {"model": BadRequest}})
async def delete_user(id: int, response: Response):
    response.status_code = await crud.delete_user(database, id)
    return response
