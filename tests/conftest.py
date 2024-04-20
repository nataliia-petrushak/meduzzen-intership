from typing import AsyncGenerator

import pytest
from sqlalchemy import NullPool, insert
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from starlette.testclient import TestClient

from app.db.database import Base
from app.db.models import User
from app.main import app
from app.dependencies import get_db
from app.config import settings
from tests.constants import payload

async_engine = create_async_engine(settings.test_postgres_url, poolclass=NullPool)
AsyncSessionLocal = sessionmaker(
    bind=async_engine,
    class_=AsyncSession,
    expire_on_commit=False,
)


async def override_get_db() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSessionLocal() as db:
        yield db


app.dependency_overrides[get_db] = override_get_db


@pytest.fixture(scope="function")
async def prepare_database():
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest.fixture(scope="function")
async def fill_database():
    async with async_engine.begin() as conn:
        await conn.execute(insert(User).values(payload))
        await conn.commit()


@pytest.fixture(name="client", scope="session")
def client() -> TestClient:
    client = TestClient(app)
    yield client
