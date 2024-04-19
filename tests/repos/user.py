from uuid import UUID

import pytest
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models import User
from app.utils.common import UserNotFound
from tests.conftest import AsyncSessionLocal
from tests.constants import pydentic_update_data, pydentic_create_data, user_repo


@pytest.fixture
async def db() -> AsyncSession:
    async with AsyncSessionLocal() as session:
        yield session


@pytest.fixture
async def user_id(db: AsyncSession) -> UUID:
    user_id = await db.execute(select(User.id).limit(1))
    return user_id.scalars().one_or_none()


@pytest.mark.asyncio(scope="function")
async def test_add_user_func(db: AsyncSession) -> None:
    result = await user_repo.create_model(db=db, model_data=pydentic_create_data)

    assert result.username == pydentic_create_data.username
    assert result.email == pydentic_create_data.email


@pytest.mark.asyncio(scope="function")
async def test_get_user_list_func(db: AsyncSession):
    result = await user_repo.get_model_list(db=db, limit=10, offset=0)

    assert len(result) == 4
    assert result[0].username == "test_1"
    assert result[1].username == "test_2"
    assert result[2].username == "test_3"
    assert result[3].username == "Afanasiy"


@pytest.mark.asyncio(scope="function")
async def test_get_user_by_id_func(db: AsyncSession, user_id: UUID) -> None:
    with pytest.raises(UserNotFound):
        await user_repo.get_model_by_id(
            db=db, model_id="af3efcf6-9c61-4865-832f-5250f7fb8aec"
        )

    result = await user_repo.get_model_by_id(db=db, model_id=user_id)

    assert result.id == user_id
    assert result.username == "test_1"
    assert result.email == "test_1@test.com"


@pytest.mark.asyncio(scope="function")
async def test_update_user(db: AsyncSession, user_id):
    with pytest.raises(UserNotFound):
        await user_repo.update_model(
            db=db,
            model_id="af3efcf6-9c61-4865-832f-5250f7fb8aec",
            model_data=pydentic_update_data,
        )

    result = await user_repo.update_model(
        db=db, model_id=user_id, model_data=pydentic_update_data
    )

    assert result.id == user_id
    assert result.username == pydentic_update_data.username
    assert result.email == pydentic_update_data.email


@pytest.mark.asyncio(scope="function")
async def test_delete_user(db: AsyncSession, user_id):
    with pytest.raises(UserNotFound):
        await user_repo.delete_model(
            db=db, model_id="af3efcf6-9c61-4865-832f-5250f7fb8aec"
        )

    result = await db.execute(select(User, User.id).filter(User.id == user_id))
    user = result.scalar()

    assert user_id == user.id
