## Описание

Система добавления данных о качественных показателях железорудного концентрата и просмотра сводной информации по всем концентратам. Качественные показатели железорудного концентрата: содержание железа, содержание кремния, содержание алюминия, содержание кальция, содержание серы. Данные вносятся ежемесячно

## Команды

Запустить проект:
docker compose -f docker-compose.dev.yml up --build

Запустить все тесты: 
docker compose -f docker-compose.test.yml up --build

Запустить конретные тесты: 
docker compose -f docker-compose.test.yml run --rm backend_test poetry run pytest tests/test_index.py -s -v