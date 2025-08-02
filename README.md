# 📦 Friends API

Проект на FastAPI с асинхронной работой с базой данных PostgreSQL, Alembic для миграций и Poetry для управления зависимостями.

---

## 📁 Структура проекта
.
├── .env # Конфигурация окружения (не коммитится)
├── .gitignore # Игнорируемые файлы Git
├── alembic.ini # Конфигурация Alembic
├── config.py # Загрузка настроек из .env
├── database.py # Подключение к БД и Base
├── main.py # Точка входа FastAPI-приложения
├── poetry.lock # Lock-файл Poetry
├── pyproject.toml # Конфигурация зависимостей Poetry
├── README.md # Документация проекта
│
├── migrations/ # Миграции Alembic
│ ├── env.py
│ ├── script.py.mako
│ ├── README
│ └── versions/
│ └── <timestamp>_init.py
│
└── models/ # SQLAlchemy-модели
├── base.py
├── friends.py
├── post.py
├── user.py
└── init.py

## 🚀 Быстрый старт

### 1. Установка Poetry (если ещё не установлен)

pip install poetry

### 2. Установка зависимостей

poetry install

### 3. Активация виртуального окружения

poetry env activate или poetry shell

### 4. Создай .env файл в корне проекта

## в нем укажите следующие параметры:

# DATABASE_HOST=
# DATABASE_PORT=
# DATABASE_NAME=
# DATABASE_USER=
# DATABASE_PASSWORD=

## В DATABASE_HOST= укажите хост базы. по умолчанию он "localhost"ю
## В DATABASE_PORT= укажите порт базы. по умолчанию он "5432".
## В DATABASE_NAME= укажите название базы.
## В DATABASE_USER= укажите имя получателя базы данных.
## В DATABASE_PASSWORD= укажите пароль пользователя.

### Файл .env используется для хранения конфиденциальных или конфигурируемых параметров окружения (переменных среды), которые:

    нельзя жёстко прописывать в коде (например, пароли или URL базы данных),

    и можно легко менять без редактирования самого исходного кода.

#### Создать новую миграцию

alembic revision --autogenerate -m "название или пояснения для лутшего понимания"

#### Применить миграции

alembic upgrade head

## Для запуска сервера рекомендуется использовать команду:

poetry run uvicorn main:app --reload




### При работе с проектом могут выявлятся ошибки, так что прошу сразу сообщить о них. ###