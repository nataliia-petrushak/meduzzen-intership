from uuid import UUID

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from app.db.database import get_db
from app.schemas.request import GetRequest
from app.schemas.users import GetUser
from app.services.auth import get_authenticated_user
from app.services.company_request import CompanyRequestService

router = APIRouter(tags=["company_request"], prefix="/company")


@router.post(
    "/{company_id}/invitation/{user_id}",
    response_model=GetRequest,
    status_code=status.HTTP_201_CREATED,
)
async def create_company_invitation(
    company_id: UUID,
    user_id: UUID,
    user: GetUser = Depends(get_authenticated_user),
    db: AsyncSession = Depends(get_db),
    request_service: CompanyRequestService = Depends(CompanyRequestService),
) -> GetRequest:
    return await request_service.create_company_invitation(
        db=db, company_id=company_id, user=user, user_id=user_id
    )


@router.delete(
    "/{company_id}/invitation/{invitation_id}", status_code=status.HTTP_204_NO_CONTENT
)
async def company_cancel_invitation(
    company_id: UUID,
    invitation_id: UUID,
    user: GetUser = Depends(get_authenticated_user),
    request_service: CompanyRequestService = Depends(CompanyRequestService),
    db: AsyncSession = Depends(get_db),
) -> None:
    return await request_service.company_cancel_request(
        db=db,
        model_id=invitation_id,
        company_id=company_id,
        user=user,
    )


@router.patch(
    "/{company_id}/join-request/{join_request_id}",
    response_model=GetRequest,
    status_code=status.HTTP_200_OK,
)
async def company_accept_join_request(
    company_id: UUID,
    join_request_id: UUID,
    user: GetUser = Depends(get_authenticated_user),
    request_service: CompanyRequestService = Depends(CompanyRequestService),
    db: AsyncSession = Depends(get_db),
) -> GetRequest:
    return await request_service.company_accept_join_request(
        db=db, company_id=company_id, join_request_id=join_request_id, user=user
    )


@router.delete(
    "/{company_id}/join-request/{join_request_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def company_decline_join_request(
    company_id: UUID,
    join_request_id: UUID,
    user: GetUser = Depends(get_authenticated_user),
    request_service: CompanyRequestService = Depends(CompanyRequestService),
    db: AsyncSession = Depends(get_db),
) -> None:
    return await request_service.company_cancel_request(
        db=db, company_id=company_id, model_id=join_request_id, user=user
    )


@router.get(
    "/{company_id}/members",
    response_model=list[GetUser],
    status_code=status.HTTP_200_OK,
)
async def company_member_list(
    company_id: UUID,
    request_service: CompanyRequestService = Depends(CompanyRequestService),
    db: AsyncSession = Depends(get_db),
    limit: int = 10,
    offset: int = 0,
) -> list[GetUser]:
    return await request_service.get_company_members(
        db=db, company_id=company_id, limit=limit, offset=offset
    )


@router.get(
    "/{company_id}/invitations",
    response_model=list[GetUser],
    status_code=status.HTTP_200_OK,
)
async def company_invitation_list(
    company_id: UUID,
    db: AsyncSession = Depends(get_db),
    user: GetUser = Depends(get_authenticated_user),
    request_service: CompanyRequestService = Depends(CompanyRequestService),
    offset: int = 0,
    limit: int = 10,
) -> list[GetUser]:
    return await request_service.get_company_requests(
        db=db, company_id=company_id, user=user, offset=offset, limit=limit
    )


@router.get(
    "/{company_id}/join-requests",
    response_model=list[GetUser],
    status_code=status.HTTP_200_OK,
)
async def company_join_request_list(
    company_id: UUID,
    db: AsyncSession = Depends(get_db),
    user: GetUser = Depends(get_authenticated_user),
    request_service: CompanyRequestService = Depends(CompanyRequestService),
    offset: int = 0,
    limit: int = 10,
) -> list[GetUser]:
    return await request_service.get_company_requests(
        db=db,
        company_id=company_id,
        user=user,
        request_type="join_request",
        offset=offset,
        limit=limit,
    )


@router.delete(
    "/{company_id}/members/{user_id}", status_code=status.HTTP_204_NO_CONTENT
)
async def company_delete_member(
    company_id: UUID,
    user_id: UUID,
    db: AsyncSession = Depends(get_db),
    user: GetUser = Depends(get_authenticated_user),
    request_service: CompanyRequestService = Depends(CompanyRequestService),
) -> None:
    return await request_service.company_delete_user(
        db=db, company_id=company_id, user_id=user_id, user=user
    )


@router.patch(
    "/{company_id}/members/{user_id}", status_code=status.HTTP_200_OK
)
async def company_assign_member_as_admin(
        company_id: UUID,
        user_id: UUID,
        user: GetUser = Depends(get_authenticated_user),
        db: AsyncSession = Depends(get_db),
        request_service: CompanyRequestService = Depends(CompanyRequestService)
) -> GetRequest:
    return await request_service.company_change_member_role(
        db=db, company_id=company_id, user_id=user_id, user=user
    )


@router.get("/{company_id}/admins", response_model=list[GetUser], status_code=status.HTTP_200_OK)
async def company_get_admin_list(
        company_id: UUID,
        db: AsyncSession = Depends(get_db),
        request_service: CompanyRequestService = Depends(CompanyRequestService),
        offset: int = 0,
        limit: int = 10,
) -> list[GetUser]:
    return await request_service.company_admin_list(
        db=db, company_id=company_id, offset=offset, limit=limit
    )
