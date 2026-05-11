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

**Статистика:** 176 тестов проходят ✅

### Frontend

```bash
cd frontend

# Запуск всех тестов
npm run test

# Режим наблюдения
npm run test:watch

# Отчёт покрытия
npm run test:coverage

# Только API тесты
npm run test tests/unit/api/

# Только тесты утилит
npm run test tests/unit/core/utils/
```

**Статистика:**
- 113 unit тестов утилит проходят ✅
- 148 API тестов (client, endpoints, services) проходят ✅
- 200 тестов сторов (UI, Cart, Configurator) проходят ✅
- **Всего:** 497 тестов ✅

## 🚀 Быстрый старт

```bash
# Клонирование репозитория
git clone https://github.com/nikolaevilya82/Yartumba.git
cd Yartumba

# Установка зависимостей
pip install -r requirements.txt

# Создание .env файла
cp .env.example .env

# Настройка DATABASE_URL в .env
# DATABASE_URL=postgresql://username:password@localhost:5432/yartumba

# Запуск миграций
alembic upgrade head

# Запуск сервера
uvicorn main:app --reload
```

## 🗄️ Миграции Alembic

```bash
# Создание новой миграции
alembic revision --autogenerate -m "description"

# Применение миграций
alembic upgrade head

# Откат миграции
alembic downgrade -1

# Текущая версия
alembic current
```

**Текущие миграции:**
- `001_update_cart_item_with_jsonb_and_product_fk` — обновление модели корзины (JSONB, FK на products, furniture_id)

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
│       ├── unit/
│       │   ├── core/
│       │   │   └── utils/      # Unit тесты утилит (113 тестов)
│       │   ├── api/            # API тесты (148 тестов)
│       │   │   ├── client.test.ts
│       │   │   ├── endpoints/
│       │   │   └── services/
│       │   ├── stores/         # Тесты сторов (200 тестов)
│       │   │   ├── ui/
│       │   │   ├── cart/
│       │   │   └── configurator/
│       │   └── hooks/          # Тесты хуков (36 тестов)
│       │       ├── useDebounce.test.ts
│       │       ├── useLocalStorage.test.ts
│       │       ├── useMediaQuery.test.ts
│       │       ├── useCart.test.ts
│       │       └── useConfigurator.test.ts
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
| Корзина | 🟡 Модель готова |
| Заказы | ⏸️ Не реализовано |
| Авторизация | ⏸️ Не реализовано |
| Фронтенд (структура) | 🟡 В разработке |
| Тесты бэкенда | ✅ 176 тестов |
| Тесты фронтенда | ✅ 461 тест |

**Общий прогресс:** ~60-70%

---

## 🛒 Модель корзины

### Структура CartItem

| Поле | Тип | Описание |
|------|-----|----------|
| `id` | UUID | Уникальный ID позиции |
| `cart_id` | UUID | Ссылка на корзину |
| `product_id` | UUID | FK на products (каталог) |
| `product_type` | String | bookshelf, nightstand, dresser |
| `furniture_id` | UUID | ID конкретной мебели |
| `configuration` | JSONB | Конфигурация товара |
| `quantity` | Integer | Количество |
| `unit_price` | Numeric(10,2) | Цена за единицу |
| `total_price` | Numeric(10,2) | Итоговая цена |
| `materials_snapshot` | JSONB | Снепшот материалов |
| `created_at` | DateTime | Дата создания |
| `updated_at` | DateTime | Дата обновления |

### Структура configuration по типам

**Bookshelf:**
```json
{
  "dimensions": {"width": 800, "height": 1800, "depth": 300},
  "parts": [
    {"type": "side_panel", "material_id": "uuid", "quantity": 2},
    {"type": "shelf", "material_id": "uuid", "quantity": 4}
  ],
  "back_panel": {"material_id": "uuid", "thickness": 8}
}
```

**Nightstand:**
```json
{
  "dimensions": {"width": 500, "height": 450, "depth": 400},
  "parts": [{"type": "side_panel", "material_id": "uuid", "quantity": 2}],
  "drawers": [
    {"drawer_id": "uuid", "slide_guide_id": "uuid", "facade_material_id": "uuid"}
  ],
  "facade_material_id": "uuid"
}
```

**Dresser:**
```json
{
  "dimensions": {"width": 1200, "height": 800, "depth": 500},
  "parts": [...],
  "drawers": [...],
  "top_material_id": "uuid",
  "hinge_id": "uuid"
}
```

### Методы CartItem

```python
# Получить объект мебели
furniture = cart_item.get_furniture_object(db)

# Пересчитать цену на основе текущих материалов
new_price = cart_item.recalculate_price(db)
```

### Pydantic схемы корзины

**По принципу SRP:**

| Схема | Назначение |
|-------|-----------|
| `CartBase` | Базовые поля (`user_id`, `session_id`) |
| `CartCreate` | Создание корзины |
| `CartUpdate` | Обновление корзины |
| `CartResponse` | Полный ответ корзины |
| `CartItemBase` | Базовые поля позиции |
| `CartItemCreate` | Создание позиции (валидация furniture_type, quantity 1-99) |
| `CartItemUpdate` | Обновление позиции |
| `CartItemResponse` | Полный ответ позиции |
| `CartSummary` | Краткое резюме |

**Вычисляемые поля:**
- `CartResponse.items_count` — общее количество товаров
- `CartResponse.subtotal` — итоговая сумма
- `CartItemResponse.item_total` — сумма позиции (quantity × unit_price)

**Валидация:**
- `furniture_type`: только `bookshelf`, `nightstand`, `dresser`
- `quantity`: от 1 до 99
- `unit_price`: `Decimal >= 0`

---

*Yartumba — создавай мебель своей мечты* 🪵
