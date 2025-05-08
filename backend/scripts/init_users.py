import asyncio
from app.core.database import async_session_maker
from app.users.schemas import SUserCreate
from app.users.services.create_user import create_user_service

users_to_add = [
    {"username": "admin", "password": "admin"},
    {"username": "user", "password": "user"},
]

async def main():
    async with async_session_maker() as session:
        for user_data in users_to_add:
            try:
                await create_user_service(SUserCreate(**user_data), session)
                print(f"Пользователь '{user_data['username']}' создан.")
            except Exception as e:
                print(f"Ошибка создания пользователя '{user_data['username']}': {e}")

if __name__ == '__main__':
    asyncio.run(main())