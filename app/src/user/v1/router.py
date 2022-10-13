from fastapi import APIRouter, Depends, Response

from src.crud.crud_user import crud_user
from src.auth.security import registartion_user
from src.sample_schemas import Params, BadRequest
from src.user.schema import UserListSchema, UserInput, UserSchema
from src.auth.security import get_current_user

user_router = APIRouter(prefix='/users')

@user_router.get('/', response_model=UserListSchema)
async def get_users(params: Params = Depends(), current_user: UserSchema | None = Depends(get_current_user)):
    users, total = await crud_user.read(params)
    response = UserListSchema(items=users, total=total)
    return response


@user_router.post('/', status_code=201, responses={400: {"model": BadRequest}})
async def post_user(user: UserInput, response: Response):
    response.status_code, _ = await registartion_user(user)
    return response


@user_router.get('/{id:int}', response_model=UserSchema, 
                              responses={404: {"model": BadRequest}})
async def get_user(id:int):
    response = await crud_user.read_one_by_condition(id=id)
    return response


@user_router.delete('/{id:int}', status_code=200, 
                    responses={400: {"model": BadRequest}})
async def delete_user(id: int, response: Response):
    response.status_code = await crud_user.delete(id)
    return response
