from types import NoneType
from jose import JWTError, jwt
from passlib.context import CryptContext
from fastapi import Depends, HTTPException, Cookie

from datetime import datetime, timedelta
from http import HTTPStatus

from src.auth.schema import TokenData, Token, RegistrationInput
from src.config import get_settings, Settings
from src.database import database, blocklist
from src.user.schema import UserSchema
from src.crud.crud_user import crud_user

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


async def create_access_token(data: dict, 
                              settings: Settings = get_settings()):
    to_encode = data.copy()
    expire = datetime.now() + timedelta(minutes=settings.access_token_expire_minutes)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.secret_key, algorithm=settings.algorithm)
    return encoded_jwt


async def is_token_revoke(access_token: str = Cookie(alias="accessToken")):
    if await blocklist.get(access_token) is not None:
        raise HTTPException(status_code=HTTPStatus.UNAUTHORIZED.value, 
                    detail="Token is revoked")


async def get_current_user(access_token: str = Cookie(alias="accessToken"),
                           _: NoneType = Depends(is_token_revoke),
                           settings: Settings = Depends(get_settings)):
    credentials_exception = HTTPException(
        status_code=HTTPStatus.UNAUTHORIZED.value,
        detail=HTTPStatus.UNAUTHORIZED.phrase
    )
    try:
        payload = jwt.decode(access_token, settings.secret_key, algorithms=settings.algorithm)
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception
    user = await crud_user.read_user_by_username(database, username=token_data.username)
    if user is None:
        raise credentials_exception
    user = UserSchema(id=user.id, username=user.username).dict()
    return user


async def authenticate_user(username: str, password: str):
    user = await crud_user.read_user_by_username(database, username)
    if not user or not verify_password(password, user.password):
        raise HTTPException(
            status_code=HTTPStatus.UNAUTHORIZED.value,
            detail=HTTPStatus.UNAUTHORIZED.phrase,
        )
    return user


async def registartion_user(user_data: RegistrationInput) -> HTTPStatus:
    user_data.password = get_password_hash(user_data.password)
    status_code = await crud_user.create(database, user_data)
    return status_code


async def logout_user(access_token: str = Cookie(alias="accessToken"),
                      settings: Settings = Depends(get_settings),):
    await blocklist.set(access_token, "", ex=settings.access_token_expire_minutes)
    return HTTPStatus.OK.value
