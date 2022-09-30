from src.sample_schemas import CamelModel, Meta
from src.user.schema import UserSchema


class MessageBase(CamelModel):
    message: str
    sender_id: int
    recipient_id: int
    chat_id: int
    
class MessageInput(MessageBase):
    pass

class MessageSchema(MessageBase):
    id: int


class MessageListSchema(CamelModel):
    items: list[MessageSchema]
