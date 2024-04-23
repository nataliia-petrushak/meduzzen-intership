import jwt
from fastapi import Security, Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions import AuthorizationError, UserNotFound
from app.dependencies import get_db
from app.schemas.users import GetUser, UserSignUp
from app.services.auth0 import Auth0Service
from app.services.security import SecurityService
from app.services.user import UserService

security = HTTPBearer()
user_service = UserService()


def jwt_authenticate(token: str) -> dict | None:
    try:
        return SecurityService.decode_user_token(token)
    except jwt.exceptions.InvalidAlgorithmError:
        return None


def auth0_authenticate(token: str) -> dict | None:
    try:
        return Auth0Service.verify(token)
    except AuthorizationError:
        return None


def authorize_user(token: HTTPAuthorizationCredentials = Security(security)):
    payload_1 = auth0_authenticate(token.credentials)
    payload_2 = jwt_authenticate(token.credentials)
    return payload_1 or payload_2


async def get_authenticated_user(
        db: AsyncSession = Depends(get_db),
        payload: dict = Depends(authorize_user)
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
