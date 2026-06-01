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
Установите PostgreSQL и создайте пользователя octagon с паролем 12345:
sudo apt update && sudo apt install postgresql postgresql-contrib -y
sudo service postgresql start
sudo -u postgres psql
В консоли psql выполните:
CREATE USER octagon WITH PASSWORD '12345';
CREATE DATABASE octagon_db OWNER octagon;
GRANT ALL PRIVILEGES ON DATABASE octagon_db TO octagon;
\q
### 2. Создание виртуального окружения и установка зависимостей
1. Создайте виртуальное окружение:
   python -m venv venv
2. Перейдите в виртуальное окружение:
   source venv/bin/activate
   *(В терминале должна появиться приставка (venv))*
3. Создайте файл requirements.txt и добавьте в него необходимые библиотеки:
   SQLAlchemy
   psycopg2-binary
   python-dotenv
   fastapi
   uvicorn[standard]
4. Установите зависимости:
```bash   pip install -r requirements.txt
```

### 3. Настройка .gitignore и .env
- Убедитесь, что в файле .gitignore указана строка venv/, чтобы окружение не попадало в репозиторий.
- Создайте файл .env в корне проекта и заполните его параметрами подключения:
  DB_HOST=localhost
  DB_PORT=5432
  DB_NAME=octagon_db
  DB_USER=octagon
  DB_PASSWORD=12345
### 4. Структура проекта и модули БД
Проект организован согласно требованиям задания:
- app/db/db.py — подключение к БД, engine, SessionLocal, зависимость get_db()
- app/db/models.py — модели SQLAlchemy Category и Book (связи через ForeignKey и relationship)
- app/db/crud.py — CRUD-функции для обеих таблиц + фильтрация get_books_by_category()
- app/schemas.py — Pydantic-схемы (базовые, для создания/обновления, ответы с id, включён from_attributes=True)
- app/api/categories.py, app/api/books.py — FastAPI-роутеры с CRUD-эндпоинтами
- app/main.py — точка входа, подключение роутеров, эндпоинт /health, авто-создание таблиц
- app/init_db.py — инициализация БД, добавление 2 категорий и 2-4 книг

### 5. Инициализация базы данных
Запустите скрипт для создания таблиц и заполнения начальными данными:
python app/init_db.py
### 6. Запуск FastAPI-сервера
uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
При первом запуске таблицы создаются автоматически через lifespan в main.py.

### 7. Тестирование API
Откройте в браузере:
- Swagger UI: http://127.0.0.1:8000/docs
- Health Check: http://127.0.0.1:8000/health

Примеры запросов через curl:
# Создание категории (возвращает 201)
curl -X POST http://127.0.0.1:8000/categories/ \
  -H "Content-Type: application/json" \
  -d '{"title": "Техническая литература"}'

# Создание книги (возвращает 201, проверяет существование категории)
curl -X POST http://127.0.0.1:8000/books/ \  -H "Content-Type: application/json" \
  -d '{"title": "Clean Code", "description": "Robert Martin", "price": 1200.0, "category_id": 1, "url": ""}'

# Получение списка книг (возвращает 200)
curl http://127.0.0.1:8000/books/

# Фильтрация по категории
curl "http://127.0.0.1:8000/books/?category_id=1"
### 8. Проверка данных в PostgreSQL
После выполнения запросов через API убедитесь, что данные записаны в БД:
sudo -u postgres psql -d octagon_db -c "SELECT * FROM categories;"
sudo -u postgres psql -d octagon_db -c "SELECT * FROM books;"
[01.06.2026 11:53] Артём: ## Документация и подтверждение выполнения (examples/)
В папке examples/ расположены скриншоты, подтверждающие выполнение чек-листа:
1. swagger.png — открытая страница http://127.0.0.1:8000/docs с перечнем всех эндпоинтов
2. request.png — результат успешного запроса к API (HTTP-код 200/201 и JSON-ответ)
3. psql.png — вывод SELECT из таблиц PostgreSQL после работы API

## Примечания
- Файлы .env и папка venv/ исключены из Git через .gitignore.
- При создании/обновлении книги проверяется существование category_id. При отсутствии категории возвращается ошибка 404.
- Все эндпоинты возвращают корректные HTTP-коды (200, 201, 204, 404, 422).
- Для тестирования можно использовать встроенный Swagger UI, Postman или curl.
