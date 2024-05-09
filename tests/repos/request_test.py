from uuid import UUID

import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from tests.constants import request_repo


@pytest.mark.asyncio
async def test_get_results_records_user_member(
    db: AsyncSession, member_id: UUID
) -> None:
    result = await request_repo.request_list(
        db=db, user_id=member_id, request_type="member"
    )

    assert len(result) == 1
    assert result[0].name == "test_1"
    assert result[0].description == ""


@pytest.mark.asyncio
async def test_get_results_records_company_members(
    db: AsyncSession, company_id: UUID, fill_db_with_members
) -> None:
    result = await request_repo.request_list(
        db=db, company_id=company_id, request_type="member"
    )

    assert len(result) == 5
    assert result[1].username == "test_1"


@pytest.mark.asyncio
async def test_get_results_records_company_admins(
    db: AsyncSession, company_id: UUID, fill_db_with_admins
) -> None:
    result = await request_repo.request_list(
        db=db, company_id=company_id, request_type="admin"
    )

    assert len(result) == 5
    assert result[1].username == "test_1"
