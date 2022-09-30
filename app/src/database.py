import databases
import sqlalchemy
import aioredis

from src.config import get_settings

database = databases.Database(get_settings().database_url)
metadata = sqlalchemy.MetaData()
# redis = aioredis.from_url(get_settings().redis_host,
#                          port=get_settings().redis_port,
#                          db=get_settings().redis_db, 
#                          password=get_settings().redis_password)

blocklist = aioredis.from_url(get_settings().redis_host,
                         port=get_settings().redis_port,
                         db=get_settings().blocklist_db, 
                         password=get_settings().redis_password)