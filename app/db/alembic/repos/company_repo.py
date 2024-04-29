from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions import ObjectNotFound
from app.db.alembic.repos.base_repo import BaseRepository
from app.db.models import Company, User


class CompanyRepository(BaseRepository):
    def __init__(self):
        super().__init__(Company)

    async def get_model_by(self, db: AsyncSession, filter_: dict) -> Company:
        result = await db.execute(
            select(self.model, self.model.id)
            .join(User, Company.owner_id == User.id)
            .filter_by(**filter_)
        )
        model = result.scalar()
        identifier = list(filter_.keys())[0]

        if not model:
            raise ObjectNotFound(identifier=identifier, model_name=self.model.__name__)

        return model
