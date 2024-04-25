from uuid import UUID

from app.core.exceptions import AccessDeniedError
from app.schemas.users import GetUser


async def check_permissions(user_id: UUID, user: GetUser) -> None:
    if user_id != user.id:
        raise AccessDeniedError()
