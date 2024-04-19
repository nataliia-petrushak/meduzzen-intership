from uuid import UUID

import pytest
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models import User
from tests.conftest import AsyncSessionLocal
from tests.constants import pydentic_update_data, pydentic_create_data, user_repo


@pytest.fixture
async def db() -> AsyncSession:
    async with AsyncSessionLocal() as session:
        yield session


@pytest.fixture
def pydentic_create_data():
    return UserSignUp(username="Afanasiy", email="email@email.com", password="1234567")


@pytest.fixture
def pydentic_update_data():
    return UserUpdate(username="Bruno", email="email@bruno.com", password="<PASSWORD>")


@pytest.mark.asyncio(scope="function")
async def test_add_user_func(
    pydentic_create_data: UserSignUp, user_repo: UserRepository, db: AsyncSession
) -> None:
    result = await user_repo.create_model(db=db, model_data=pydentic_create_data)

    assert result["username"] == pydentic_create_data.username
    assert result["email"] == pydentic_create_data.email


@pytest.mark.asyncio(scope="function")
async def test_get_user_list_func(db: AsyncSession, user_repo: UserRepository):
    await user_repo.create_model(
        db=db,
        model_data=UserSignUp(username="Test", email="user1@user.com", password="123"),
    )
    await user_repo.create_model(
        db=db,
        model_data=UserSignUp(username="Test1", email="user2@user.com", password="123"),
    )
    await user_repo.create_model(
        db=db,
        model_data=UserSignUp(username="Test2", email="user3@user.com", password="123"),
    )

    result = await user_repo.get_model_list(db=db, limit=10, offset=0)

    assert len(result) == 4
    assert result[1].username == "Test"
    assert result[2].username == "Test1"
    assert result[3].username == "Test2"


@pytest.mark.asyncio(scope="function")
async def test_get_user_by_id_func(db: AsyncSession, user_repo: UserRepository):
    user = await user_repo.get_model_list(db=db, limit=1, offset=0)
    user_id = user[0].id
    result = await user_repo.get_model_by_id(db=db, model_id=user_id)

    assert result.id == user_id
    assert result.username == user[0].username
    assert result.email == user[0].email


@pytest.mark.asyncio(scope="function")
async def test_update_user(
    pydentic_update_data: UserUpdate, db: AsyncSession, user_repo: UserRepository
):
    user = await user_repo.get_model_list(db=db, limit=1, offset=0)
    user_id = user[0].id
    result = await user_repo.update_model(
        db=db, model_id=user_id, model_data=pydentic_update_data
    )

    assert result.id == user_id
    assert result.username == pydentic_update_data.username
    assert result.email == pydentic_update_data.email


@pytest.mark.asyncio(scope="function")
async def test_delete_user(db: AsyncSession, user_repo: UserRepository):
    user = await user_repo.get_model_list(db=db, limit=1, offset=0)
    user_id = user[0].id
    await user_repo.delete_model(db=db, model_id=user_id)

    result = await user_repo.get_model_list(db=db, limit=10, offset=0)

    assert user not in result
