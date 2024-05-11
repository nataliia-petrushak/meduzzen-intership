from uuid import UUID

import pytest
from starlette import status
from starlette.testclient import TestClient

from tests.constants import company_data, company_payload, company_update_data


@pytest.mark.asyncio
async def test_create_company(
    client: TestClient, owner_token: str, prepare_database
) -> None:
    response = client.post(
        "/companies",
        json=company_data,
        headers={"Authorization": f"Bearer {owner_token}"},
    )

    assert response.status_code == status.HTTP_201_CREATED
    assert response.json()["name"] == company_data["name"]
    assert response.json()["description"] == company_data["description"]
    assert response.json()["is_hidden"] == company_data["is_hidden"]


@pytest.mark.asyncio
async def test_can_not_create_company_unauthorized(
    client: TestClient, prepare_database
) -> None:
    response = client.post("/companies", json=company_data)

    assert response.status_code == status.HTTP_403_FORBIDDEN


@pytest.mark.asyncio
async def test_get_company_list(
    client: TestClient, prepare_database, fill_database_with_companies
) -> None:
    response = client.get("/companies")
    result = response.json()

    assert response.status_code == status.HTTP_200_OK
    assert result[0]["name"] == company_payload[0]["name"]
    assert result[1]["name"] == company_payload[1]["name"]
    assert result[2]["name"] == company_payload[2]["name"]


@pytest.mark.asyncio
async def test_get_company_by_id(
    client: TestClient, company_id: UUID, prepare_database, fill_database_with_companies
) -> None:
    response = client.get(f"/companies/{company_id}")
    result = response.json()

    assert response.status_code == status.HTTP_200_OK
    assert result["name"] == company_payload[0]["name"]

    response_2 = client.get("/companies/af3efcf6-9c61-4865-832f-5250f7fb8aec")
    assert response_2.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.asyncio
async def test_update_company_unauthorized(
    client: TestClient,
    company_id: UUID,
    prepare_database,
    fill_database_with_companies,
) -> None:
    response = client.patch(f"/companies/{company_id}", json=company_update_data)

    assert response.status_code == status.HTTP_403_FORBIDDEN


@pytest.mark.asyncio
async def test_update_company_authorized_forbidden(
    client: TestClient,
    company_id: UUID,
    owner_token: str,
    prepare_database,
    fill_database_with_companies,
) -> None:
    response = client.patch(
        f"/companies/{company_id}",
        json=company_update_data,
        headers={"Authorization": f"Bearer {owner_token}"},
    )
    result = response.json()

    assert response.status_code == status.HTTP_200_OK
    assert result["name"] == company_update_data["name"]
    assert result["is_hidden"] == company_update_data["is_hidden"]


@pytest.mark.asyncio
async def test_delete_company_unauthorized_forbidden(
    client: TestClient,
    company_id: UUID,
    prepare_database,
    fill_database_with_companies,
) -> None:
    response = client.delete(f"/companies/{company_id}")

    assert response.status_code == status.HTTP_403_FORBIDDEN


@pytest.mark.asyncio
async def test_delete_company_unauthorized(
    client: TestClient,
    company_id: UUID,
    owner_token: str,
    prepare_database,
    fill_database_with_companies,
) -> None:
    response = client.delete(
        f"/companies/{company_id}", headers={"Authorization": f"Bearer {owner_token}"}
    )

    assert response.status_code == status.HTTP_204_NO_CONTENT
