import uuid

import pytest
from httpx import AsyncClient
from starlette import status


@pytest.fixture
def user_signup_data():
    return {
        "username": "test_user",
        "email": "test@example.com",
        "password": "test_password",
    }


@pytest.fixture
def user_update_data():
    return {"username": "Updated", "email": "user@user.com", "password": "<PASSWORD>"}


@pytest.mark.asyncio
async def test_create_user(ac: AsyncClient, user_signup_data) -> None:
    response = await ac.post("/users/", json=user_signup_data)
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["username"] == user_signup_data["username"]


@pytest.mark.asyncio
async def test_can_not_create_user_with_bad_data(
    ac: AsyncClient, user_signup_data
) -> None:
    response = await ac.post("/users/", json=user_signup_data.update({"name": "Ilona"}))
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


@pytest.mark.asyncio
async def test_get_user_list(ac: AsyncClient) -> None:
    response = await ac.get("/users/")
    assert response.status_code == status.HTTP_200_OK


@pytest.mark.asyncio
async def test_get_user_by_id(ac: AsyncClient) -> None:
    users = await ac.get("/users/")
    user_id = users.json()[0]["id"]
    response = await ac.get(f"/users/{user_id}/")

    assert response.status_code == status.HTTP_200_OK
    assert response.json()["id"] == user_id

    key_2 = uuid.uuid4()
    response_2 = await ac.get(f"/users/{key_2}/")
    assert response_2.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.asyncio
async def test_update_user(ac: AsyncClient, user_update_data) -> None:
    users = await ac.get("/users/")
    user_id = users.json()[0]["id"]
    response = await ac.patch(f"/users/{user_id}/", json=user_update_data)

    assert response.status_code == status.HTTP_200_OK
    assert response.json()["username"] == user_update_data["username"]
    assert response.json()["email"] == user_update_data["email"]


@pytest.mark.asyncio
async def test_delete_user(ac: AsyncClient) -> None:
    users = await ac.get("/users/")
    user_id = users.json()[0]["id"]
    response = await ac.delete(f"/users/{user_id}/")

    assert response.status_code == status.HTTP_200_OK

    response_2 = await ac.get(f"/users/{user_id}/")

    assert response_2.status_code == status.HTTP_404_NOT_FOUND
