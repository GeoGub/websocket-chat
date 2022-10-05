from src.sample_schemas import CamelModel, Meta

class UserBase(CamelModel):
    username: str

class UserInput(UserBase):
    password: str

class UserSchema(UserBase):
    id: int

class UserListSchema(Meta):
    items: list[UserSchema]
