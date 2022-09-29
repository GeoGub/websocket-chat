from src.sample_schemas import CamalModel, Meta

class UserBase(CamalModel):
    username: str

class UserInput(UserBase):
    password: str

class UserSchema(UserBase):
    id: int

class UserListSchema(Meta):
    items: list[UserSchema]
