from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions import OwnerRequestError, AssignError
from app.db.alembic.repos.company_repo import CompanyRepository
from app.db.alembic.repos.request_repo import RequestRepository
from app.db.models import RequestType
from app.dependencies import check_permissions
from app.schemas.request import GetRequest
from app.schemas.users import GetUser


class CompanyRequestService:
    def __init__(self):
        self._request_repo = RequestRepository()
        self._company_repo = CompanyRepository()

    async def create_company_invitation(
        self,
        db: AsyncSession,
        user_id: UUID,
        company_id: UUID,
        user: GetUser,
    ) -> GetRequest:
        company = await self._company_repo.get_model_by(
            db=db, filters={"id": company_id}
        )
        check_permissions(user_id=company.owner_id, user=user)
        if user_id == company.owner_id:
            raise OwnerRequestError()
        model_data = {
            "company_id": company_id,
            "user_id": user_id,
            "request_type": "invitation",
        }
        return await self._request_repo.create_model(db=db, model_data=model_data)

    async def company_cancel_request(
        self, db: AsyncSession, model_id: UUID, company_id: UUID, user: GetUser
    ) -> None:
        company = await self._company_repo.get_model_by(
            db=db, filters={"id": company_id}
        )
        check_permissions(user_id=company.owner_id, user=user)
        await self._request_repo.delete_model(db=db, model_id=model_id)

    async def company_accept_join_request(
        self, db: AsyncSession, join_request_id: UUID, user: GetUser, company_id: UUID
    ) -> GetRequest:
        company = await self._company_repo.get_model_by(
            db=db, filters={"id": company_id}
        )
        check_permissions(user_id=company.owner_id, user=user)
        return await self._request_repo.update_model(
            db=db, model_id=join_request_id, model_data={"request_type": "member"}
        )

    async def get_company_requests(
        self,
        db: AsyncSession,
        company_id: UUID,
        user: GetUser,
        offset: int = 0,
        limit: int = 10,
        request_type: str = "invitation",
    ) -> list[GetUser]:
        company = await self._company_repo.get_model_by(
            db=db, filters={"id": company_id}
        )
        check_permissions(user_id=company.owner_id, user=user)
        return await self._request_repo.request_list(
            db=db,
            offset=offset,
            limit=limit,
            company_id=company_id,
            request_type=request_type,
        )

    async def get_company_members(
        self,
        db: AsyncSession,
        company_id: UUID,
        offset: int = 0,
        limit: int = 10,
    ) -> list[GetUser]:
        return await self._request_repo.request_list(
            db=db,
            company_id=company_id,
            request_type="member",
            offset=offset,
            limit=limit,
        )

    async def company_delete_user(
        self, db: AsyncSession, user_id: UUID, company_id: UUID, user: GetUser
    ) -> None:
        company = await self._company_repo.get_model_by(
            db=db, filters={"id": company_id}
        )
        check_permissions(user_id=company.owner_id, user=user)
        invitation = await self._request_repo.get_model_by(
            db=db, filters={"user_id": user_id, "company_id": company_id}
        )
        await db.delete(invitation)
        await db.commit()

    async def company_change_member_role(
            self,
            db: AsyncSession,
            company_id: UUID,
            user_id: UUID,
            user: GetUser,
            request_type: RequestType,
    ) -> GetRequest:
        company = await self._company_repo.get_model_by(
            db=db, filters={"id": company_id}
        )
        check_permissions(user_id=company.owner_id, user=user)
        request = await self._request_repo.get_model_by(
            db=db, filters={"user_id": user_id, "company_id": company_id}
        )
        if request.request_type in [RequestType.join_request, RequestType.invitation]:
            raise AssignError(identifier=request.user_id)
        if request_type in [RequestType.invitation, RequestType.join_request]:
            raise AssignError(identifier=user_id)

        return await self._request_repo.update_model(
            db=db, model_id=request.id, model_data={"request_type": request_type}
        )

    async def company_admin_list(
            self,
            db: AsyncSession,
            company_id: UUID,
            offset: int = 0,
            limit: int = 10,
    ) -> list[GetUser]:
        return await self._request_repo.request_list(
            db=db, company_id=company_id, request_type="admin", offset=offset, limit=limit
        )
