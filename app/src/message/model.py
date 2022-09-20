from sqlalchemy import Table, Column, Integer, String, ForeignKey

from src.database import metadata
from ..user.model import user

message = Table(
    "messages", 
    metadata,
    Column("id", Integer, primary_key=True),
    Column("message", String),
    Column("sender_id", Integer, ForeignKey("user.id")),
    Column("recipient_id", Integer)
)