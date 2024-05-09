from uuid import UUID

import pytest
from starlette import status
from starlette.testclient import TestClient

from tests.constants import (
    quiz_data,
    quiz_data_1_question,
    quiz_data_1_answer,
    quiz_update_data,
    quiz_payload,
)


@pytest.mark.asyncio
async def test_owner_create_quiz(
    client: TestClient,
    company_id: UUID,
    owner_token: str,
    prepare_database,
) -> None:
    response = client.post(
        f"company/{company_id}/quiz",
        headers={"Authorization": f"Bearer {owner_token}"},
        json=quiz_data,
    )

    assert response.status_code == status.HTTP_201_CREATED
    assert response.json()["name"] == quiz_data["name"]
    assert response.json()["description"] == quiz_data["description"]
    assert response.json()["questions"] == quiz_data["questions"]


@pytest.mark.asyncio
async def test_admin_create_quiz(
    client: TestClient,
    company_id: UUID,
    token: str,
    prepare_database,
    fill_db_with_admins,
) -> None:
    response = client.post(
        f"company/{company_id}/quiz",
        headers={"Authorization": f"Bearer {token}"},
        json=quiz_data,
    )

    assert response.status_code == status.HTTP_201_CREATED
    assert response.json()["name"] == quiz_data["name"]
    assert response.json()["description"] == quiz_data["description"]
    assert response.json()["questions"] == quiz_data["questions"]


@pytest.mark.asyncio
async def test_member_create_quiz_forbidden(
    client: TestClient,
    company_id: UUID,
    token: str,
    prepare_database,
    fill_db_with_members,
) -> None:
    response = client.post(
        f"company/{company_id}/quiz",
        headers={"Authorization": f"Bearer {token}"},
        json=quiz_data,
    )

    assert response.status_code == status.HTTP_403_FORBIDDEN


@pytest.mark.asyncio
async def test_create_quiz_with_1_question(
    client: TestClient,
    company_id: UUID,
    owner_token: str,
    prepare_database,
) -> None:
    response = client.post(
        f"company/{company_id}/quiz",
        headers={"Authorization": f"Bearer {owner_token}"},
        json=quiz_data_1_question,
    )

    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


@pytest.mark.asyncio
async def test_create_quiz_with_1_answer(
    client: TestClient,
    company_id: UUID,
    owner_token: str,
    prepare_database,
) -> None:
    response = client.post(
        f"company/{company_id}/quiz",
        headers={"Authorization": f"Bearer {owner_token}"},
        json=quiz_data_1_answer,
    )

    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


@pytest.mark.asyncio
async def test_admin_update_quiz(
    client: TestClient,
    company_id: UUID,
    quiz_id: UUID,
    token: str,
    prepare_database,
    fill_db_with_admins,
) -> None:
    response = client.patch(
        f"company/{company_id}/quiz/{quiz_id}",
        headers={"Authorization": f"Bearer {token}"},
        json=quiz_update_data,
    )

    assert response.status_code == status.HTTP_200_OK
    assert response.json()["name"] == quiz_update_data["name"]
    assert response.json()["description"] == quiz_update_data["description"]


@pytest.mark.asyncio
async def test_owner_update_quiz(
    client: TestClient,
    company_id: UUID,
    quiz_id: UUID,
    owner_token: str,
    prepare_database,
) -> None:
    response = client.patch(
        f"company/{company_id}/quiz/{quiz_id}",
        headers={"Authorization": f"Bearer {owner_token}"},
        json=quiz_update_data,
    )

    assert response.status_code == status.HTTP_200_OK
    assert response.json()["name"] == quiz_update_data["name"]
    assert response.json()["description"] == quiz_update_data["description"]


@pytest.mark.asyncio
async def test_member_update_quiz_forbidden(
    client: TestClient,
    company_id: UUID,
    quiz_id: UUID,
    token: str,
    prepare_database,
) -> None:
    response = client.patch(
        f"company/{company_id}/quiz/{quiz_id}",
        headers={"Authorization": f"Bearer {token}"},
        json=quiz_update_data,
    )

    assert response.status_code == status.HTTP_403_FORBIDDEN


@pytest.mark.asyncio
async def test_owner_delete_quiz(
    client: TestClient,
    company_id: UUID,
    quiz_id: UUID,
    owner_token: str,
    prepare_database,
) -> None:
    response = client.delete(
        f"company/{company_id}/quiz/{quiz_id}",
        headers={"Authorization": f"Bearer {owner_token}"},
    )

    assert response.status_code == status.HTTP_204_NO_CONTENT


@pytest.mark.asyncio
async def test_admin_delete_quiz(
    client: TestClient,
    company_id: UUID,
    quiz_id: UUID,
    token: str,
    prepare_database,
    fill_db_with_admins,
) -> None:
    response = client.delete(
        f"company/{company_id}/quiz/{quiz_id}",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == status.HTTP_204_NO_CONTENT


@pytest.mark.asyncio
async def test_user_delete_quiz_forbidden(
    client: TestClient,
    company_id: UUID,
    quiz_id: UUID,
    token: str,
    prepare_database,
) -> None:
    response = client.delete(
        f"company/{company_id}/quiz/{quiz_id}",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == status.HTTP_403_FORBIDDEN


@pytest.mark.asyncio
async def test_user_get_quiz_list(
    client: TestClient,
    company_id: UUID,
    token: str,
    prepare_database,
    fill_db_with_quizzes,
) -> None:
    response = client.get(
        f"company/{company_id}/quiz",
        headers={"Authorization": f"Bearer {token}"},
    )
    result = response.json()

    assert response.status_code == status.HTTP_200_OK
    assert result[0]["name"] == quiz_payload[0]["name"]
    assert result[1]["name"] == quiz_payload[1]["name"]
    assert result[2]["name"] == quiz_payload[2]["name"]
