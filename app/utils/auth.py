from fastapi import Depends, Security
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions import UserNotFound
from app.dependencies import get_db
from app.schemas.users import GetUser, UserSignUp
from app.services.user import UserService
from app.utils.auth_bearer import auth_bearer


async def get_authenticated_user(
    db: AsyncSession = Depends(get_db),
    user_service: UserService = Depends(UserService),
    payload: dict = Security(auth_bearer),
) -> GetUser:
    user_email = payload["email"]
    username = user_email.split("@")[0]

    try:
        user = await user_service.get_user_by_email(db=db, email=user_email)
    except UserNotFound:
        user = await user_service.create_model(
            db=db,
            model_data=UserSignUp(
                email=user_email, username=username, password=username
            ),
        )
    return user
