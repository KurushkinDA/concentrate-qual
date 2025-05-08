from typing import Annotated

from pydantic import BaseModel, Field


class SUserAuth(BaseModel):
    """Модель авторизации пользователя (логин и пароль)."""

    username: str = Field(..., description="Имя пользователя для входа")
    password: str = Field(..., description="Пароль пользователя")


class SUserCreate(BaseModel):
    """Модель создания нового пользователя с валидацией."""

    username: Annotated[
        str,
        Field(
            min_length=3,
            max_length=50,
            strip_whitespace=True,
            description="Имя пользователя (от 3 до 50 символов)",
        ),
    ]
    password: Annotated[
        str,
        Field(
            min_length=3,
            max_length=100,
            description="Пароль пользователя (от 3 символов)",
        ),
    ]


class SUserPublic(BaseModel):
    """Публичная информация о пользователе, возвращаемая в ответах."""

    id: int = Field(..., description="Уникальный идентификатор пользователя")
    username: str = Field(..., description="Имя пользователя")

    model_config = {"from_attributes": True}
