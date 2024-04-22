import jwt

from app.config import settings
from app.core.exceptions import AuthorizationError


class Auth0Service:
    @staticmethod
    def verify(token: str):
        jwt_client = jwt.PyJWKClient(settings.auth_url)

        try:
            signing_key = jwt_client.get_signing_key_from_jwt(token).key
        except jwt.exceptions.PyJWKClientError as error:
            raise AuthorizationError(detail=str(error))
        except jwt.exceptions.DecodeError as error:
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
