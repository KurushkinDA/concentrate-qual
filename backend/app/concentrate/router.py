from typing import List, Optional
from app.concentrate.services.delete_concentrate import delete_concentrate_service
from app.concentrate.services.get_all_concentrates import get_all_concentrates_service
from app.concentrate.services.get_concentrate_by_id import get_concentrate_by_id_service
from app.concentrate.services.get_concentrate_statistics import get_concentrate_statistics_service
from app.concentrate.services.update_concentrate import update_concentrate_service
from fastapi import APIRouter, Depends, Request, Response, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db
from app.users.dependencies import get_current_user
from app.users.models import User
from app.concentrate.schemas import SConcentrateCreate, SConcentrateRead, SConcentrateStats, SConcentrateUpdate
from app.schemas import PaginatedResponse, ResponseWithData, SuccessResponse
from app.concentrate.services.create_concentrate import create_concentrate_service

router = APIRouter(prefix="/concentrates", tags=["Качественные показатели"])



@router.get(
    "/report",
    response_model=ResponseWithData[SConcentrateStats],
    summary="Получить отчет по показателям за месяц",
    status_code=status.HTTP_200_OK
)
async def get_concentrate_statistics(
    report_month: str,
    session: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return await get_concentrate_statistics_service(session, report_month)

@router.post("", 
             response_model=ResponseWithData[SConcentrateRead],
             status_code=status.HTTP_201_CREATED,
             summary="Добавить")
async def create_concentrate(
    data: SConcentrateCreate,
    response: Response,
    session: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return await create_concentrate_service(
        data=data, 
        session=session, 
        user_id=current_user.id
    )


@router.get("/{concentrate_id}", 
            response_model=ResponseWithData[SConcentrateRead],
            summary="Получить запись по ID")
async def get_concentrate_by_id(
    concentrate_id: int,
    session: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):

    return await get_concentrate_by_id_service(concentrate_id, session)


@router.put("/{concentrate_id}", 
            response_model=ResponseWithData[SConcentrateRead],
            summary="Обновить")
async def update_concentrate(
    concentrate_id: int,
    data: SConcentrateUpdate,
    session: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return await update_concentrate_service(
        concentrate_id=concentrate_id,
        data=data,
        session=session,
    )


@router.delete("/{concentrate_id}", 
               response_model=SuccessResponse, 
               summary="Удалить по ID")
async def delete_concentrate(
    concentrate_id: int,
    session: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return await delete_concentrate_service(
        session=session,
        concentrate_id=concentrate_id,
    )


@router.get(
    "",
    response_model=PaginatedResponse[SConcentrateRead],
    summary="Получить все записи"
)
async def get_all_concentrates(
    report_month: Optional[str] = None,
    session: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return await get_all_concentrates_service(session, report_month)


