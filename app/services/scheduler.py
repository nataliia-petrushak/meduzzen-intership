from app.db.database import SessionLocal
from app.logger import custom_logger
from app.services.notification import NotificationService


class SchedulerService:
    def __init__(self) -> None:
        self._notification_service = NotificationService()
        self._db = SessionLocal()

    async def send_reminder_notifications(self):
        custom_logger.info("Starting to send reminder notifications")
        await self._notification_service.send_reminder_notifications(db=self._db)
