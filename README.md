# Deribit Price Parser

Парсер цен криптовалют с Deribit API с сохранением в PostgreSQL и периодическим обновлением через Celery.

## Стек

Python 3.12

FastAPI

Celery + Redis

PostgreSQL

Docker + Docker Compose

## Установка и запуск

### Клонируем репозиторий:

``` bash
https://github.com/Gasuaska/test_deribit_parser.git
cd test_deribit_parser
```

### Создаем .env файл:

```
DATABASE_URL=postgresql://user:password@db:5432/deribit_db
POSTGRES_DB=deribit_db
POSTGRES_USER=user
POSTGRES_PASSWORD=password
CELERY_BROKER_URL=redis://redis:6379/0
```

### Запуск Docker Compose:

``` bash
docker compose up --build
```

### Проверяем, что всё работает:

FastAPI: http://localhost:8000/docs

Celery воркер и Beat логи: выводят успешное получение данных

## Эндпоинты

```
GET /prices?ticker=<TICKER>limit=<LIMIT_INT>
```
— все цены указанного тикера, limit - опционально

```
GET /prices/latest?ticker=<TICKER> 
```
— последняя цена тикера

```
GET /prices/filter?ticker=<TICKER>&from_ts=<TS1>&to_ts=<TS2>
```
— цены указанного тикера за указанное время

## Тикеры

Список доступных тикеров хранится в app/constants.py в TICKERS.

## Логи и мониторинг
Приложение логирует в файл **app.log**
