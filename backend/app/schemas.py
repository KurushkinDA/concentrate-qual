"""
Базовые схемы ответов API.

Содержит универсальные шаблоны ответов, которые можно переиспользовать в любом приложении:

- ResponseWithData — ответ с сообщением и данными (например, объект).
- SuccessResponse — простой ответ с сообщением об успехе.
- PaginatedResponse — ответ с массивом элементов (для списков).
"""

from typing import Generic, Optional, TypeVar, List
from pydantic import BaseModel
from pydantic.generics import GenericModel

T = TypeVar("T")

class ResponseWithData(GenericModel, Generic[T]):
    """
    Универсальный ответ, содержащий:
    - message: текстовое сообщение (например, "Успешно выполнено")
    - data: объект данных произвольного типа (T)
    """
    message: Optional[str] = None
    data: Optional[T]

class SuccessResponse(BaseModel):
    """
    Простой ответ, сигнализирующий об успешном завершении операции.
    - message: описание результата (например, "Удалено успешно")
    """
    message: str

class PaginatedResponse(GenericModel, Generic[T]):
    """
    Ответ для пагинированных списков.
    - items: список элементов типа T
    """
    items: List[T]