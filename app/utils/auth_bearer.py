import jwt
from fastapi import Request
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from app.core.exceptions import AuthorizationError
from app.services.auth0 import Auth0Service
from app.services.security import SecurityService


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


auth_bearer = AuthBearer()
