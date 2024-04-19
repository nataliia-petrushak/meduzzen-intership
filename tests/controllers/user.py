import uuid

from starlette import status
from starlette.testclient import TestClient

from tests.constants import user_signup_data, user_update_data, user_bad_data


def test_create_user_endpoint(client: TestClient) -> None:
    response = client.post("/users", json=user_signup_data)
    assert response.status_code == status.HTTP_201_CREATED
    assert response.json()["username"] == user_signup_data["username"]


def test_can_not_create_user_with_bad_data(client: TestClient) -> None:
    response = client.post("/users", json=user_bad_data)
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


async def test_get_user_list_endpoint(client: TestClient) -> None:
    response = client.get("/users")
    assert response.status_code == status.HTTP_200_OK


def test_get_user_by_id_endpoint(client: TestClient) -> None:
    users = client.get("/users")
    user_id = users.json()[0]["id"]
    response = client.get(f"/users/{user_id}")

    assert response.status_code == status.HTTP_200_OK
    assert response.json()["id"] == user_id

    key_2 = uuid.uuid4()
    response_2 = client.get(f"/users/{key_2}")
    assert response_2.status_code == status.HTTP_404_NOT_FOUND


async def test_update_user_endpoint(client: TestClient) -> None:
    users = client.get("/users")
    user_id = users.json()[0]["id"]
    response = client.patch(f"/users/{user_id}", json=user_update_data)

    assert response.status_code == status.HTTP_200_OK
    assert response.json()["username"] == user_update_data["username"]
    assert response.json()["email"] == user_update_data["email"]


def test_delete_user_endpoint(client: TestClient) -> None:
    users = client.get("/users")
    user_id = users.json()[0]["id"]
    response = client.delete(f"/users/{user_id}")

    assert response.status_code == status.HTTP_204_NO_CONTENT

    response_2 = client.get(f"/users/{user_id}")

    assert response_2.status_code == status.HTTP_404_NOT_FOUND
