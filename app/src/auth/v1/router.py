from fastapi import APIRouter, Depends, HTTPException, Response
from fastapi.security import OAuth2PasswordRequestForm

from http import HTTPStatus
from datetime import timedelta

from src.database import database
from src.auth.schema import Token, AuthInput, RegistrationInput
from src.user.schema import UserSchema
from src.config import get_settings, Settings
from src.auth.security import authenticate_user, create_access_token, get_current_user, registartion_user

auth_router = APIRouter(prefix="/auth")

@auth_router.post("/login", response_model=Token)
async def login(auth_data: AuthInput, 
                settings: Settings = Depends(get_settings)):
    user = await authenticate_user(database, auth_data.username, auth_data.password)
    access_token_expires = timedelta(minutes=settings.access_token_expire_minutes)
    access_token = await create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

@auth_router.post("/registration")
async def registration(registartion_data: RegistrationInput, response: Response):
    response.status_code = await registartion_user(database, registartion_data)
    return response

@auth_router.get("/me", response_model=UserSchema)
async def get_me(current_user: UserSchema = Depends(get_current_user)):
    return current_user
