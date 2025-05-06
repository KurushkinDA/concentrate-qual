FROM python:3.13-slim

RUN pip install --no-cache-dir poetry

WORKDIR /app

COPY backend/pyproject.toml backend/poetry.lock* /app/
RUN poetry install --no-root

COPY backend /app

CMD ["poetry", "run", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]