import databases
import sqlalchemy

DATABASE_URL = "postgresql://postgres:root@127.0.0.1/websocket"
database = databases.Database(DATABASE_URL)
metadata = sqlalchemy.MetaData()


