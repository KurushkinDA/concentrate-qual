from app.users.schemas import SUserPublic
from pydantic import BaseModel, Field, constr, field_validator
from typing import Annotated, Optional
import re

class SConcentrateBase(BaseModel):
    name: str
    iron: float
    silicon: float
    aluminum: float
    calcium: float
    sulfur: float
    report_month: Annotated[str, Field(pattern=r"^\d{4}-\d{2}$")]  # формат YYYY-MM


class SConcentrateCreate(SConcentrateBase):
    pass

class SConcentrateUpdate(SConcentrateBase):
    pass

class SConcentrateRead(SConcentrateBase):
    id: int
    user_id: int
    user: SUserPublic

    model_config = {"from_attributes": True}


class SConcentrateStats(BaseModel):
    average_iron: float
    min_iron: float
    max_iron: float

    average_silicon: float
    min_silicon: float
    max_silicon: float

    average_aluminum: float
    min_aluminum: float
    max_aluminum: float

    average_calcium: float
    min_calcium: float
    max_calcium: float

    average_sulfur: float
    min_sulfur: float
    max_sulfur: float