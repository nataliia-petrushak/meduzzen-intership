from datetime import datetime
from uuid import UUID

import pytest
from starlette import status
from starlette.testclient import TestClient


@pytest.mark.asyncio
async def test_user_avg_score_dynamic(
    client: TestClient,
    token: str,
    prepare_database,
    fill_db_with_results,
    fill_database
) -> None:
    response = client.get(
        f"statistic/me/avg_score_dynamics",
        headers={"Authorization": f"Bearer {token}"},
    )
    result = response.json()

    assert response.status_code == status.HTTP_200_OK
    assert result[0]["date"] == datetime(2024, 2, 2, 2, 2, 2).isoformat()
    assert result[1]["date"] == datetime(2024, 3, 3, 3, 3, 3).isoformat()
    assert result[0]["score"] == round(1 / 3, 3)
    assert result[1]["score"] == round(3 / 8, 3)


@pytest.mark.asyncio
async def test_get_owner_company_all_users_avg_dynamic(
    client: TestClient,
    company_id: UUID,
    owner_token: str,
    prepare_database,
    fill_db_with_results,
) -> None:
    response = client.get(
        f"statistic/{company_id}/avg_score_dynamic",
        headers={"Authorization": f"Bearer {owner_token}"},
    )
    result = response.json()

    assert response.status_code == status.HTTP_200_OK
    assert result[0]["date"] == datetime(2024, 2, 2, 2, 2, 2).isoformat()
    assert result[1]["date"] == datetime(2024, 3, 3, 3, 3, 3).isoformat()
    assert result[0]["score"] == round(1 / 3, 3)
    assert result[1]["score"] == round(3 / 8, 3)


@pytest.mark.asyncio
async def test_get_user_all_company_users_avg_dynamic_forbidden(
    client: TestClient,
    company_id: UUID,
    token: str,
    prepare_database,
    fill_db_with_results,
) -> None:
    response = client.get(
        f"statistic/{company_id}/avg_score_dynamic",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == status.HTTP_403_FORBIDDEN


@pytest.mark.asyncio
async def test_get_quiz_last_comp_time(
    client: TestClient,
    token: str,
    prepare_database,
    fill_db_with_results,
    fill_database
) -> None:
    response = client.get(
        f"statistic/me/quizzes",
        headers={"Authorization": f"Bearer {token}"},
    )
    result = response.json()

    assert response.status_code == status.HTTP_200_OK
    assert "quiz_id" in result[0]
    assert result[0]["date"] == datetime(2024, 2, 2, 2, 2, 2).isoformat()
    assert result[1]["date"] == datetime(2024, 3, 3, 3, 3, 3).isoformat()


@pytest.mark.asyncio
async def test_owner_get_users_last_comp_time_for_quiz(
    client: TestClient,
    company_id: UUID,
    quiz_id: UUID,
    owner_token: str,
    prepare_database,
    fill_db_with_results,
) -> None:
    response = client.get(
        f"statistic/{company_id}/quiz/{quiz_id}/users",
        headers={"Authorization": f"Bearer {owner_token}"},
    )
    result = response.json()

    assert response.status_code == status.HTTP_200_OK
    assert "user_id" in result[0]
    assert result[0]["date"] == datetime(2024, 2, 2, 2, 2, 2).isoformat()
    assert result[1]["date"] == datetime(2024, 3, 3, 3, 3, 3).isoformat()


@pytest.mark.asyncio
async def test_user_get_users_last_comp_time_for_quiz_forbidden(
    client: TestClient,
    company_id: UUID,
    quiz_id: UUID,
    token: str,
    prepare_database,
    fill_db_with_results,
) -> None:
    response = client.get(
        f"statistic/{company_id}/quiz/{quiz_id}/users",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == status.HTTP_403_FORBIDDEN
