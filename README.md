# 🪑 Yartumba

> Мебельная конфигураторная система нового поколения

![Python](https://img.shields.io/badge/Python-3.11+-blue?style=flat-square)
![FastAPI](https://img.shields.io/badge/FastAPI-0.109+-green?style=flat-square)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-15+-blue?style=flat-square)
![License](https://img.shields.io/badge/License-MIT-yellow?style=flat-square)

## ✨ Особенности

- 🧩 **Конфигуратор мебели** — создавай мебель под свои нужды
- 🎨 **Выбор материалов** — более 50+ декоров и текстур
- 📐 **Настройка размеров** — любые габариты с точностью до миллиметра
- 🔧 **Наполнение** — выбор фурнитуры, направляющих, петель
- 💰 **Авторасчёт цены** — мгновенный пересчёт при изменении параметров

## 🏠 Поддерживаемая мебель

| Тип | Описание |
|-----|----------|
| 📚 **Книжные полки** | Открытые, закрытые, комбинированные |
| 🛏️ **Прикроватные тумбы** | С ящиками, с полкой, на ножках |
| 🗄️ **Комоды** | Стандартные, с зеркалом, угловые |

## 🛠️ Технологический стек

- **Backend:** Python 3.11+, FastAPI, SQLAlchemy, Pydantic
- **Database:** PostgreSQL 15+, Alembic (миграции)
- **Frontend:** React 18+, Vite, TypeScript
- **Testing:** 
  - Backend: pytest, pytest-asyncio, coverage
  - Frontend: Vitest, @testing-library/react, MSW

## 🧪 Тестирование

### Backend

```bash
# Запуск всех тестов
python3 -m pytest tests/ -v

# Запуск с покрытием
python3 -m pytest tests/ -v --coverage

# Только unit тесты
python3 -m pytest tests/goods/ tests/catalog/ tests/components/ -v
```

**Статистика:** 130 тестов проходят ✅

### Frontend

```bash
cd frontend

# Запуск всех тестов
npm run test

# Режим наблюдения
npm run test:watch

# Отчёт покрытия
npm run test:coverage
```

**Статистика:** 113 unit тестов проходят ✅

## 🚀 Быстрый старт

```bash
# Клонирование репозитория
git clone https://github.com/nikolaevilya82/Yartumba.git
cd Yartumba

# Установка зависимостей
pip install -r requirements.txt

# Запуск миграций
alembic upgrade head

# Запуск сервера
uvicorn main:app --reload
```

## 📁 Структура проекта

```
Yartumba/
├── app/
│   ├── models/           # Модели БД
│   │   ├── catalog/      # Каталог, товары, атрибуты
│   │   ├── goods/        # Мебель (полки, тумбы, комоды)
│   │   └── materials/    # Материалы и фурнитура
│   ├── api/              # API эндпоинты
│   ├── services/         # Бизнес-логика
│   └── core/             # Конфигурация, база, DI
├── migrations/           # Миграции Alembic
├── tests/                # Тесты
│   ├── catalog/          # Тесты каталога
│   ├── goods/            # Тесты товаров
│   ├── components/       # Тесты компонентов
│   ├── materials/        # Тесты материалов
│   ├── schemas/          # Тесты Pydantic схем
│   └── integration/      # Интеграционные тесты
├── frontend/             # React приложение
│   ├── src/
│   │   ├── core/         # Ядро (конфиги, типы, утилиты)
│   │   ├── api/          # API клиент и сервисы
│   │   ├── components/   # Компоненты
│   │   └── modules/      # Модули (каталог, корзина)
│   └── tests/            # Тесты фронтенда
│       └── unit/core/utils/  # Unit тесты утилит
├── KODA.md              # Контекст для AI-ассистента
└── README.md            # Документация проекта
```

## 🔌 API Endpoints

### Товары (CRUD)

**Книжные полки:**
- `POST /v1/goods/bookshelf/` — создать полку
- `GET /v1/goods/bookshelf/` — список полок
- `GET /v1/goods/bookshelf/{id}` — получить полку
- `GET /v1/goods/bookshelf/{id}/full` — полка + детали
- `PATCH /v1/goods/bookshelf/{id}` — обновить полку
- `DELETE /v1/goods/bookshelf/{id}` — удалить полку
- `POST /v1/goods/bookshelf/{id}/parts` — добавить деталь
- `GET /v1/goods/bookshelf/{id}/parts` — список деталей
- `PATCH /v1/goods/bookshelf/{id}/parts/{part_id}` — обновить деталь
- `DELETE /v1/goods/bookshelf/{id}/parts/{part_id}` — удалить деталь

**Прикроватные тумбы:**
- `POST /v1/goods/nightstand/` — создать тумбу
- `GET /v1/goods/nightstand/` — список тумб
- `GET /v1/goods/nightstand/{id}/full` — тумба + детали
- `PATCH /v1/goods/nightstand/{id}` — обновить тумбу
- `DELETE /v1/goods/nightstand/{id}` — удалить тумбу

**Комоды:**
- `POST /v1/goods/dresser/` — создать комод
- `GET /v1/goods/dresser/` — список комодов
- `GET /v1/goods/dresser/{id}/full` — комод + детали
- `PATCH /v1/goods/dresser/{id}` — обновить комод
- `DELETE /v1/goods/dresser/{id}` — удалить комод

### Конфигуратор
- `GET /v1/configurator/options` — получить материалы и фурнитуру
- `POST /v1/configurator/validate` — валидация конфигурации
- `POST /v1/configurator/calculate` — расчёт стоимости

### Каталог
- `GET /v1/categories` — список категорий
- `GET /v1/products` — товары каталога
- `GET /v1/products/{id}` — карточка товара

### Материалы
- `GET /v1/materials/sheet` — листовые материалы
- `GET /v1/materials/edges` — кромка
- `GET /v1/materials/hardware` — фурнитура

## 🎨 Пример использования

```python
from app.models.goods import Bookshelf
from app.models.materials import SheetMaterial, FurnitureMaterial

# Создаём полку
bookshelf = Bookshelf(
    width=1200,
    height=2000,
    depth=400,
    shelf_count=5,
    shelf_type="closed"
)

# Назначаем материал
material = FurnitureMaterial(
    furniture_type="bookshelf",
    furniture_id=bookshelf.id,
    part_type="body",
    sheet_material_id=sheet_mat.id,
    decor_id=decor.id
)
```

## 📄 Лицензия

MIT License — подробности в файле `LICENSE`

---

## 📊 Статус проекта

| Компонент | Статус |
|-----------|--------|
| Модели БД | ✅ Готово |
| API Routes (CRUD) | ✅ Готово |
| Конфигуратор | 🟡 В разработке |
| Корзина | ⏸️ Не реализовано |
| Заказы | ⏸️ Не реализовано |
| Авторизация | ⏸️ Не реализовано |
| Фронтенд (структура) | 🟡 В разработке |
| Тесты бэкенда | ✅ 130 тестов |
| Тесты фронтенда | ✅ 113 тестов |

**Общий прогресс:** ~55-65%

---

*Yartumba — создавай мебель своей мечты* 🪵
