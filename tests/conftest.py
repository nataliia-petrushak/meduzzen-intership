from typing import AsyncGenerator

import httpx
import pytest
from httpx import AsyncClient
from sqlalchemy import NullPool
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from db.models import Base

from app.main import app
from dependencies import get_db
from config import settings

async_engine = create_async_engine(settings.test_postgres_url, poolclass=NullPool)
AsyncSessionLocal = sessionmaker(
    bind=async_engine,
    class_=AsyncSession,
    expire_on_commit=False,
)


@pytest.fixture(scope="function", autouse=True)
async def session_override():
    async def test_db() -> AsyncSession:
        async with AsyncSessionLocal() as db:
            yield db

    app.dependency_overrides[get_db] = test_db


@pytest.fixture(autouse=True, scope="session")
async def prepare_db():
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest.fixture(scope="session")
async def ac() -> AsyncGenerator[AsyncClient, None]:
    async with AsyncClient(transport=httpx.ASGITransport(app=app), base_url="http://test") as ac:
        yield ac
