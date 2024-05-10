from typing import Any
from uuid import UUID


class ObjectNotFound(Exception):
    def __init__(self, identifier: Any, model_name: str) -> None:
        self.msg = f"{model_name} with identifier - {identifier} not found"
        super().__init__(self.msg)


class NameExistError(Exception):
    def __init__(self, model_name: str, name: str) -> None:
        self.msg = f"The {model_name} with name: {name} already exists"
        super().__init__(self.msg)


class AuthorizationError(Exception):
    def __init__(self, detail: str) -> None:
        self.msg = f"Authorization failed: {detail}"
        super().__init__(self.msg)


class AccessDeniedError(Exception):
    def __init__(self) -> None:
        self.msg = "Access denied: You do not have permission to modify or delete data"
        super().__init__(self.msg)


class OwnerRequestError(Exception):
    def __init__(self) -> None:
        self.msg = (
            "The owner of the company cannot invite themselves "
            "and send join request to their companies."
        )
        super().__init__(self.msg)


class AssignError(Exception):
    def __init__(self, identifier: Any) -> None:
        self.msg = f"You can`t assign user with {identifier} for this position"
        super().__init__(self.msg)


class ValidationError(Exception):
    def __init__(self, detail: str) -> None:
        self.msg = detail
        super().__init__(self.msg)


class IntegrityError(Exception):
    def __init__(self, company_id: UUID, user_id: UUID) -> None:
        self.msg = f"The object with company id {company_id} and user_id {user_id} already exists"
        super().__init__(self.msg)
