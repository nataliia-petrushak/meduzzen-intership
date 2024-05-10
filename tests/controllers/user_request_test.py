from uuid import UUID

import pytest
from starlette import status
from starlette.testclient import TestClient

from tests.constants import company_payload


@pytest.mark.asyncio
async def test_user_create_join_request(
    client: TestClient,
    token: str,
    user_id: UUID,
    company_id: UUID,
    prepare_database,
) -> None:
    response = client.post(
        f"user/{user_id}/join-requests/{company_id}",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == status.HTTP_201_CREATED
    assert response.json()["request_type"] == "join_request"
    assert response.json()["user_id"] == str(user_id)
    assert response.json()["company_id"] == str(company_id)


async def test_unauthorized_user_create_request_forbidden(
    client: TestClient,
    user_id: UUID,
    company_id: UUID,
    prepare_database,
) -> None:
    response = client.post(
        f"user/{user_id}/join-requests/{company_id}",
    )

    assert response.status_code == status.HTTP_403_FORBIDDEN


@pytest.mark.asyncio
async def test_user_cancel_join_request(
    client: TestClient,
    token: str,
    request_id: UUID,
    user_id: UUID,
    prepare_database,
) -> None:
    response = client.delete(
        f"user/{user_id}/join-requests/{request_id}",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == status.HTTP_204_NO_CONTENT


@pytest.mark.asyncio
async def test_unauthorized_user_cancel_request_forbidden(
    client: TestClient,
    request_id: UUID,
    user_id: UUID,
    prepare_database,
) -> None:
    response = client.delete(f"user/{user_id}/join-requests/{request_id}")

    assert response.status_code == status.HTTP_403_FORBIDDEN


@pytest.mark.asyncio
async def test_user_accept_invitation(
    client: TestClient,
    user_id: UUID,
    invitation_id: UUID,
    token: str,
    prepare_database,
) -> None:
    response = client.patch(
        f"user/{user_id}/invitations/{invitation_id}",
        headers={"Authorization": f"Bearer {token}"},
    )
    result = response.json()

    assert response.status_code == status.HTTP_200_OK
    assert result["request_type"] == "member"
    assert result["user_id"] == str(user_id)
    assert result["id"] == str(invitation_id)


@pytest.mark.asyncio
async def test_user_decline_invitation(
    client: TestClient,
    user_id: UUID,
    invitation_id: UUID,
    token: str,
    prepare_database,
) -> None:
    response = client.delete(
        f"user/{user_id}/invitations/{invitation_id}",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == status.HTTP_204_NO_CONTENT


@pytest.mark.asyncio
async def test_user_get_invitation_list(
    client: TestClient,
    user_id: UUID,
    token: str,
    prepare_database,
    fill_db_with_invitations,
) -> None:
    response = client.get(
        f"user/{user_id}/invitations", headers={"Authorization": f"Bearer {token}"}
    )
    result = response.json()

    assert response.status_code == status.HTTP_200_OK
    assert result[0]["company"]["name"] == company_payload[0]["name"]
    assert result[1]["company"]["name"] == company_payload[1]["name"]


@pytest.mark.asyncio
async def test_user_get_request_list(
    client: TestClient,
    user_id: UUID,
    token: str,
    prepare_database,
    fill_db_with_join_requests,
) -> None:
    response = client.get(
        f"user/{user_id}/join-requests", headers={"Authorization": f"Bearer {token}"}
    )
    result = response.json()

    assert response.status_code == status.HTTP_200_OK
    assert result[0]["company"]["name"] == company_payload[0]["name"]


@pytest.mark.asyncio
async def test_user_leave_company(
    client: TestClient,
    member_id: UUID,
    company_id: UUID,
    token: str,
    prepare_database,
) -> None:
    response = client.delete(
        f"user/{member_id}/leave/{company_id}",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == status.HTTP_204_NO_CONTENT
