from src.sample_schemas import CamelModel
from src.message.schema import MessageListSchema, MessageSchema
from src.user.schema import UserSchema


class ChatBase(CamelModel):
    sel: UserSchema

class ChatSchema(ChatBase):
    id: int

class ChatListSchema(CamelModel):
    chats: list[ChatSchema]

class ChatMessageSchema(CamelModel):
    messages: list[MessageSchema]
