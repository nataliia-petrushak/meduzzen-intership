import jwt
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Request, Depends, Security

from app.core.exceptions import AuthorizationError, UserNotFound
from app.dependencies import get_db
from app.schemas.auth import Token
from app.schemas.users import UserSignIn, UserSignUp, GetUser
from app.services.security import SecurityService, Auth0Service
from app.services.user import UserService


class AuthService:
    def __init__(self):
        self._user_service = UserService()

    async def sign_in(self, db: AsyncSession, user_data: UserSignIn) -> Token:
        user = await self._user_service.get_user_by_email(db=db, email=user_data.email)
        if user and SecurityService.verify_password(
            password=user_data.password, hashed_password=user.password
        ):
            access_token = SecurityService.encode_user_token(email=user.email)
            return Token(access_token=access_token, token_type="Bearer")
        raise AuthorizationError(detail="Incorrect credentials")


class AuthBearer(HTTPBearer):
    def __init__(self, auto_error: bool = True):
        super(AuthBearer, self).__init__(auto_error=auto_error)

    async def __call__(self, request: Request):
        credentials: HTTPAuthorizationCredentials = await super(
            AuthBearer, self
        ).__call__(request)
        if credentials:
            if not credentials.scheme == "Bearer":
                raise AuthorizationError(detail="Invalid authentication scheme.")
            if not self.authorize_user(credentials.credentials):
                raise AuthorizationError(detail="Invalid token or expired token.")
            return self.authorize_user(credentials.credentials)
        else:
            raise AuthorizationError(detail="Invalid authorization code.")

    @staticmethod
    def jwt_authenticate(credentials: str) -> dict | None:
        try:
            return SecurityService.decode_user_token(credentials)
        except (
            jwt.exceptions.InvalidAlgorithmError,
            jwt.exceptions.InvalidSignatureError,
        ):
            return None

    @staticmethod
    def auth0_authenticate(credentials: str) -> dict | None:
        try:
            return Auth0Service.verify(credentials)
        except AuthorizationError:
            return None

    def authorize_user(self, credentials: str) -> dict | None:
        payload_1 = self.auth0_authenticate(credentials)
        payload_2 = self.jwt_authenticate(credentials)
        return payload_1 or payload_2


async def get_authenticated_user(
    db: AsyncSession = Depends(get_db),
    user_service: UserService = Depends(UserService),
    payload: dict = Security(AuthBearer()),
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
