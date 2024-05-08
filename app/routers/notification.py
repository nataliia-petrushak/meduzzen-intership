from uuid import UUID

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from app.db.database import get_db
from app.db.models import NotificationStatus
from app.schemas.notification import GetNotification
from app.schemas.users import GetUser
from app.services.auth import get_authenticated_user
from app.services.notification import NotificationService

router = APIRouter(tags=["notification"], prefix="/notification")


@router.get("/{user_id}", response_model=list[GetNotification], status_code=status.HTTP_200_OK)
async def get_notification_list(
        user_id: UUID,
        db: AsyncSession = Depends(get_db),
        user: GetUser = Depends(get_authenticated_user),
        notification_service: NotificationService = Depends(NotificationService),
        limit: int = 10,
        offset: int = 0
) -> list[GetNotification]:
    return await notification_service.user_get_notification_list(
        user_id=user_id,
        user=user,
        db=db,
        limit=limit,
        offset=offset
    )


@router.post(
    "/{user_id}/notification/{notification_id}",
    response_model=GetNotification,
    status_code=status.HTTP_200_OK
)
async def change_notification_status(
        user_id: UUID,
        notification_id: UUID,
        status: NotificationStatus,
        user: GetUser = Depends(get_authenticated_user),
        notification_service: NotificationService = Depends(NotificationService),
        db: AsyncSession = Depends(get_db),
) -> GetNotification:
    return await notification_service.change_notification_status(
        user_id=user_id,
        notification_id=notification_id,
        status=status,
        user=user,
        db=db
    )
