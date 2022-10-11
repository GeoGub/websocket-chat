from sqlalchemy import Table, Column, Integer, String, ForeignKey

from src.database import metadata

chat = Table(
    "chats",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("user_iniciator_id", Integer, ForeignKey("users.id", onupdate="CASCADE", ondelete="CASCADE")),
    Column("user_id", Integer, ForeignKey("users.id", onupdate="CASCADE", ondelete="CASCADE"))
)