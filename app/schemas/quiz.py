from uuid import UUID

from pydantic import BaseModel, field_validator

from app.core.exceptions import ValidationError


class Question(BaseModel):
    question: str
    variants: list[str]
    answers: list[str]

    @field_validator("variants", mode="before")
    @classmethod
    def validate_variants(cls, variants: list[str]):
        if len(variants) < 2:
            raise ValidationError(detail="Variants of answers should be at least 2")
        return variants


class QuizBase(BaseModel):
    name: str
    description: str
    questions: list[Question]

    @field_validator("name", mode="before")
    @classmethod
    def validate_name(cls, name: str):
        if len(name) > 100:
            raise ValidationError(detail="Quiz name is too long")
        if len(name) < 1:
            raise ValidationError(detail="Quiz name is too short")
        return name

    @field_validator("questions", mode="before")
    @classmethod
    def validate_questions(cls, questions: list):
        if len(questions) < 2:
            raise ValidationError(detail="Questions should be at least 2")
        return questions


class QuizCreate(QuizBase):
    pass


class QuizUpdate(QuizBase):
    pass


class GetQuiz(QuizBase):
    id: UUID
