from app.users.schemas import SUserPublic
from pydantic import BaseModel, Field, constr, field_validator
from typing import Annotated, Optional
import re

class SConcentrateBase(BaseModel):
    """Базовая схема для показателей концентрата."""
    name: str = Field(..., description="Наименование концентрата")
    iron: float = Field(..., description="Содержание железа (Fe)")
    silicon: float = Field(..., description="Содержание кремния (Si)")
    aluminum: float = Field(..., description="Содержание алюминия (Al)")
    calcium: float = Field(..., description="Содержание кальция (Ca)")
    sulfur: float = Field(..., description="Содержание серы (S)")
    report_month: Annotated[
        str, Field(pattern=r"^\d{4}-\d{2}$", description="Отчётный месяц в формате YYYY-MM")
    ]


class SConcentrateCreate(SConcentrateBase):
    pass

class SConcentrateUpdate(SConcentrateBase):
    pass

class SConcentrateRead(SConcentrateBase):
    """
    Схема для чтения данных о концентрате с дополнительной информацией.

    Наследуется от базовой схемы и включает:
    - ID записи
    - ID пользователя
    - Информацию о пользователе
    """
    id: int = Field(..., description="ID записи")
    user_id: int = Field(..., description="ID пользователя, добавившего запись")
    user: SUserPublic = Field(..., description="Информация о пользователе")

    model_config = {"from_attributes": True}


class SConcentrateStats(BaseModel):
    """Статистика по показателям за месяц."""

    average_iron: float = Field(..., description="Среднее содержание железа")
    min_iron: float = Field(..., description="Минимальное содержание железа")
    max_iron: float = Field(..., description="Максимальное содержание железа")
    
    average_silicon: float = Field(..., description="Среднее содержание кремния")
    min_silicon: float = Field(..., description="Минимальное содержание кремния")
    max_silicon: float = Field(..., description="Максимальное содержание кремния")
    
    average_aluminum: float = Field(..., description="Среднее содержание алюминия")
    min_aluminum: float = Field(..., description="Минимальное содержание алюминия")
    max_aluminum: float = Field(..., description="Максимальное содержание алюминия")
    
    average_calcium: float = Field(..., description="Среднее содержание кальция")
    min_calcium: float = Field(..., description="Минимальное содержание кальция")
    max_calcium: float = Field(..., description="Максимальное содержание кальция")
    
    average_sulfur: float = Field(..., description="Среднее содержание серы")
    min_sulfur: float = Field(..., description="Минимальное содержание серы")
    max_sulfur: float = Field(..., description="Максимальное содержание серы")