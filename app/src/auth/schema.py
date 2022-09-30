from fastapi.param_functions import Form

from src.sample_schemas import CamelModel


class AuthInput(CamelModel):
    username: str = Form()
    password: str = Form()

class RegistrationInput(AuthInput):
    pass

class Token(CamelModel):
    access_token: str
    refresh_token: str
    token_type: str


class TokenData(CamelModel):
    username: str | None = None
