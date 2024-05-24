from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions import ObjectNotFound, ObjectAlreadyExistError, NoResultsError
from app.db.models import User
from app.schemas.users import UserSignUp, UserUpdate, GetUser
from app.services.security import SecurityService
from app.db.alembic.repos.user_repo import UserRepository


class UserService:
    def __init__(self):
        self._user_repo = UserRepository()

    async def create_model(self, db: AsyncSession, model_data: UserSignUp) -> User:
        try:
            await self._user_repo.get_model_by(
                db=db, filters={"email": model_data.email}
            )
            raise ObjectAlreadyExistError(model_name="User", identifier=model_data.email)
        except ObjectNotFound:
            model_data.password = SecurityService.hash_password(model_data.password)
            model_data = model_data.model_dump()
            user = await self._user_repo.create_model(db=db, model_data=model_data)
        return user

    async def update_model(
        self, db: AsyncSession, model_data: UserUpdate, user: GetUser
    ) -> User:
        if model_data.password:
            model_data.password = SecurityService.hash_password(model_data.password)
        model_data = model_data.model_dump(exclude_unset=True)
        result = await self._user_repo.update_model(
            db=db, model_id=user.id, model_data=model_data
        )
        return result

    async def get_model_list(
        self, db: AsyncSession, offset: int = 0, limit: int = 10
    ) -> list[User]:
        users = await self._user_repo.get_model_list(
            db, offset, limit, filters={"is_active": True}
        )
        if not users:
            raise NoResultsError()
        return users

    async def get_model_by_id(self, db: AsyncSession, model_id: UUID) -> User:
        return await self._user_repo.get_model_by(db=db, filters={"id": model_id})

    async def user_deactivate(
        self, db: AsyncSession, user: GetUser
    ) -> None:
        await self._user_repo.update_model(
            db=db, model_id=user.id, model_data={"is_active": False}
        )

    async def get_user_by_email(self, db: AsyncSession, email: str) -> User:
        return await self._user_repo.get_model_by(db=db, filters={"email": email})
