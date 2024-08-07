from uuid import UUID

import pytest
from starlette import status
from starlette.testclient import TestClient

from tests.constants import user_payload


@pytest.mark.asyncio
async def test_owner_create_company_invitation(
    client: TestClient,
    user_id: UUID,
    company_id: UUID,
    owner_token: str,
    prepare_database,
) -> None:
    response = client.post(
        f"company/{company_id}/invitation/{user_id}",
        headers={"Authorization": f"Bearer {owner_token}"},
    )

    assert response.status_code == status.HTTP_201_CREATED
    assert response.json()["request_type"] == "invitation"
    assert response.json()["user_id"] == str(user_id)
    assert response.json()["company_id"] == str(company_id)


@pytest.mark.asyncio
async def test_owners_invite_themself_forbidden(
    client: TestClient,
    owner_id: UUID,
    company_id: UUID,
    owner_token: str,
    prepare_database,
) -> None:
    response = client.post(
        f"company/{company_id}/invitation/{owner_id}",
        headers={"Authorization": f"Bearer {owner_token}"},
    )

    assert response.status_code == status.HTTP_403_FORBIDDEN


async def test_user_create_company_invitation_forbidden(
    client: TestClient,
    user_id: UUID,
    company_id: UUID,
    token: str,
    prepare_database,
) -> None:
    response = client.post(
        f"company/{company_id}/invitation/{user_id}",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == status.HTTP_403_FORBIDDEN


@pytest.mark.asyncio
async def test_owner_cancel_company_invitation(
    client: TestClient,
    invitation_id: UUID,
    company_id: UUID,
    owner_token: str,
    prepare_database,
) -> None:
    response = client.delete(
        f"company/{company_id}/invitation/{invitation_id}",
        headers={"Authorization": f"Bearer {owner_token}"},
    )

    assert response.status_code == status.HTTP_204_NO_CONTENT


@pytest.mark.asyncio
async def test_user_cancel_company_invitation_forbidden(
    client: TestClient,
    invitation_id: UUID,
    company_id: UUID,
    token: str,
    prepare_database,
) -> None:
    print(invitation_id)
    response = client.delete(
        f"company/{company_id}/invitation/{invitation_id}",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == status.HTTP_403_FORBIDDEN


@pytest.mark.asyncio
async def test_owner_accept_join_request(
    client: TestClient,
    company_id: UUID,
    request_id: UUID,
    owner_token: str,
    prepare_database,
) -> None:
    response = client.patch(
        f"company/{company_id}/join-request/{request_id}",
        headers={"Authorization": f"Bearer {owner_token}"},
    )
    result = response.json()

    assert response.status_code == status.HTTP_200_OK
    assert result["request_type"] == "member"
    assert result["company_id"] == str(company_id)
    assert result["id"] == str(request_id)


@pytest.mark.asyncio
async def test_user_accept_join_request_forbidden(
    client: TestClient,
    company_id: UUID,
    request_id: UUID,
    token: str,
    prepare_database,
) -> None:
    response = client.patch(
        f"company/{company_id}/join-request/{request_id}",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == status.HTTP_403_FORBIDDEN


@pytest.mark.asyncio
async def test_owner_decline_join_request(
    client: TestClient,
    company_id: UUID,
    request_id: UUID,
    owner_token: str,
    prepare_database,
) -> None:
    response = client.delete(
        f"company/{company_id}/join-request/{request_id}",
        headers={"Authorization": f"Bearer {owner_token}"},
    )

    assert response.status_code == status.HTTP_204_NO_CONTENT


@pytest.mark.asyncio
async def test_user_decline_join_request_forbidden(
    client: TestClient,
    company_id: UUID,
    request_id: UUID,
    token: str,
    prepare_database,
) -> None:
    response = client.delete(
        f"company/{company_id}/join-request/{request_id}",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == status.HTTP_403_FORBIDDEN


@pytest.mark.asyncio
async def test_get_company_member_list(
    client: TestClient, company_id: UUID, prepare_database, fill_db_with_members
) -> None:
    response = client.get(f"company/{company_id}/members")
    result = response.json()

    assert response.status_code == status.HTTP_200_OK
    assert result[1]["user"]["username"] == user_payload[1]["username"]
    assert result[2]["user"]["username"] == user_payload[2]["username"]
    assert result[3]["user"]["username"] == user_payload[3]["username"]


@pytest.mark.asyncio
async def test_owner_get_company_invitation_list(
    client: TestClient,
    company_id: UUID,
    owner_token: str,
    prepare_database,
    fill_db_with_invitations,
) -> None:
    response = client.get(
        f"company/{company_id}/invitations",
        headers={"Authorization": f"Bearer {owner_token}"},
    )
    result = response.json()

    assert response.status_code == status.HTTP_200_OK
    assert result[0]["user"]["username"] == user_payload[1]["username"]


@pytest.mark.asyncio
async def test_user_get_company_invitation_list_forbidden(
    client: TestClient,
    company_id: UUID,
    token: str,
    prepare_database,
    fill_db_with_invitations,
) -> None:
    response = client.get(
        f"company/{company_id}/invitations",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == status.HTTP_403_FORBIDDEN


@pytest.mark.asyncio
async def test_owner_get_company_request_list(
    client: TestClient,
    company_id: UUID,
    owner_token: str,
    prepare_database,
    fill_db_with_join_requests,
) -> None:
    response = client.get(
        f"company/{company_id}/join-requests",
        headers={"Authorization": f"Bearer {owner_token}"},
    )
    result = response.json()

    assert response.status_code == status.HTTP_200_OK
    assert result[1]["user"]["username"] == user_payload[1]["username"]
    assert result[2]["user"]["username"] == user_payload[2]["username"]


@pytest.mark.asyncio
async def test_user_get_company_request_list_forbidden(
    client: TestClient,
    company_id: UUID,
    token: str,
    prepare_database,
    fill_db_with_join_requests,
) -> None:
    response = client.get(
        f"company/{company_id}/join-requests",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == status.HTTP_403_FORBIDDEN


@pytest.mark.asyncio
async def test_owner_delete_member(
    client: TestClient,
    company_id: UUID,
    member_id: UUID,
    owner_token: str,
    prepare_database,
) -> None:
    response = client.delete(
        f"company/{company_id}/members/{member_id}",
        headers={"Authorization": f"Bearer {owner_token}"},
    )

    assert response.status_code == status.HTTP_204_NO_CONTENT


@pytest.mark.asyncio
async def test_user_delete_member_forbidden(
    client: TestClient,
    company_id: UUID,
    member_id: UUID,
    token: str,
    prepare_database,
) -> None:
    response = client.delete(
        f"company/{company_id}/members/{member_id}",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == status.HTTP_403_FORBIDDEN


@pytest.mark.asyncio
async def test_owner_assign_admin(
    client: TestClient,
    company_id: UUID,
    member_id: UUID,
    owner_token: str,
    prepare_database,
) -> None:
    response = client.patch(
        f"company/{company_id}/members/{member_id}",
        headers={"Authorization": f"Bearer {owner_token}"},
        params={"request_type": "admin"},
    )
    assert response.status_code == status.HTTP_200_OK
    assert response.json().get("request_type") == "admin"


@pytest.mark.asyncio
async def test_owner_assign_admin_as_member(
    client: TestClient,
    company_id: UUID,
    user_id: UUID,
    owner_token: str,
    prepare_database,
    fill_db_with_admins,
) -> None:
    response = client.patch(
        f"company/{company_id}/members/{user_id}",
        headers={"Authorization": f"Bearer {owner_token}"},
        params={"request_type": "member"},
    )
    assert response.status_code == status.HTTP_200_OK
    assert response.json().get("request_type") == "member"


@pytest.mark.asyncio
async def test_owner_assign_not_member_as_admin_forbidden(
    client: TestClient,
    company_id: UUID,
    user_id: UUID,
    owner_token: str,
    prepare_database,
    fill_db_with_invitations,
) -> None:
    response = client.patch(
        f"company/{company_id}/members/{user_id}",
        headers={"Authorization": f"Bearer {owner_token}"},
        params={"request_type": "admin"},
    )
    assert response.status_code == status.HTTP_403_FORBIDDEN


@pytest.mark.asyncio
async def test_user_assign_member_as_admin_forbidden(
    client: TestClient,
    company_id: UUID,
    user_id: UUID,
    token: str,
    prepare_database,
    fill_db_with_invitations,
) -> None:
    response = client.patch(
        f"company/{company_id}/members/{user_id}",
        headers={"Authorization": f"Bearer {token}"},
        params={"request_type": "admin"},
    )
    assert response.status_code == status.HTTP_403_FORBIDDEN


@pytest.mark.asyncio
async def test_owner_assign_member_other_roles_forbidden(
    client: TestClient,
    company_id: UUID,
    member_id: UUID,
    token: str,
    prepare_database,
) -> None:
    response = client.patch(
        f"company/{company_id}/members/{member_id}",
        headers={"Authorization": f"Bearer {token}"},
        params={"request_type": "invitation"},
    )
    assert response.status_code == status.HTTP_403_FORBIDDEN


@pytest.mark.asyncio
async def test_company_admin_list(
    client: TestClient, company_id: UUID, prepare_database, fill_db_with_admins
) -> None:
    response = client.get(f"company/{company_id}/admins")

    result = response.json()

    assert response.status_code == status.HTTP_200_OK
    assert len(result) == 5
    assert result[0]["user"]["username"] == user_payload[0]["username"]
    assert result[1]["user"]["username"] == user_payload[1]["username"]
    assert result[2]["user"]["username"] == user_payload[2]["username"]
