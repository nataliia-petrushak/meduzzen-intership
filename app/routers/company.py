from uuid import UUID
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from app.db.database import get_db
from app.schemas.company import GetCompany, CompanyDetail, CompanyUpdate, CompanyCreate
from app.schemas.users import GetUser
from app.services.auth import get_authenticated_user
from app.services.company import CompanyService
from app.services.user import UserService

router = APIRouter(tags=["companies"], prefix="/companies")


@router.post("/", response_model=GetCompany, status_code=status.HTTP_201_CREATED)
async def create_company(
    model_data: CompanyCreate,
    db: AsyncSession = Depends(get_db),
    user: GetUser = Depends(get_authenticated_user),
    company_service: CompanyService = Depends(CompanyService),
) -> GetCompany:
    return await company_service.create_model(db=db, model_data=model_data, user=user)


@router.get("/", response_model=list[GetCompany], status_code=status.HTTP_200_OK)
async def get_company_list(
    offset: int = 0,
    limit: int = 10,
    db: AsyncSession = Depends(get_db),
    company_service: UserService = Depends(CompanyService),
) -> list[GetCompany]:
    return await company_service.get_model_list(db=db, offset=offset, limit=limit)


@router.get(
    "/{company_id}", response_model=CompanyDetail, status_code=status.HTTP_200_OK
)
async def get_company_by_id(
    company_id: UUID,
    db: AsyncSession = Depends(get_db),
    company_service: UserService = Depends(CompanyService),
) -> CompanyDetail:
    return await company_service.get_model_by_id(db=db, model_id=company_id)


@router.patch(
    "/{company_id}", response_model=GetCompany, status_code=status.HTTP_200_OK
)
async def update_company(
    company_id: UUID,
    company_data: CompanyUpdate,
    user: GetUser = Depends(get_authenticated_user),
    db: AsyncSession = Depends(get_db),
    company_service: CompanyService = Depends(CompanyService),
) -> GetCompany:
    return await company_service.update_model(
        model_data=company_data, db=db, model_id=company_id, user=user
    )


@router.delete("/{company_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_company(
    company_id: UUID,
    user: GetUser = Depends(get_authenticated_user),
    db: AsyncSession = Depends(get_db),
    company_service: CompanyService = Depends(CompanyService),
) -> None:
    return await company_service.delete_model(model_id=company_id, db=db, user=user)
