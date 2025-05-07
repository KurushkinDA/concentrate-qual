from fastapi import FastAPI

from app.users.router import router as router_users
from app.concentrate.router import router as router_concentrate
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings


app = FastAPI(
    title="Cистема добавления данных о качественных показателях железорудного концентрата",
    docs_url=None if settings.MODE == "PROD" else "/docs",
    redoc_url=None if settings.MODE == "PROD" else "/redoc",
    openapi_url=None if settings.MODE == "PROD" else "/openapi.json",
)

# Подключение роутеров
app.include_router(router_users)
app.include_router(router_concentrate)

# Допустимые домены
origins = [
    'http://localhost:3000'
] 

# Настройка CORS
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
        "Authorization"
    ],
)





