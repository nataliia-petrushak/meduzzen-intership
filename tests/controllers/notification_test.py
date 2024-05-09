from uuid import UUID

import pytest
from starlette import status
from starlette.testclient import TestClient

from tests.constants import quiz_data


@pytest.mark.asyncio
async def test_get_notification_list(
    client: TestClient,
    user_id: UUID,
    token: str,
    prepare_database,
    fill_db_with_notifications,
) -> None:
    response = client.get(
        f"/notification/{user_id}",
        headers={"Authorization": f"Bearer {token}"},
    )
    result = response.json()

    assert response.status_code == status.HTTP_200_OK
    assert result[0]["notification_status"] == "unread"
    assert result[1]["message"] == "Hello World!"
    assert "quiz_id" in result[2]


@pytest.mark.asyncio
async def test_change_notification_status(
    client: TestClient,
    user_id: UUID,
    notification_id: UUID,
    token: str,
    prepare_database,
) -> None:
    response = client.patch(
        f"/notification/{user_id}/notification/{notification_id}",
        headers={"Authorization": f"Bearer {token}"},
        params={"notification_status": "read"},
    )
    result = response.json()

    assert response.status_code == status.HTTP_200_OK
    assert result["notification_status"] == "read"


@pytest.mark.asyncio
async def test_create_notification_when_quiz_created(
    client: TestClient, company_id: UUID, owner_token: str, member_id: UUID, token: str
) -> None:
    client.post(
        f"/company/{company_id}/quiz",
        headers={"Authorization": f"Bearer {owner_token}"},
        json=quiz_data,
    )
    response = client.get(
        f"/notification/{member_id}",
        headers={"Authorization": f"Bearer {token}"},
    )
    result = response.json()
    assert response.status_code == status.HTTP_200_OK
    assert result[0]["notification_status"] == "unread"
