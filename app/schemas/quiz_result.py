from datetime import datetime
from uuid import UUID

from pydantic import BaseModel


class Answers(BaseModel):
    question: str
    answers: list
    is_correct: bool


class AllQuizResults(BaseModel):
    date: datetime
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
