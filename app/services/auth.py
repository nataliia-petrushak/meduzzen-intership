from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions import AuthorizationError, UserNotFound
from app.schemas.auth import Token
from app.schemas.users import UserSignIn, UserSignUp
from app.services.security import SecurityService
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

    async def get_active_user(self, db: AsyncSession, payload: dict) -> UserSignUp:
        user_email = payload["email"]
        username = user_email.split("@")[0]

        try:
            user = await self._user_service.get_user_by_email(db=db, email=user_email)
        except UserNotFound:
            user = await self._user_service.create_model(
                db=db,
                model_data=UserSignUp(
                    email=user_email, username=username, password=username
                ),
            )
        return user
