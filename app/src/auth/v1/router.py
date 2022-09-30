from fastapi import APIRouter, Depends, HTTPException, Response, Cookie
from fastapi.security import OAuth2PasswordRequestForm

from http import HTTPStatus
from datetime import timedelta

from src.auth.schema import Token, AuthInput, RegistrationInput
from src.user.schema import UserSchema
from src.config import get_settings, Settings
from src.auth.security import authenticate_user, create_access_token, get_current_user, logout_user, registartion_user

auth_router = APIRouter(prefix="/auth")

@auth_router.post("/login", response_model=Token)
async def login(auth_data: AuthInput, 
                response: Response,
                settings: Settings = Depends(get_settings)):
    user = await authenticate_user(auth_data.username, auth_data.password)
    access_token = await create_access_token(
        data={"sub": user.username}
    )
    response.set_cookie("accessToken", access_token)
    response.status_code = 200
    return response

@auth_router.post("/registration")
async def registration(registartion_data: RegistrationInput, response: Response):
    response.status_code = await registartion_user(registartion_data)
    return response

@auth_router.get("/me", response_model=UserSchema)
async def get_me(access_token: str = Cookie(alias="accessToken"),
                 current_user: UserSchema = Depends(get_current_user)):
    return current_user

@auth_router.post("/logout")
async def logout(access_token: str = Cookie(alias="accessToken"),
                 response: int = Depends(logout_user)):
    return response
