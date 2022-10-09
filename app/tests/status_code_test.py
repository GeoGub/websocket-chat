from fastapi import Response
from fastapi.testclient import TestClient

from tests import client, test_data


def test_correct_registration(client: TestClient, test_data: dict):
    data = test_data["auth"]["register"]["correct"]
    response = client.post("/auth/registration", json=data["payload"])
    assert response.status_code == data["expected"]["status_code"]

def test_incorrect_registration(client: TestClient, test_data: dict):
    data = test_data["auth"]["register"]["incorrect"]
    response = client.post("/auth/registration", json=data["payload"])
    assert response.status_code == data["expected"]["status_code"]

def test_correct_login(client: TestClient, test_data: dict):
    data = test_data["auth"]["login"]["correct"][0]
    response = client.post("/auth/login", json=data["payload"])
    assert response.status_code == data["expected"]["status_code"]

def test_incorrect_login_username(client: TestClient, test_data: dict):
    data = test_data["auth"]["login"]["incorrect"][0]
    response = client.post("/auth/login", json=data["payload"])
    assert response.status_code == data["expected"]["status_code"]


def test_incorrect_login_password(client: TestClient, test_data: dict):
    data = test_data["auth"]["login"]["incorrect"][1]
    response = client.post("/auth/login", json=data["payload"])
    assert response.status_code == data["expected"]["status_code"]

def test_correct_get_messages(client: TestClient, test_data: dict):
    pass
