import databases
import sqlalchemy

from src.config import get_settings

database = databases.Database(get_settings().database_url)
metadata = sqlalchemy.MetaData()


