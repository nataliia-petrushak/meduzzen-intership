from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions import NameExistError
from app.db.alembic.repos.company_repo import CompanyRepository
from app.db.models import Company
from app.dependencies import check_permissions
from app.schemas.company import CompanyCreate, CompanyUpdate
from app.schemas.users import GetUser


class CompanyService:
    def __init__(self):
        self._company_repo = CompanyRepository()

    async def create_model(
        self, db: AsyncSession, model_data: CompanyCreate, user: GetUser
    ) -> Company:
        company = self._company_repo.get_model_by(db=db, filter_={"name": model_data["name"]})
        if company:
            raise NameExistError(model_name="company", name=model_data["name"])
        model_data = model_data.model_dump()
        model_data["owner_id"] = user.id
        return await self._company_repo.create_model(db=db, model_data=model_data)

    async def update_model(
        self, db: AsyncSession, model_id: UUID, model_data: CompanyUpdate, user: GetUser
    ) -> Company:
        company = await self._company_repo.get_model_by(db=db, filter_={"id": model_id})
        check_permissions(user_id=company.owner_id, user=user)
        model_data = model_data.model_dump(exclude_unset=True)
        return await self._company_repo.update_model(
            db=db, model_id=model_id, model_data=model_data
        )

    async def get_model_list(
        self, db: AsyncSession, offset: int = 0, limit: int = 10
    ) -> list[Company]:
        return await self._company_repo.get_model_list(
            db=db, offset=offset, limit=limit, filters={"is_hidden": False}
        )

    async def get_model_by_id(self, db: AsyncSession, model_id: UUID) -> Company:
        return await self._company_repo.get_model_by(db=db, filter_={"id": model_id})

    async def delete_model(
        self, db: AsyncSession, model_id: UUID, user: GetUser
    ) -> None:
        company = await self._company_repo.get_model_by(db=db, filter_={"id": model_id})
        check_permissions(user_id=company.owner_id, user=user)
        await self._company_repo.delete_model(db=db, model_id=model_id)
