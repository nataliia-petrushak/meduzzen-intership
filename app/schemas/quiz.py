from uuid import UUID

from pydantic import BaseModel, field_validator

from app.core.exceptions import ValidationError


class Question(BaseModel):
    question: str
    variants: list[str]
    answers: list[str]

    @classmethod
    @field_validator("variants", mode="before")
    def validate_variants(cls, variants: list[str]):
        if len(variants) < 2:
            raise ValidationError(detail="Variants of answers should be at least 2")
        return variants


class QuizBase(BaseModel):
    name: str
    description: str
    questions: list[Question]

    @classmethod
    @field_validator("questions", mode="before")
    def validate_question(cls, value: list):
        if len(value) < 2:
            raise ValidationError(detail="Questions should be at least 2")
        return value


class QuizCreate(QuizBase):
    pass


class QuizUpdate(QuizBase):
    pass


class GetQuiz(QuizBase):
    id: UUID
