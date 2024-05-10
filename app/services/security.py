from datetime import datetime, timedelta

import jwt
from passlib.context import CryptContext
from app.config import settings
from app.core.exceptions import AuthorizationError

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class SecurityService:
    @staticmethod
    def hash_password(password: str) -> str:
        return pwd_context.hash(password)

    @staticmethod
    def verify_password(password: str, hashed_password: str) -> bool:
        return pwd_context.verify(password, hashed_password)

    @staticmethod
    def encode_user_token(email: str) -> str:
        payload = {
            "email": email,
            "expires": f"{datetime.utcnow() + timedelta(minutes=10)}",
        }
        token = jwt.encode(
            payload, settings.JWT_SECRET, algorithm=settings.JWT_ALGORITHMS
        )
        return token

    @staticmethod
    def decode_user_token(token: str) -> dict:
        return jwt.decode(
            token, settings.JWT_SECRET, algorithms=[settings.JWT_ALGORITHMS]
        )


class Auth0Security:
    @staticmethod
    def verify(token: str):
        jwt_client = jwt.PyJWKClient(settings.auth_url)

        try:
            signing_key = jwt_client.get_signing_key_from_jwt(token).key
        except (jwt.exceptions.PyJWKClientError, jwt.exceptions.DecodeError) as error:
            raise AuthorizationError(detail=str(error))
        try:
            payload = jwt.decode(
                token,
                key=signing_key,
                algorithms=[settings.AUTH0_ALGORITHMS],
                audience=settings.AUTH0_IDENTIFIER,
                issuer=settings.AUTH0_ISSUER,
            )
        except jwt.PyJWTError as error:
            raise AuthorizationError(detail=str(error))
        return payload
