from uuid import UUID

import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions import ObjectNotFound
from tests.constants import pydentic_update_data, pydentic_create_data, user_repo


@pytest.mark.asyncio
async def test_add_user_func(db: AsyncSession) -> None:
    result = await user_repo.create_model(
        db=db, model_data=pydentic_create_data.model_dump()
    )

    assert result.username == pydentic_create_data.username
    assert result.email == pydentic_create_data.email


@pytest.mark.asyncio
async def test_get_user_list_func(db: AsyncSession, fill_database) -> None:
    result = await user_repo.get_model_list(db=db, limit=10, offset=0)

    assert len(result) == 5
    assert result[1].username == "test_1"
    assert result[2].username == "test_2"
    assert result[3].username == "test_3"


@pytest.mark.asyncio
async def test_get_user_by_id_func(
    db: AsyncSession, user_id: UUID, fill_database
) -> None:
    with pytest.raises(ObjectNotFound):
        await user_repo.get_model_by(
            db=db, filters={"id": "af3efcf6-9c61-4865-832f-5250f7fb8aec"}
        )

    result = await user_repo.get_model_by(db=db, filters={"id": user_id})

    assert result.id == user_id
    assert result.username == "test_1"
    assert result.email == "test_1@test.com"


@pytest.mark.asyncio
async def test_update_user(db: AsyncSession, user_id: UUID, fill_database) -> None:
    with pytest.raises(ObjectNotFound):
        await user_repo.update_model(
            db=db,
            model_id="af3efcf6-9c61-4865-832f-5250f7fb8aec",
            model_data=pydentic_update_data.model_dump(),
        )

    result = await user_repo.update_model(
        db=db, model_id=user_id, model_data=pydentic_update_data.model_dump()
    )

    assert result.id == user_id
    assert result.username == pydentic_update_data.username


@pytest.mark.asyncio
async def test_delete_user(db: AsyncSession, user_id: UUID, fill_database) -> None:
    with pytest.raises(ObjectNotFound):
        await user_repo.delete_model(
            db=db, model_id="af3efcf6-9c61-4865-832f-5250f7fb8aec"
        )

    result = await user_repo.delete_model(db=db, model_id=user_id)
    assert user_id == result.id
