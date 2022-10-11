from src.sample_schemas import CamelModel, Meta
from src.user.schema import UserSchema

class ChatBase(CamelModel):
    user_iniciator: UserSchema
    user: UserSchema

class ChatInput(ChatBase):
    pass

class ChatSchema(ChatBase):
    id: int

class ChatListSchema(Meta):
    items: list[ChatSchema]
