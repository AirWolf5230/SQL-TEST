# SQL-TEST: REST API для управления книгами и категориями (PostgreSQL + FastAPI)

## Описание
Проект реализует REST API для работы с базой данных PostgreSQL на основе фреймворков SQLAlchemy и FastAPI. Выполнен в рамках заданий 5 и 6. Включает настройку БД, реализацию CRUD-операций, валидацию через Pydantic, фильтрацию по категориям и автоматическую документацию через Swagger.

## Стек технологий
- PostgreSQL
- Python 3.10+
- SQLAlchemy 2.0
- FastAPI + Uvicorn
- Pydantic
- python-dotenv

## Полная последовательность настройки и запуска

### 1. Установка PostgreSQL в WSL
Установите PostgreSQL и создайте пользователя `octagon` с паролем `12345`:
```bash
sudo apt update && sudo apt install postgresql postgresql-contrib -y
sudo service postgresql start
sudo -u postgres psql