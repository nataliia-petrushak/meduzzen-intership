from uuid import UUID

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions import AccessDeniedError
from app.db.database import SessionLocal
from app.db.models import User
from app.services.auth import get_authenticated_user


async def check_permissions(user_id: UUID, user: User = Depends(get_authenticated_user)) -> User:
    if user_id != user.id:
        raise AccessDeniedError()
    return user
