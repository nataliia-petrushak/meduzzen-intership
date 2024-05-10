from uuid import UUID

import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions import ObjectNotFound
from tests.constants import company_repo, company_data, company_update_data


@pytest.mark.asyncio
async def test_add_company_func(db: AsyncSession, user_id: UUID) -> None:
    company_data["owner_id"] = user_id
    result = await company_repo.create_model(db=db, model_data=company_data)

    assert result.name == company_data["name"]
    assert result.is_hidden == company_data["is_hidden"]


@pytest.mark.asyncio
async def test_get_company_list_func(
    db: AsyncSession, fill_database_with_companies
) -> None:
    result = await company_repo.get_model_list(db=db, limit=10, offset=0)

    assert len(result) == 3
    assert result[0].name == "test_1"
    assert result[1].name == "test_2"
    assert result[2].name == "test_3"


@pytest.mark.asyncio
async def test_get_company_by_id_func(
    db: AsyncSession, company_id: UUID, fill_database_with_companies
) -> None:
    with pytest.raises(ObjectNotFound):
        await company_repo.get_model_by(
            db=db, filters={"id": "af3efcf6-9c61-4865-832f-5250f7fb8aec"}
        )

    result = await company_repo.get_model_by(db=db, filters={"id": company_id})

    assert result.id == company_id
    assert result.name == "test_1"


@pytest.mark.asyncio
async def test_update_company(
    db: AsyncSession, company_id: UUID, fill_database_with_companies
) -> None:
    with pytest.raises(ObjectNotFound):
        await company_repo.update_model(
            db=db,
            model_id="af3efcf6-9c61-4865-832f-5250f7fb8aec",
            model_data=company_update_data,
        )

    result = await company_repo.update_model(
        db=db, model_id=company_id, model_data=company_update_data
    )

    assert result.id == company_id
    assert result.name == company_update_data["name"]


@pytest.mark.asyncio
async def test_delete_company(
    db: AsyncSession, company_id: UUID, fill_database_with_companies
) -> None:
    with pytest.raises(ObjectNotFound):
        await company_repo.delete_model(
            db=db, model_id="af3efcf6-9c61-4865-832f-5250f7fb8aec"
        )

    result = await company_repo.delete_model(db=db, model_id=company_id)
    assert company_id == result.id
