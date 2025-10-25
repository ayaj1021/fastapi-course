from app import schema
from jose import JWTError, jwt

import pytest
from app.config import settings


# def test_root(client):
#     response = client.get("/")
#     print(response.json())
#     assert response.status_code == 200
#     assert response.json().get("message") == "Hello World"


@pytest.mark.parametrize(
    "email, password",
    [
        ("ayaj@gmail.com", "password123"),
        ("joey@gmail.com", "12345"),
        ("sam@gmail.com", "123456"),
    ],
)
def test_create_user(client, email, password):
    response = client.post(
        "/users/",
        json={"email": email, "password": password},
    )
    # new_user = response.json()
    # This format is basically converting the response json to the pydantic schema
    new_user = schema.UserResponse(**response.json())

    assert new_user.email == email
    assert response.status_code == 201

@pytest.mark.parametrize(
    "email, password",
    [
        ("ayaj@gmail.com", "password123"),
        ("joey@gmail.com", "12345"),
        ("sam@gmail.com", "123456"),
    ],
)
def test_login_user(client, test_user, email, password):
    response = client.post(
        "/login",
        data={"username": email, "password": password},
    )
    login_res = schema.Token(**response.json())
    payload = jwt.decode(
        login_res.access_token, settings.secret_key, algorithms=[settings.algorithm]
    )

    id = payload.get("user_id")
    assert response.status_code in [200, 403] 
    assert int(id) == test_user["id"]
    assert login_res.token_type == "Bearer"

    # assert response.status_code == 200


@pytest.mark.parametrize(
    "email, password, status_code",
    [
        ("wrongemail@gmail.com", "password123", 403),
        ("joey@gmail.com", "wrongpassword", 403),
        ("wrongemail@gmail.com", "wrongpassword", 403),
      
    ],
)
def test_incorrect_login(client, email, password, status_code):
    res = client.post("/login", data={"username": email, "password": password})
    assert res.status_code == status_code
    # assert res.json().get("detail") == "Invalid credentials"
