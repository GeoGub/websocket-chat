from src.sample_schemas import CamalModel


class AuthInput(CamalModel):
    username: str
    password: str

class RegistrationInput(AuthInput):
    pass

class Token(CamalModel):
    access_token: str
    token_type: str


class TokenData(CamalModel):
    username: str | None = None
