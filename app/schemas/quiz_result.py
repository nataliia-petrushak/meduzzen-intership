from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, Field


class Answers(BaseModel):
    question: str
    answers: list
    is_correct: bool = False

    @field_validator("answers")
    def validate_answers(cls, answers: list) -> list:
        if len(answers) == 0:
            raise ValidationError(detail="Question must have at least one answer")
        return answers

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
    rating: float
