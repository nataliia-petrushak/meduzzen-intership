from typing import Any


class ObjectNotFound(Exception):
    def __init__(self, identifier: Any, model_name: str) -> None:
        self.msg = f"{model_name} with {identifier} not found"
        super().__init__(self.msg)


class AuthorizationError(Exception):
    def __init__(self, detail: str) -> None:
        self.msg = f"Authorization failed: {detail}"
        super().__init__(self.msg)


class AccessDeniedError(Exception):
    def __init__(self) -> None:
        self.msg = "Access denied: You do not have permission to modify or delete data"
        super().__init__(self.msg)
