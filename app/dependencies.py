from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.core.exceptions import AccessDeniedError
from app.db.models import User, Company
from app.schemas.users import GetUser


def check_permissions(user_id: UUID, user: GetUser) -> None:
    if user_id != user.id:
        raise AccessDeniedError()
