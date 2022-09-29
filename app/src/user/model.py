from enum import unique
from sqlalchemy import Table, Column, Integer, String

from src.database import metadata

user = Table(
    "users",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("username", String, unique=True),
    Column("password", String)
)

