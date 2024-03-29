import os

from fastapi.testclient import TestClient
from fastapi import status
from dotenv import load_dotenv

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
    session_cookies = login_and_get_cookies()
    response_session = client.get("/session", cookies=session_cookies)
    assert response_session.status_code == status.HTTP_200_OK


def test_no_session_between_tests():
    response = client.get("/session")
    assert response.status_code == 401


def test_login_no_duplicate_session():
    client_2 = TestClient(main.app)
    session_1_cookies = login_and_get_cookies()
    response_client_1_session = client.get("/session", cookies=session_1_cookies)

    response_client_2_session = client_2.get("/session")
    assert response_client_1_session.status_code == status.HTTP_200_OK
    assert response_client_2_session.status_code == 401


def test_calif_no_session():
    response = client.get("/calif")
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_calif_invalid_session():
    response = client.get("/calif", cookies={"PHPSESSID": "test"})
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_calif_valid_session():
    session_1_cookies = login_and_get_cookies()
    response_client_1_session = client.get("/calif", cookies=session_1_cookies)
    assert response_client_1_session.status_code == status.HTTP_200_OK


def test_calif_remove_unnecessary_link():
    session_1_cookies = login_and_get_cookies()
    response_client_1_session = client.get("/calif", cookies=session_1_cookies)
    assert "<link" not in response_client_1_session.text

def test_kardex_no_session():
    response = client.get("/kardex")
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_kardex_invalid_session():
    response = client.get("/kardex", cookies={"PHPSESSID": "test"})
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_kardex_valid_session():
    session_1_cookies = login_and_get_cookies()
    response = client.get("/kardex", cookies=session_1_cookies)
    assert response.status_code == status.HTTP_200_OK


def test_avance_ret_no_session():
    response = client.get("/avance_reticular")
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    

def test_avance_ret_invalid_session():
    response = client.get("/avance_reticular", cookies={"PHPSESSID": "test"})
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_avance_ret_valid_session():
    session_1_cookies = login_and_get_cookies()
    response = client.get("/avance_reticular", cookies=session_1_cookies)
    assert response.status_code == status.HTTP_200_OK


def test_grupos_cargados_no_session():
    response = client.get("/grupos_cargados")
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_grupos_cargados_invalid_session():
    response = client.get("/grupos_cargados", cookies={"PHPSESSID": "test"})
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_grupos_cargados_valid_session():
    session_1_cookies = login_and_get_cookies()
    response_client_1_session = client.get("/grupos_cargados", cookies=session_1_cookies)
    assert response_client_1_session.status_code == status.HTTP_200_OK


def test_horario_no_session():
    response = client.get("/horario")
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_horario_invalid_session():
    response = client.get("/horario", cookies={"PHPSESSID": "test"})
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_horario_valid_session():
    session_cookies = login_and_get_cookies()
    response_1 = client.get("/horario", cookies=session_cookies)
    assert response_1.status_code == status.HTTP_200_OK


def test_signout_no_session():
    response = client.get("/signout")
    assert response.status_code == status.HTTP_400_BAD_REQUEST


def test_signout_session():
    response = client.get("/signout", cookies={"PHPSESSID": "test"})
    assert response.status_code == status.HTTP_200_OK


def test_signout_valid_session():
    session_1_cookies = login_and_get_cookies()
    response_client_session = client.get("/session", cookies=session_1_cookies)
    assert response_client_session.status_code == status.HTTP_200_OK

    logout_response = client.get("/signout", cookies=session_1_cookies)
    assert logout_response.status_code == status.HTTP_200_OK

    response_client_session_after = client.get("/session", cookies=session_1_cookies)
    assert response_client_session_after.status_code == status.HTTP_401_UNAUTHORIZED


def login_and_get_cookies():
    response_client_1 = client.post(
        "/login",
        data={
            "usuario": os.environ.get("VALID_USER"),
            "contrasena": os.environ.get("VALID_PASS"),
        }
    )
    assert response_client_1.status_code == 200
    return client.cookies.get_dict()
