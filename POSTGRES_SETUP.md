# Настройка PostgreSQL

## Создание базы данных

```bash
# Подключиться к PostgreSQL
sudo -u postgres psql

# Создать базу данных
CREATE DATABASE yartumba;

# Создать пользователя
CREATE USER yartumba_user WITH PASSWORD 'your_password';

# Выдать права
GRANT ALL PRIVILEGES ON DATABASE yartumba TO yartumba_user;
\q
```

## Конфигурация

1. Скопируйте `.env.example` в `.env`:
```bash
cp .env.example .env
```

2. Отредактируйте `.env`:
```env
DATABASE_URL=postgresql://yartumba_user:your_password@localhost:5432/yartumba
```

## Установка зависимостей

```bash
pip install psycopg2-binary
```

## Миграции (Alembic)

```bash
# Инициализировать Alembic (если ещё не сделано)
alembic init alembic

# Создать миграцию
alembic revision --autogenerate -m "Initial migration"

# Применить миграции
alembic upgrade head
```

## Запуск приложения

```bash
uvicorn app.main:app --reload
```
