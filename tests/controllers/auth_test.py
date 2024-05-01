import pytest
from starlette import status
from starlette.testclient import TestClient

from tests.constants import user_signup_data, user_bad_data


@pytest.mark.asyncio
async def test_create_user_endpoint(client: TestClient, prepare_database) -> None:
    response = client.post("auth/register", json=user_signup_data)
    assert response.status_code == status.HTTP_201_CREATED
    assert response.json()["username"] == user_signup_data["username"]
    assert response.json()["email"] == user_signup_data["email"]


@pytest.mark.asyncio
async def test_can_not_create_user_with_bad_data(
    client: TestClient, prepare_database
) -> None:
    response = client.post("auth/register", json=user_bad_data)
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


@pytest.mark.asyncio
async def test_user_login(client: TestClient, prepare_database, fill_database) -> None:
    response = client.post(
        "auth/login", json={"email": "test_1@test.com", "password": "string"}
    )

    assert response.status_code == status.HTTP_200_OK
    assert "access_token" in response.json()
    assert "token_type" in response.json()


@pytest.mark.asyncio
async def test_user_me(
    client: TestClient, token: str, prepare_database, fill_database
) -> None:
    response = client.get("auth/me", headers={"Authorization": f"Bearer {token}"})
    result = response.json()

    assert response.status_code == status.HTTP_200_OK
    assert result["username"] == "test_1"
