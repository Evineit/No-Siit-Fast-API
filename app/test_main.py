from warnings import filterwarnings

from fastapi.testclient import TestClient
from fastapi import status
from urllib3.exceptions import InsecureRequestWarning

import main

client = TestClient(main.app)
filterwarnings(action='ignore', category=InsecureRequestWarning)

def test_read_main():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello World"}


def test_login_no_form_data():
    response = client.post("/login")
    assert response.status_code == 400


def test_login_invalid_data():
    response = client.post("/login", data={"usuario": "10041101", "contrasena": "1111"})
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_session_no_cookie():
    response = client.get("/session")
    assert response.status_code == 401
