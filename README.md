# 🧪 Система учёта качественных показателей железорудного концентрата

## 📌 Описание

Веб-приложение для внесения и анализа качественных показателей железорудного концентрата.
Позволяет добавлять данные по месяцам и получать статистику по содержанию элементов:

* Fe (железо)
* Si (кремний)
* Al (алюминий)
* Ca (кальций)
* S (сера)

Приложение разделено на **Backend** и **Frontend**, с поддержкой авторизации.

---

## 🛠 Стэк

### 🔹 Backend (FastAPI)

* **FastAPI** — основной веб-фреймворк
* **SQLAlchemy 2.0** — асинхронная ORM
* **asyncpg** — асинхронный драйвер PostgreSQL
* **Alembic** — миграции базы данных
* **Pydantic v2** — валидация данных
* **Passlib (bcrypt)** — хеширование паролей
* **JWT (PyJWT)** — авторизация по токенам
* **Docker** — контейнеризация окружения
* **Pytest + pytest-asyncio** — тестирование

### 🔹 Frontend (React)

* **React** — библиотека для построения UI
* **React Router** — маршрутизация
* **TailwindCSS** — утилитарная стилизация
* **Handsontable** — редактирование таблиц
* **Sonner** — система уведомлений

### 🔹 Dev & Lint Tools

* **Poetry** — управление зависимостями и виртуальным окружением
* **Black / isort / flake8 / autoflake** — автоформатирование и линтинг

### 🔹 Инфраструктура

* **Docker Compose** — оркестрация сервисов (бэкенд, фронтенд, БД, тестовая среда)
* **PostgreSQL** — основная БД проекта

Проект структурирован по принципу разделения ответственности: `backend/` — для backend-приложения, `frontend/` — для интерфейса. Тесты backend находятся в папке `backend/tests/`.

---

## 🧭 Структура проекта

```
project-root/
├── backend/                       # Backend на FastAPI
│   ├── app/
│   │   ├── concentrate/           # Работа с концентратами
│   │   ├── users/                 # Авторизация и управление пользователями
│   │   ├── core/                  # Настройки, база данных
│   │   ├── schemas.py             # Общие схемы ответов
│   │   └── main.py                # Точка входа FastAPI
│   ├── tests/                     # Unit-тесты (по слоям)
│   │   └── unit/
│   │       ├── users/             # Тесты пользователей
│   │       ├── concentrate/       # Тесты концентратов
│   │       └── conftest.py        # Общие фикстуры для тестов
│   └── pyproject.toml             # Зависимости и настройки (Poetry)
│
├── frontend/                      # Frontend на React
│   ├── src/
│   │   ├── components/            # Переиспользуемые компоненты
│   │   ├── pages/                 # Страницы (Login, Home и т.д.)
│   │   ├── api.js                 # Запросы к бэкенду
│   │   └── App.js                 # Главный компонент
│   └── package.json               # Зависимости React
│
├── docker-compose.dev.yml         # Compose-файл для разработки
├── docker-compose.test.yml        # Compose-файл для тестов
└── .env                           # Переменные окружения
```

---

## 🚀 Команды запуска

**Запуск проекта в dev-режиме:**

```bash
docker compose -f docker-compose.dev.yml up --build
```

**Запуск всех тестов:**

```bash
docker compose -f docker-compose.test.yml up --build
```

**Запуск конкретного теста:**

```bash
docker compose -f docker-compose.test.yml run --rm backend_test poetry run pytest tests/unit/users/test_create_user.py -v -s
```


**Frontend доступен по адресу:** `http://localhost:3000`
**Backend доступен по адресу:** `http://localhost:8000/docs`

Автоматически создаются 2 пользователя: admin (pas: admin), user (pas: user)

---

## ✅ Прогресс

* [x] CRUD для пользователей
* [x] Авторизация и логаут
* [x] CRUD для концентратов
* [x] Статистика по месяцам
* [x] Юнит-тесты для сервисного слоя
* [x] Конфигурация и окружение через `.env`

---

## 📬 Обратная связь

Если нашли баг или есть предложение — welcome в Issues или на почту ✉️ [kurushkin.dimka@yandex.ru](mailto:kurushkin.dimka@yandex.ru)

---

> Проект разработан с ❤️ для тестового задания (2025)
