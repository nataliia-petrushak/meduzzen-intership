from uuid import UUID

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from app.db.database import get_db
from app.schemas.company import GetCompany
from app.schemas.request import GetRequest
from app.schemas.users import GetUser
from app.services.auth import get_authenticated_user
from app.services.user_request import UserRequestService

router = APIRouter(tags=["user_request"], prefix="/user")


@router.put(
    "/{user_id}/invitations/{invitation_id}",
    response_model=GetRequest,
    status_code=status.HTTP_200_OK
)
async def user_accept_invitation(
        user_id: UUID,
        invitation_id: UUID,
        db: AsyncSession = Depends(get_db),
        user: GetUser = Depends(get_authenticated_user),
        request_service: UserRequestService = Depends(UserRequestService)
) -> GetRequest:
    return await request_service.user_accept_invitation(
        db=db, user_id=user_id, user=user, model_id=invitation_id
    )


@router.delete(
    "/{user_id}/invitations/{invitation_id}",
    status_code=status.HTTP_204_NO_CONTENT
)
async def user_decline_invitation(
        user_id: UUID,
        invitation_id: UUID,
        db: AsyncSession = Depends(get_db),
        user: GetUser = Depends(get_authenticated_user),
        request_service: UserRequestService = Depends(UserRequestService)
) -> None:
    return await request_service.user_cancel_request(
        db=db, request_id=invitation_id, user_id=user_id, user=user
    )


@router.post(
    "/{user_id}/join-requests/{company_id}",
    response_model=GetRequest,
    status_code=status.HTTP_201_CREATED
)
async def user_send_join_request(
        user_id: UUID,
        company_id: UUID,
        user: GetUser = Depends(get_authenticated_user),
        db: AsyncSession = Depends(get_db),
        request_service: UserRequestService = Depends(UserRequestService)
) -> GetRequest:
    return await request_service.user_send_join_request(
        db=db, company_id=company_id, user_id=user_id, user=user
    )


@router.delete(
    "/{user_id}/join-requests/{join_request_id}",
    status_code=status.HTTP_204_NO_CONTENT
)
async def user_cancel_join_request(
        user_id: UUID,
        join_request_id: UUID,
        user: GetUser = Depends(get_authenticated_user),
        db: AsyncSession = Depends(get_db),
        request_service: UserRequestService = Depends(UserRequestService)
) -> None:
    return await request_service.user_cancel_request(
        db=db, request_id=join_request_id, user_id=user_id, user=user
    )


@router.get(
    "/{user_id}/invitations",
    response_model=list[GetCompany],
    status_code=status.HTTP_200_OK
)
async def user_invitation_list(
        user_id: UUID,
        db: AsyncSession = Depends(get_db),
        user: GetUser = Depends(get_authenticated_user),
        request_service: UserRequestService = Depends(UserRequestService),
        offset: int = 0,
        limit: int = 10,
) -> list[GetCompany]:
    return await request_service.get_user_requests(
        db=db, user_id=user_id, offset=offset, limit=limit, user=user
    )


@router.get(
    "/{user_id}/join-requests",
    response_model=list[GetCompany],
    status_code=status.HTTP_200_OK
)
async def user_join_request_list(
        user_id: UUID,
        db: AsyncSession = Depends(get_db),
        user: GetUser = Depends(get_authenticated_user),
        request_service: UserRequestService = Depends(UserRequestService),
        offset: int = 0,
        limit: int = 10,
) -> list[GetCompany]:
    return await request_service.get_user_requests(
        db=db, user_id=user_id, offset=offset, limit=limit, user=user, status="JOIN_REQUEST"
    )


@router.delete("/{user_id}/leave/{company_id}", status_code=status.HTTP_204_NO_CONTENT)
async def user_leave_request(
        user_id: UUID,
        company_id: UUID,
        user: GetUser = Depends(get_authenticated_user),
        db: AsyncSession = Depends(get_db),
        request_service: UserRequestService = Depends(UserRequestService)
) -> None:
    return await request_service.user_leave_company(
        db=db, user_id=user_id, company_id=company_id, user=user
    )
