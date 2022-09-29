from databases import Database
from jose import JWTError, jwt
from passlib.context import CryptContext
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer

from datetime import datetime, timedelta
from http import HTTPStatus

from src.auth.schema import TokenData, Token, RegistrationInput
from src.config import get_settings, Settings
from src.user.schema import UserSchema
from src.crud.crud_user import crud_user

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)

async def create_access_token(data: dict, settings: Settings = Depends(get_settings), expires_delta: timedelta | None = None):
    to_encode = data.copy()
    # Неправильно отрабатывает Depends
    print(settings)
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.secret_key, algorithm=settings.algorithm)
    return encoded_jwt

async def get_current_user(token: str = Depends(oauth2_scheme), settings: Settings = Depends(get_settings)):
    credentials_exception = HTTPException(
        status_code=HTTPStatus.UNAUTHORIZED.value,
        detail=HTTPStatus.UNAUTHORIZED.phrase
    )
    try:
        payload = jwt.decode(token, settings.secret_key, algorithms=settings.algorithm)
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception
    user = crud_user.read_user_by_username(username=token_data.username)
    if user is None:
        raise credentials_exception
    user = UserSchema(id=user.id, username=user.username).dict()
    return user

async def authenticate_user(db: Database, username: str, password: str):
    user = await crud_user.read_user_by_username(db, username)
    if not user or not verify_password(password, user.password):
        raise HTTPException(
            status_code=HTTPStatus.UNAUTHORIZED.value,
            detail=HTTPStatus.UNAUTHORIZED.phrase,
        )
    return user

async def registartion_user(db: Database, user_data: RegistrationInput) -> HTTPStatus:
    user_data.password = get_password_hash(user_data.password)
    status_code = await crud_user.create(db, user_data)
    return status_code

