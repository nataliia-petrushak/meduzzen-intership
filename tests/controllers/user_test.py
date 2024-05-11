from uuid import UUID
from fastapi import status
from fastapi.testclient import TestClient

from tests.constants import (
    user_signup_data,
    user_update_data,
    user_bad_data,
    user_payload,
)


async def test_get_user_list_endpoint(
    client: TestClient, prepare_database, fill_database
) -> None:
    response = client.get("users/")
    result = response.json()
    assert response.status_code == status.HTTP_200_OK
    assert result[0]["username"] == user_payload[0]["username"]
    assert result[1]["username"] == user_payload[1]["username"]
    assert result[2]["username"] == user_payload[2]["username"]


def test_get_user_by_id_endpoint(
    client: TestClient, user_id: UUID, prepare_database, fill_database
) -> None:
    response = client.get(f"users/{user_id}")

    assert response.status_code == status.HTTP_200_OK
    assert response.json()["id"] == str(user_id)

    response_2 = client.get("/users/af3efcf6-9c61-4865-832f-5250f7fb8aec")
    assert response_2.status_code == status.HTTP_404_NOT_FOUND


async def test_update_user_endpoint(
    client: TestClient, user_id: UUID, prepare_database, fill_database, token
) -> None:
    response = client.patch(
        f"users/{user_id}",
        json=user_update_data,
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == status.HTTP_200_OK
    assert response.json()["username"] == user_update_data["username"]


def test_delete_user_endpoint(
    client: TestClient, user_id: UUID, prepare_database, fill_database, token
) -> None:
    response = client.patch(
        f"users/{user_id}/deactivate", headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == status.HTTP_204_NO_CONTENT
