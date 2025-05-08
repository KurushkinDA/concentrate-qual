"""
Модуль конфигурации проекта.

Загружает переменные окружения из `.env` файла с помощью Pydantic Settings.
Определяет параметры подключения к базам данных, настройки логирования и авторизации.
"""

from typing import Literal
from pydantic_settings import BaseSettings
from pydantic import ConfigDict

class Settings(BaseSettings): 
    # Основные параметры проекта
    PROJECT_NAME: str
    MODE: Literal['DEV', 'TEST', 'PROD']
    LOG_LEVEL: Literal['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL']

    # Настройки основной базы данных
    DB_HOST: str
    DB_PORT: int
    DB_USER: str
    DB_PASS: str
    DB_NAME: str

    # Настройки тестовой базы данных
    TEST_DB_HOST: str
    TEST_DB_PORT: int
    TEST_DB_USER: str
    TEST_DB_PASS: str
    TEST_DB_NAME: str

    # Настройки JWT авторизации
    AUTH_SECRET_KEY: str
    AUTH_ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int
    REFRESH_TOKEN_EXPIRE_DAYS: int

    # Загрузка настроек из .env файла
    model_config = ConfigDict(env_file=".env", extra="forbid")  # type: ignore

    @property
    def DATABASE_URL(self) -> str:
        """URL подключения к основной базе данных."""
        return (
            f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASS}"
            f"@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
        )

    @property
    def TEST_DATABASE_URL(self) -> str:
        """URL подключения к тестовой базе данных."""
        return (
            f"postgresql+asyncpg://{self.TEST_DB_USER}:{self.TEST_DB_PASS}"
            f"@{self.TEST_DB_HOST}:{self.TEST_DB_PORT}/{self.TEST_DB_NAME}"
        )

# Инициализация глобального объекта настроек
settings = Settings()  # type: ignore