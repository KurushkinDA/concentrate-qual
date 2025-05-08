from typing import Optional

from fastapi import APIRouter, Depends, Response, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.concentrate.schemas import (
    SConcentrateCreate,
    SConcentrateRead,
    SConcentrateStats,
    SConcentrateUpdate,
)
from app.concentrate.services.create_concentrate import create_concentrate_service
from app.concentrate.services.delete_concentrate import delete_concentrate_service
from app.concentrate.services.get_all_concentrates import get_all_concentrates_service
from app.concentrate.services.get_concentrate_by_id import get_concentrate_by_id_service
from app.concentrate.services.get_concentrate_statistics import (
    get_concentrate_statistics_service,
)
from app.concentrate.services.update_concentrate import update_concentrate_service
from app.core.database import get_db
from app.schemas import PaginatedResponse, ResponseWithData, SuccessResponse
from app.users.dependencies import get_current_user
from app.users.models import User

router = APIRouter(prefix="/concentrates", tags=["Качественные показатели"])


@router.get(
    "/report",
    response_model=ResponseWithData[SConcentrateStats],
    summary="Получить отчет по показателям за месяц",
    description=(
        "Формирует сводный отчет по содержанию элементов (Fe, Si, Al, Ca, S) "
        "в концентрате за указанный месяц. Возвращает среднее, минимальное и "
        "максимальное значения."
    ),
    status_code=status.HTTP_200_OK,
)
async def get_concentrate_statistics(
    report_month: str,
    session: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return await get_concentrate_statistics_service(session, report_month)


@router.post(
    "",
    response_model=ResponseWithData[SConcentrateRead],
    status_code=status.HTTP_201_CREATED,
    summary="Добавить запись о показателях",
    description=(
        "Добавляет новую запись о качественных показателях концентрата (железо,"
        " кремний, алюминий, кальций, сера) за указанный месяц от текущего "
        "пользователя."
    ),
)
async def create_concentrate(
    data: SConcentrateCreate,
    response: Response,
    session: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return await create_concentrate_service(
        data=data, session=session, user_id=current_user.id
    )


@router.get(
    "/{concentrate_id}",
    response_model=ResponseWithData[SConcentrateRead],
    summary="Получить запись по ID",
    description=(
        "Возвращает данные о показателях концентрата по указанному ID."
        " Требуется авторизация."
    )
)
async def get_concentrate_by_id(
    concentrate_id: int,
    session: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):

    return await get_concentrate_by_id_service(concentrate_id, session)


@router.put(
    "/{concentrate_id}",
    response_model=ResponseWithData[SConcentrateRead],
    summary="Обновить запись по ID",
    description=(
        "Обновляет данные показателей концентрата по ID. Требуется "
        "авторизация. Возвращает обновлённую запись."
    ),
)
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


@router.delete(
    "/{concentrate_id}", 
    response_model=SuccessResponse, 
    summary="Удалить по ID", 
    description=(
        "Удаляет запись по ID. Требуется авторизация"
    )
)
async def delete_concentrate(
    concentrate_id: int,
    session: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return await delete_concentrate_service(
        session=session,
        concentrate_id=concentrate_id,
    )


@router.get(
    "",
    response_model=PaginatedResponse,
    summary="Получить все записи",
    description=(
        "Получает все записи списком. Фильтрация по месяцу."
        "Требуется авторизация."
    ),
)
async def get_all_concentrates(
    report_month: Optional[str] = None,
    session: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return await get_all_concentrates_service(session, report_month)
