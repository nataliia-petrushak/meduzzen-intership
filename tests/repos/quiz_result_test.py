from datetime import datetime
from uuid import UUID

import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from tests.constants import quiz_result_repo


@pytest.mark.asyncio
async def test_get_results_records(
    db: AsyncSession, user_id: UUID, fill_db_with_results
) -> None:
    result = await quiz_result_repo.get_results_records(
        db=db, filters={"user_id": user_id}
    )
    assert len(result) == 6
    assert result[0]["date"] == datetime(2024, 2, 2, 2, 2, 2).isoformat()
    assert result[1]["num_corr_answers"] == 2


@pytest.mark.asyncio
async def test_get_overdue_quiz_results(db: AsyncSession, fill_db_with_results) -> None:
    result = await quiz_result_repo.get_overdue_quiz_results(db=db)
    assert len(result) == 6
