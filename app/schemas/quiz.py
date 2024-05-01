from uuid import UUID

from pydantic import BaseModel


class QuizBase(BaseModel):
    name: str
    description: str
    questions: list[dict]


class QuizCreate(QuizBase):
    pass


class QuizUpdate(QuizBase):
    pass


class GetQuiz(QuizBase):
    id: UUID
