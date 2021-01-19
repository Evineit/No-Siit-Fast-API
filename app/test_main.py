import os

from fastapi.testclient import TestClient
from fastapi import status
from dotenv import load_dotenv
from starlette import responses

import main

client = TestClient(main.app)
load_dotenv()


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


def test_session_invalid_session():
    response = client.get("/session", cookies={"PHPSESSID": "randomsessid"})
    assert response.status_code == 401


def test_login_correct_data():
    response_login = client.post(
        "/login",
        data={
            "usuario": os.environ.get("VALID_USER"),
            "contrasena": os.environ.get("VALID_PASS"),
        },
    )
    session_cookies = client.cookies.get_dict()
    response_session = client.get("/session",cookies=session_cookies)
    assert response_login.status_code == status.HTTP_200_OK
    assert response_session.status_code == status.HTTP_200_OK

def test_no_session_between_tests():
    response = client.get("/session")
    assert response.status_code == 401


def test_login_no_duplicate_session():
    client_2 = TestClient(main.app)
    response_client_1 = client.post(
        "/login",
        data={
            "usuario": os.environ.get("VALID_USER"),
            "contrasena": os.environ.get("VALID_PASS"),
        }
    )
    session_1_cookies = client.cookies.get_dict()
    response_client_1_session = client.get("/session", cookies=session_1_cookies)

    response_client_2_session = client_2.get("/session")
    assert response_client_1.status_code == 200
    assert response_client_1_session.status_code == status.HTTP_200_OK
    assert response_client_2_session.status_code == 401

def test_calif_no_session():
    response = client.get("/calif")
    assert response.status_code == status.HTTP_401_UNAUTHORIZED

def test_calif_invalid_session():
    response = client.get("/calif")
    assert response.status_code == status.HTTP_401_UNAUTHORIZED

def test_calif_valid_session():
    response_client_1 = client.post(
        "/login",
        data={
            "usuario": os.environ.get("VALID_USER"),
            "contrasena": os.environ.get("VALID_PASS"),
        }
    )
    session_1_cookies = client.cookies.get_dict()
    response_client_1_session = client.get("/session", cookies=session_1_cookies)
    assert response_client_1.status_code == 200
    assert response_client_1_session.status_code == status.HTTP_200_OK

def test_signout_no_session():
    response = client.get("/signout")
    assert response.status_code == status.HTTP_400_BAD_REQUEST

def test_signout_session():
    response = client.get("/signout", cookies={"PHPSESSID": "test"})
    assert response.status_code == status.HTTP_200_OK
