from uuid import UUID

import pytest
from starlette import status
from starlette.testclient import TestClient

from tests.constants import answers


@pytest.mark.asyncio
async def test_member_get_result(
    client: TestClient,
    quiz_id: UUID,
    token: str,
    prepare_database,
    fill_db_with_members,
) -> None:
    response = client.post(
        f"result/{quiz_id}",
        headers={"Authorization": f"Bearer {token}"},
        json=answers,
    )
    result = response.json()

    assert response.status_code == status.HTTP_200_OK
    assert result["all_results"][-1]["num_corr_answers"] == 2
    assert result["all_results"][-1]["questions_count"] == 3
    assert "date" in result["all_results"][-1]
    assert result["quiz_id"] == str(quiz_id)
    assert "user_id" in result
    assert "company_id" in result


@pytest.mark.asyncio
async def test_result_updated_if_it_already_exists(
    client: TestClient,
    quiz_id: UUID,
    token: str,
    prepare_database,
    fill_db_with_members,
    fill_db_with_results,
) -> None:
    response = client.post(
        f"result/{quiz_id}",
        headers={"Authorization": f"Bearer {token}"},
        json=answers,
    )
    result = response.json()

    assert response.status_code == status.HTTP_200_OK
    assert len(result["all_results"]) == 2
    assert result["all_results"][0]["num_corr_answers"] == 1
    assert result["all_results"][1]["num_corr_answers"] == 2


@pytest.mark.asyncio
async def test_not_member_get_result_forbidden(
    client: TestClient,
    quiz_id: UUID,
    token: str,
    prepare_database,
) -> None:
    response = client.post(
        f"result/{quiz_id}",
        headers={"Authorization": f"Bearer {token}"},
        json=answers,
    )
    assert response.status_code == status.HTTP_403_FORBIDDEN


@pytest.mark.asyncio
async def test_user_get_total_rating(
    client: TestClient, token: str, fill_db_with_results, fill_database
) -> None:
    response = client.get(
        "result/me/total_rating",
        headers={"Authorization": f"Bearer {token}"},
    )
    result = response.json()

    assert response.status_code == status.HTTP_200_OK
    assert result["rating"] == round(
        sum([1, 2, 1, 2, 1, 2]) / sum([3, 5, 3, 5, 3, 5]), 3
    )


@pytest.mark.asyncio
async def test_user_get_company_rating(
    client: TestClient,
    company_id: UUID,
    token: str,
    fill_db_with_results,
    fill_database
) -> None:
    response = client.get(
        f"result/me/company/{company_id}",
        headers={"Authorization": f"Bearer {token}"},
    )
    result = response.json()

    assert response.status_code == status.HTTP_200_OK
    assert result["rating"] == round(
        sum([1, 2, 1, 2, 1, 2]) / sum([3, 5, 3, 5, 3, 5]), 3
    )


@pytest.mark.asyncio
async def test_user_get_total_rating_without_results(
    client: TestClient,
    company_id: UUID,
    token: str,
    fill_database
) -> None:
    response = client.get(
        f"result/me/company/{company_id}",
        headers={"Authorization": f"Bearer {token}"},
    )
    result = response.json()

    assert response.status_code == status.HTTP_200_OK
    assert result["rating"] is None


@pytest.mark.asyncio
async def test_user_get_cached_results(
    client: TestClient,
    token: str,
    fill_db_with_results,
    fill_database
) -> None:
    response = client.get(
        "result/me/cached_results",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == status.HTTP_200_OK


@pytest.mark.asyncio
async def test_owner_get_company_cached_results(
    client: TestClient,
    owner_id: UUID,
    company_id: UUID,
    owner_token: str,
    fill_db_with_results,
) -> None:
    response = client.get(
        f"result/{company_id}/cache",
        headers={"Authorization": f"Bearer {owner_token}"},
    )
    assert response.status_code == status.HTTP_200_OK


@pytest.mark.asyncio
async def test_user_get_company_cached_results_forbidden(
    client: TestClient,
    user_id: UUID,
    company_id: UUID,
    token: str,
    fill_db_with_results,
) -> None:
    response = client.get(
        f"result/{company_id}/cache",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == status.HTTP_403_FORBIDDEN
