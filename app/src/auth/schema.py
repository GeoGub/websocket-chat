from fastapi.param_functions import Form

from src.sample_schemas import CamalModel


class AuthInput(CamalModel):
    username: str = Form()
    password: str = Form()

class RegistrationInput(AuthInput):
    pass

class Token(CamalModel):
    access_token: str
    refresh_token: str
    token_type: str


class TokenData(CamalModel):
    username: str | None = None
