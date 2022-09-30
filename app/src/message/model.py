from sqlalchemy import Table, Column, Integer, String, ForeignKey

from src.database import metadata
from ..chat.model import chat

message = Table(
    "messages", 
    metadata,
    Column("id", Integer, primary_key=True),
    Column("message", String),
    Column("sender_id", Integer, ForeignKey("users.id", onupdate="CASCADE", ondelete="CASCADE")),
    Column("recipient_id", Integer, ForeignKey("users.id", onupdate="CASCADE", ondelete="CASCADE")),
    Column("chat_id", Integer, ForeignKey("chats.id", onupdate="CASCADE", ondelete="CASCADE"))
)