"""
Точка входа в FastAPI-приложение.

- Инициализирует экземпляр FastAPI.
- Подключает роутеры пользователей и концентрата.
- Настраивает CORS для взаимодействия с фронтендом.
- Отключает Swagger и ReDoc в продакшене.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.concentrate.router import router as router_concentrate
from app.core.config import settings
from app.users.router import router as router_users

# Инициализация FastAPI
app = FastAPI(
    title=(
        "Cистема добавления данных о качественных показателях "
        "железорудного концентрата"
    ),
    docs_url=None if settings.MODE == "PROD" else "/docs",
    redoc_url=None if settings.MODE == "PROD" else "/redoc",
    openapi_url=None if settings.MODE == "PROD" else "/openapi.json",
)

# Подключение роутеров
app.include_router(router_users)
app.include_router(router_concentrate)

# Разрешённые источники (для CORS)
origins = [
    "http://localhost:3000",  # Фронтенд React (локальная разработка)
]

# Настройка CORS — требуется для работы с куками и авторизацией между фронтом и бэком
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS", "DELETE", "PATCH", "PUT"],
    allow_headers=[
        "Content-Type",
        "Set-Cookie",
        "Access-Control-Allow-Headers",
        "Access-Control-Allow-Origin",
        "Authorization",
    ],
)
