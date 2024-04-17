from app.db.models import UserBase
from app.db.repos.base_repo import BaseRepository


class UserServices(BaseRepository):
    def __init__(self):
        super().__init__(UserBase)


user_services = UserServices()
