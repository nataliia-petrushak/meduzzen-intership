from uuid import UUID

import sqlalchemy
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions import OwnerRequestError, IntegrityError, NoResultsError
from app.db.alembic.repos.company_repo import CompanyRepository
from app.db.alembic.repos.request_repo import RequestRepository
from app.permissions import check_permissions
from app.schemas.request import GetRequest, CompanyRequest
from app.schemas.users import GetUser


class UserRequestService:
    def __init__(self):
        self._request_repo = RequestRepository()
        self._company_repo = CompanyRepository()

    async def user_accept_invitation(
        self,
        db: AsyncSession,
        model_id: UUID,
        user: GetUser,
        user_id: UUID,
    ) -> GetRequest:
        check_permissions(user_id=user_id, user=user)
        return await self._request_repo.update_model(
            db=db, model_id=model_id, model_data={"request_type": "member"}
        )

    async def user_send_join_request(
        self, db: AsyncSession, user: GetUser, company_id: UUID
    ) -> GetRequest:
        company = await self._company_repo.get_model_by(
            db=db, filters={"id": company_id}
        )
        if user.id == company.owner_id:
            raise OwnerRequestError()
        model_data = {
            "user_id": user.id,
            "company_id": company_id,
            "request_type": "join_request",
        }
        try:
            return await self._request_repo.create_model(db=db, model_data=model_data)
        except sqlalchemy.exc.IntegrityError:
            raise IntegrityError(company_id=company_id, user_id=user.id)

    async def user_cancel_request(
        self, db: AsyncSession, user: GetUser, user_id: UUID, request_id: UUID
    ) -> None:
        check_permissions(user_id=user_id, user=user)
        return await self._request_repo.delete_model(db=db, model_id=request_id)

    async def get_user_requests(
        self,
        db: AsyncSession,
        user: GetUser,
        limit: int = 10,
        offset: int = 0,
        request_type: str = "invitation",
    ) -> list[CompanyRequest]:
        requests = await self._request_repo.get_model_list(
            db=db,
            limit=limit,
            offset=offset,
            filters={"user_id": user.id, "request_type": request_type},
        )
        if not requests:
            raise NoResultsError()
        return requests

    async def user_leave_company(
        self, db: AsyncSession, user: GetUser, company_id: UUID
    ) -> None:
        request = await self._request_repo.get_model_by(
            db=db, filters={"user_id": user.id, "company_id": company_id}
        )
        await db.delete(request)
        await db.commit()
