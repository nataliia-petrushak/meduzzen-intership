from typing import AsyncGenerator
from uuid import UUID

import pytest
from sqlalchemy import NullPool, insert, select
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from fastapi.testclient import TestClient

from app.db.database import Base
from app.db.models import User, Company, Request
from app.main import app
from app.db.database import get_db
from app.config import settings
from app.services.security import SecurityService
from tests.constants import user_payload, company_payload

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
        await conn.execute(insert(User).values(user_payload))
        await conn.commit()


@pytest.fixture
async def user_id(db: AsyncSession, fill_database) -> UUID:
    user_id = await db.execute(select(User.id).filter(User.username == "test_1"))
    return user_id.scalars().one_or_none()


@pytest.fixture
async def owner_id(db: AsyncSession, fill_database) -> UUID:
    user_id = await db.execute(select(User.id).filter(User.username == "owner"))
    return user_id.scalars().one_or_none()


@pytest.fixture(scope="function")
async def fill_database_with_companies(owner_id: UUID):
    async with async_engine.begin() as conn:
        for company in company_payload:
            company["owner_id"] = owner_id
            await conn.execute(insert(Company).values(company))
        await conn.commit()


@pytest.fixture
async def company_id(db: AsyncSession, fill_database_with_companies) -> UUID:
    user_id = await db.execute(select(Company.id).filter(Company.name == "test_1"))
    return user_id.scalars().one_or_none()


@pytest.fixture(scope="function")
async def fill_db_with_invitations(user_id, fill_database_with_companies):
    async with async_engine.begin() as conn:
        companies = await conn.execute(select(Company))
        for company in companies:
            await conn.execute(
                insert(Request).values(
                    {
                        "user_id": user_id,
                        "company_id": company.id,
                        "request_type": "invitation",
                    }
                )
            )
        await conn.commit()


@pytest.fixture
async def invitation_id(db: AsyncSession, fill_db_with_invitations, company_id) -> UUID:
    invitation_id = await db.execute(
        select(Request.id).filter(Request.company_id == company_id)
    )
    return invitation_id.scalars().one_or_none()


@pytest.fixture(scope="function")
async def fill_db_with_join_requests(company_id, fill_database_with_companies):
    async with async_engine.begin() as conn:
        users = await conn.execute(select(User))
        for user in users:
            await conn.execute(
                insert(Request).values(
                    {
                        "user_id": user.id,
                        "company_id": company_id,
                        "request_type": "join_request",
                    }
                )
            )
        await conn.commit()


@pytest.fixture
async def request_id(db: AsyncSession, fill_db_with_join_requests, user_id) -> UUID:
    request_id = await db.execute(select(Request.id).filter(Request.user_id == user_id))
    return request_id.scalars().one_or_none()


@pytest.fixture(scope="function")
async def fill_db_with_members(company_id, fill_database_with_companies):
    async with async_engine.begin() as conn:
        users = await conn.execute(select(User))
        for user in users:
            await conn.execute(
                insert(Request).values(
                    {
                        "user_id": user.id,
                        "company_id": company_id,
                        "request_type": "member",
                    }
                )
            )
        await conn.commit()


@pytest.fixture
async def member_id(db: AsyncSession, fill_db_with_members, user_id) -> UUID:
    member_id = await db.execute(
        select(User.id)
        .join(Request, Request.user_id == User.id)
        .filter(Request.user_id == user_id)
    )
    return member_id.scalars().one_or_none()


@pytest.fixture
async def db(prepare_database) -> AsyncSession:
    async with AsyncSessionLocal() as session:
        yield session


@pytest.fixture
async def token(db: AsyncSession) -> str:
    user_email = "test_1@test.com"
    return SecurityService.encode_user_token(email=user_email)


@pytest.fixture
async def owner_token(db: AsyncSession) -> str:
    user_email = "owner@test.com"
    return SecurityService.encode_user_token(email=user_email)


@pytest.fixture(name="client", scope="session")
def client() -> TestClient:
    client = TestClient(app)
    yield client
