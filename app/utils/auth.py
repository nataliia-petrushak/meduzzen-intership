import jwt
from fastapi import Security
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from app.core.exceptions import AuthorizationError
from app.services.auth0 import Auth0Service
from app.services.security import SecurityService


security = HTTPBearer()


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
