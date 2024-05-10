from app.db.alembic.repos.base_repo import BaseRepository
from app.db.models import Request


class RequestRepository(BaseRepository):
    def __init__(self):
        super().__init__(Request)
