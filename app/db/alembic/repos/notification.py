from app.db.alembic.repos.base_repo import BaseRepository
from app.db.models import Notification


class NotificationRepository(BaseRepository):
    def __init__(self) -> None:
        super().__init__(Notification)
