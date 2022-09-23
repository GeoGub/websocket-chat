from src.sample_schemas import CamalModel, Meta

class UserBase(CamalModel):
    username: str
    password: str

class UserInput(UserBase):
    pass

class UserSchema(UserBase):
    id: int

    # class Config:
    #     orm_mode = True

class UserListSchema(Meta):
    items: list[UserSchema]
