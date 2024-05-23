from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions import ObjectAlreadyExistError, ObjectNotFound
from app.db.alembic.repos.company_repo import CompanyRepository
from app.permissions import check_permissions
from app.schemas.company import CompanyCreate, CompanyUpdate, GetCompany, CompanyDetail
from app.schemas.users import GetUser


class CompanyService:
    def __init__(self):
        self._company_repo = CompanyRepository()

    async def create_model(
        self, db: AsyncSession, model_data: CompanyCreate, user: GetUser
    ) -> GetCompany:
        try:
            await self._company_repo.get_model_by(
                db=db, filters={"name": model_data.name}
            )
            raise ObjectAlreadyExistError(model_name="company", identifier=model_data.name)
        except ObjectNotFound:
            model_data = model_data.model_dump()
            model_data["owner_id"] = user.id
            return await self._company_repo.create_model(db=db, model_data=model_data)

    async def update_model(
        self, db: AsyncSession, model_id: UUID, model_data: CompanyUpdate, user: GetUser
    ) -> GetCompany:
        company = await self._company_repo.get_model_by(db=db, filters={"id": model_id})
        check_permissions(user_id=company.owner_id, user=user)
        model_data = model_data.model_dump(exclude_unset=True)
        return await self._company_repo.update_model(
            db=db, model_id=model_id, model_data=model_data
        )

    async def get_model_list(
        self, db: AsyncSession, offset: int = 0, limit: int = 10
    ) -> list[GetCompany]:
        return await self._company_repo.get_model_list(
            db=db, offset=offset, limit=limit, filters={"is_hidden": False}
        )

    async def get_model_by_id(self, db: AsyncSession, model_id: UUID) -> CompanyDetail:
        company = await self._company_repo.get_model_by(db=db, filters={"id": model_id})
        if company.is_hidden:
            raise ObjectNotFound(model_name="Company", identifier=model_id)
        return company

    async def delete_model(
        self, db: AsyncSession, model_id: UUID, user: GetUser
    ) -> None:
        company = await self._company_repo.get_model_by(db=db, filters={"id": model_id})
        check_permissions(user_id=company.owner_id, user=user)
        await self._company_repo.delete_model(db=db, model_id=model_id)
