from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions import ObjectNotFound
from app.db.alembic.repos.base_repo import BaseRepository
from app.db.models import Company, User


class CompanyRepository(BaseRepository):
    def __init__(self):
        super().__init__(Company)

    async def get_model_by_id(self, db: AsyncSession, model_id: UUID) -> Company:
        result = await db.execute(
            select(self.model, self.model.id)
            .join(User, Company.owner_id == User.id)
            .filter(self.model.id == model_id)
        )
        model = result.scalar()

        if not model:
            raise ObjectNotFound(identifier=model_id, model_name=self.model.__name__)

        return model
