from fastapi.testclient import TestClient
import pytest

from typing import Generator
import os
import json

from src.main import app

@pytest.fixture() 
def client() -> Generator: 
    with TestClient(app) as client:   # context manager will invoke startup event 
        yield client

@pytest.fixture(scope="function")
def test_data() -> dict:
    print(os.path)
    with open(r"D:\websocket-chat\app\tests\mocks.json", "r") as file:
        data = json.loads(file.read())

    return data