from app import schemas
from app.config import settings
import pytest
from jose import jwt

# def test_root(client):
#     res = client.get("/")

#     assert res.status_code == 200
#     assert res.json().get('message') == 'Welcome to my API'

def test_create_user(client):
    res = client.post("/users/", json={"email": "car@gmail.com", "password": "123"})
    new_user = schemas.UserOut(**res.json())

    assert res.status_code == 201
    assert new_user.email == "car@gmail.com"

def test_login_user(client, test_user):
    res = client.post("/login", data={"username": test_user['email'], "password": test_user['password']})
    login_res = schemas.Token(**res.json())
    payload = jwt.decode(login_res.access_token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
    id = payload.get("user_id")

    assert res.status_code == 200
    assert id == test_user['id']
    assert login_res.token_type == "bearer"

@pytest.mark.parametrize("username, password, status_code", [
                         ('wrongemail@mail.com', '123', 403),
                         ('car@gmail.com', 'wrongpassword', 403),
                         ('wrongemail@gmail.com', 'wrongpassword', 403),
                         (None, '123', 403),
                         ('car@gmail.com', None, 403)
                         ])
def test_failed_login(test_user, client, username, password, status_code):
    res = client.post("/login", data={"username": username, "password": password})

    assert res.status_code == status_code