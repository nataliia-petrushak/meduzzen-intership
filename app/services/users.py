from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models import UserBase
from app.db.repos.base_repo import BaseRepository
from app.schemas.users import UserSignUp, UserUpdate


class UserServices(BaseRepository):
    def __init__(self):
        super().__init__(UserBase)

    def create_model(self, db: AsyncSession, model_data: UserSignUp) -> UserBase:
        return super().create_model(db, model_data)

    def update_model(
        self, db: AsyncSession, model_id: UUID, model_data: UserUpdate
    ) -> UserBase:
        return super().update_model(db, model_id, model_data)


user_services = UserServices()
