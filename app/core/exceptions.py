from typing import Any
from uuid import UUID


class ObjectNotFound(Exception):
    def __init__(self, model_name: str, object_id: Any) -> None:
        self.msg = f"{model_name} with given identifier - {object_id} not found"
        super().__init__(self.msg)


class UserNotFound(ObjectNotFound):
    def init(self, model_id: UUID, model_name: str = "User") -> None:
        super().__init__(model_name=model_name, object_id=model_id)

