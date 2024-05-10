from datetime import datetime
from uuid import UUID

from pydantic import BaseModel


class AvgScoreWithTime(BaseModel):
    date: datetime
    score: float


class QuizWithCompleteTime(BaseModel):
    quiz_id: UUID
    date: datetime


class UsersQuizCompleteTime(BaseModel):
    user_id: UUID
    date: datetime
