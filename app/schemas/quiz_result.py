from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, Field

from app.schemas.company import GetCompany
from app.schemas.quiz import GetQuiz
from app.schemas.users import GetUser


class Answers(BaseModel):
    question: str
    answers: list
    is_correct: bool


class AllQuizResults(BaseModel):
    date: datetime = Field(default_factory=datetime.now)
    num_corr_answers: int
    questions_count: int


class QuizResultBase(BaseModel):
    all_results: list[AllQuizResults]


class GetQuizResult(QuizResultBase):
    id: UUID
    user_id: UUID
    company_id: UUID
    quiz_id: UUID


class Rating(BaseModel):
    rating: float | None


class RedisResult(BaseModel):
    user_id: UUID
    company_id: UUID
    quiz_id: UUID
    answers: list[Answers]
