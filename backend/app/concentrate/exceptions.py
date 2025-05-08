"""
Исключения, связанные с качественными показателями концентрата.
Используются в сервисах и роутах для возврата стандартных HTTP-ошибок.
"""

from fastapi import HTTPException, status

ConcentrateNotFound = HTTPException(
    status_code=status.HTTP_404_NOT_FOUND, detail="Запись не найдена"
)

WrongFormatDate = HTTPException(
    status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
    detail="Неверный формат месяца. Используйте ГГГГ-ММ (например, 2025-10)",
)

NoDataFound = HTTPException(
    status_code=status.HTTP_404_NOT_FOUND,
    detail="Нет данных",
)
