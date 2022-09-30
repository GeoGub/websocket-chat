from sqlalchemy import Table, Column, Integer, String, ForeignKey

from src.database import metadata
from src.user.model import user

chat = Table(
    "chats",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("initiator_id", Integer, ForeignKey("users.id", onupdate="CASCADE", ondelete="CASCADE")),
    Column("recipient_id", Integer, ForeignKey("users.id", onupdate="CASCADE", ondelete="CASCADE"))
)