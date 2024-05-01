from app.db.alembic.repos.base_repo import BaseRepository
from app.db.models import Quiz


class QuizRepository(BaseRepository):
    def __init__(self):
        super().__init__(Quiz)
