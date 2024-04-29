from app.db.alembic.repos.base_repo import BaseRepository
from app.db.models import Company


class CompanyRepository(BaseRepository):
    def __init__(self):
        super().__init__(Company)
