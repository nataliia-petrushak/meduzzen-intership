from uuid import UUID

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from app.db.database import get_db
from app.schemas.quiz import GetQuiz, QuizCreate, QuizUpdate
from app.schemas.users import GetUser
from app.services.auth import get_authenticated_user
from app.services.quiz import QuizService

router = APIRouter(tags=["quiz"], prefix="/company/{company_id}/quiz")


@router.post(
    "/", response_model=GetQuiz, status_code=status.HTTP_201_CREATED
)
async def create_quiz(
    company_id: UUID,
    quiz_data: QuizCreate,
    user: GetUser = Depends(get_authenticated_user),
    quiz_service: QuizService = Depends(QuizService),
    db: AsyncSession = Depends(get_db),
) -> GetQuiz:
    return await quiz_service.create_quiz(
        db=db, company_id=company_id, quiz_data=quiz_data, user=user
    )


@router.get(
    "/", response_model=list[GetQuiz], status_code=status.HTTP_200_OK
)
async def get_quiz_list(
    company_id: UUID,
    user: GetUser = Depends(get_authenticated_user),
    db: AsyncSession = Depends(get_db),
    offset: int = 0,
    limit: int = 10,
    quiz_service: QuizService = Depends(QuizService),
) -> list[GetQuiz]:
    return await quiz_service.get_quiz_list(
        db=db, company_id=company_id, offset=offset, limit=limit, user=user
    )


@router.patch(
    "/{quiz_id}",
    response_model=GetQuiz,
    status_code=status.HTTP_200_OK,
)
async def update_quiz(
    company_id: UUID,
    quiz_id: UUID,
    quiz_data: QuizUpdate,
    user: GetUser = Depends(get_authenticated_user),
    db: AsyncSession = Depends(get_db),
    quiz_service: QuizService = Depends(QuizService),
) -> GetQuiz:
    return await quiz_service.update_quiz(
        db=db, company_id=company_id, quiz_id=quiz_id, quiz_data=quiz_data, user=user
    )


@router.delete("/{quiz_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_quiz(
    company_id: UUID,
    quiz_id: UUID,
    user: GetUser = Depends(get_authenticated_user),
    db: AsyncSession = Depends(get_db),
    quiz_service: QuizService = Depends(QuizService),
) -> None:
    return await quiz_service.delete_quiz(
        db=db, company_id=company_id, quiz_id=quiz_id, user=user
    )
