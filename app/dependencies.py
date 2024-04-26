from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.core.exceptions import AccessDeniedError
from app.db.models import User, Company
from app.schemas.users import GetUser


def check_permissions(user_id: UUID, user: GetUser) -> None:
    if user_id != user.id:
        raise AccessDeniedError()


async def check_company_owner(
    db: AsyncSession, company_id: UUID, user: GetUser
) -> None:
    result = await db.execute(
        select(Company.id)
        .join(User, Company.owner_id == User.id)
        .filter(Company.owner_id == user.id)
    )
    company = [company[0] for company in result.fetchall() if company[0] == company_id]
    if not company:
        raise AccessDeniedError()
