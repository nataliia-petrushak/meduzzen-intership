from datetime import datetime, timedelta

import jwt
from passlib.context import CryptContext
from app.config import settings

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
