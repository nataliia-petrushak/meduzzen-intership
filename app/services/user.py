from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions import ObjectNotFound
from app.db.models import User
from app.dependencies import check_permissions
from app.schemas.users import UserSignUp, UserUpdate, GetUser
from app.services.security import SecurityService
from app.db.alembic.repos.user_repo import UserRepository


class UserService:
    def __init__(self):
        self._user_repo = UserRepository()

    async def create_model(self, db: AsyncSession, model_data: UserSignUp) -> User:
        try:
            user = await self._user_repo.get_user_by_email(
                db=db, email=model_data.email
            )
            user.is_active = True
            await db.commit()
        except ObjectNotFound:
            model_data.password = SecurityService.hash_password(model_data.password)
            model_data = model_data.model_dump(exclude_unset=True)
            user = await self._user_repo.create_model(db=db, model_data=model_data)
        return user

    async def update_model(
        self, db: AsyncSession, model_id: UUID, model_data: UserUpdate, user: GetUser
    ) -> User:
        check_permissions(user_id=model_id, user=user)
        if model_data.password:
            model_data.password = SecurityService.hash_password(model_data.password)
        model_data = model_data.model_dump(exclude_unset=True)
        result = await self._user_repo.update_model(
            db=db, model_id=model_id, model_data=model_data
        )
        return result

    async def get_model_list(
        self, db: AsyncSession, offset: int = 0, limit: int = 10
    ) -> list[User]:
        return await self._user_repo.get_model_list(
            db, offset, limit, filters={"is_active": True}
        )

    async def get_model_by_id(self, db: AsyncSession, model_id: UUID) -> User:
        return await self._user_repo.get_model_by_id(db, model_id=model_id)

    async def user_deactivate(
        self, db: AsyncSession, user_id: UUID, user: GetUser
    ) -> None:
        check_permissions(user_id=user_id, user=user)
        await self._user_repo.update_model(
            db=db, model_id=user_id, model_data={"is_active": False}
        )

    async def get_user_by_email(self, db: AsyncSession, email: str) -> User:
        return await self._user_repo.get_user_by_email(db=db, email=email)
