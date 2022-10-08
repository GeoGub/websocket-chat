from fastapi import Depends

from sqlalchemy import create_engine, MetaData
from fastapi.testclient import TestClient
import pytest

from src.main import app

# @pytest.fixture(scope="session")
# def db_engine():
#     engine = create_engine(SQLALCHEMY_DATABASE_URL)
#     metadata = MetaData()
#     metadata.create_all(bind=engine)
#     yield engine


# @pytest.fixture(scope="function")
# def db(db_engine):
#     connection = db_engine.connect()

#     # begin a non-ORM transaction
#     transaction = connection.begin()

#     # bind an individual Session to the connection
#     db = Session(bind=connection)
#     # db = Session(db_engine)

#     yield db

#     db.rollback()
#     connection.close()

# @pytest.fixture() 
# def client(): 
#     with TestClient(app) as client:   # context manager will invoke startup event 
#         yield client