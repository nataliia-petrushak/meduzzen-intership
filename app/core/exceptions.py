from typing import Any
from uuid import UUID


class ObjectNotFound(Exception):
    def __init__(self, identifier: Any, model_name: str = "Object") -> None:
        self.msg = f"{model_name} with {identifier} not found"
        super().__init__(self.msg)


class UserNotFound(ObjectNotFound):
    def init(self, identifier: UUID, model_name: str = "User") -> None:
        super().__init__(model_name=model_name, identifier=identifier)


class AuthorizationError(Exception):
    def __init__(self, detail: str) -> None:
        self.msg = f"Authorization failed: {detail}"
        super().__init__(self.msg)
