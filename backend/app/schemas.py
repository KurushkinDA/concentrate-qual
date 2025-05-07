from typing import Generic, Optional, TypeVar, List
from pydantic import BaseModel
from pydantic.generics import GenericModel

T = TypeVar("T")

class ResponseWithData(GenericModel, Generic[T]):
    message: Optional[str] = None
    data: Optional[T]

class SuccessResponse(BaseModel):
    message: str

class PaginatedResponse(GenericModel, Generic[T]):
    items: List[T]
