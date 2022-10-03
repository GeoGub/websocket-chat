from typing import Optional

from src.sample_schemas import CamelModel, Meta
from src.user.schema import UserSchema


class MessageBase(CamelModel):
    message: str
    sender_id: int | None
    
class MessageInput(MessageBase):
    pass

class MessageSchema(MessageBase):
    id: int


class MessageListSchema(Meta):
    items: list[MessageSchema]
