from sqlalchemy import Table, Column, Integer, String, ForeignKey

from src.database import metadata

message = Table(
    "messages", 
    metadata,
    Column("id", Integer, primary_key=True),
    Column("message", String),
    Column("sender_id", Integer, ForeignKey("users.id", onupdate="CASCADE", ondelete="CASCADE"))
)