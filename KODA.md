# KODA — Контекст проекта Yartumba

## О проекте

Мебельная конфигураторная система. Позволяет создавать мебель (книжные полки, тумбы, комоды) с выбором материалов и фурнитуры.

---

## Структура БД

### Основные таблицы

| Таблица | Описание |
|---------|----------|
| `categories` | Категории товаров |
| `products` | Товары в каталоге |
| `bookshelves` | Книжные полки |
| `bookshelf_parts` | Детали полок (боковины, полки, задняя стенка) |
| `nightstands` | Прикроватные тумбы |
| `nightstand_parts` | Детали тумб (боковины, полки, фасады) |
| `dressers` | Комоды |
| `dresser_parts` | Детали комодов (боковины, полки, фасады) |
| `drawers` | Универсальные выдвижные ящики |

### Поля изображений

Во всех моделях добавлено опциональное поле `image_url` (String 500). Если не задано — URL формируется автоматически по шаблону из `app/core/image_config.py`.

| Таблица | Папка изображений |
|---------|-------------------|
| `categories` | `/images/ui/` |
| `products` | `/images/products/` |
| `bookshelves` | `/images/products/bookshelf/` |
| `nightstands` | `/images/products/nightstand/` |
| `dressers` | `/images/products/dresser/` |
| `sheet_materials` | `/images/materials/sheet/` |
| `edge_materials` | `/images/materials/edge/` |
| `slide_guides` | `/images/hardware/slide_guides/` |
| `hinges` | `/images/hardware/hinges/` |
| `supports` | `/images/hardware/supports/` |
| `wall_mounts` | `/images/hardware/wall_mounts/` |

### Материалы (пакет `app/models/materials/`)

| Таблица | Описание |
|---------|----------|
| `sheet_materials` | Листовые материалы (ДСП, МДФ, ЛДСП, фанера, массив). Включает декор, цену, размеры листа |
| `edge_materials` | Кромка. Связь 1:1 с `sheet_materials` |
| `slide_guides` | Направляющие для ящиков |
| `hinges` | Петли для фасадов |
| `supports` | Опоры/ножки |
| `wall_mounts` | Крепления для подвесной мебели |

### Связь материалов с изделиями

| Таблица | Описание |
|---------|----------|
| `furniture_materials` | Универсальная связь материала с изделием. Содержит `furniture_type` (bookshelf/nightstand/dresser) и `furniture_id`. Поля: `sheet_material_id`, `edge_id`, `slide_guide_id`, `hinge_id`, `support_id`, `wall_mount_id`, `quantity` |

### Корзина

| Таблица | Описание |
|---------|----------|
| `carts` | Корзины пользователей (одна на пользователя или сессию) |
| `cart_items` | Позиции корзины с JSONB конфигурацией товаров |

---

## Модели Python

### Импорты

```python
# Каталог
from app.models.catalog import (
    Category, Product,
    AttributeType, SizeUnit,
    Attribute, AttributeValue,
    ProductAttribute,
    ProductConfiguration, ConfigurationItem,
    FurnitureMaterial,
)

# Товары
from app.models.goods import (
    Bookshelf, BookshelfPart,
    Nightstand, NightstandPart,
    Dresser, DresserPart,
)

# Компоненты
from app.models.components import Drawer

# Материалы
from app.models.materials import (
    SheetMaterial,
    SlideGuide, Hinge,
    EdgeMaterial,
    Support, WallMount,
)

# Корзина
from app.models.cart import Cart, CartItem
```

---

## Архитектура

```
app/
├── __init__.py           # Главный экспорт моделей
├── main.py               # Приложение FastAPI
├── models/               # Модели БД
│   ├── __init__.py       # Экспорт всех моделей
│   ├── catalog/          # Каталог (товары, атрибуты)
│   │   ├── category.py
│   │   ├── product.py
│   │   ├── attribute.py
│   │   ├── attribute_type.py
│   │   ├── product_attribute.py
│   │   ├── product_configuration.py
│   │   └── material.py   # FurnitureMaterial
│   ├── goods/            # Мебель
│   │   ├── bookshelf.py
│   │   ├── nightstand.py
│   │   └── dresser.py
│   ├── components/       # Компоненты
│   │   └── drawer.py     # Универсальные ящики
│   ├── materials/        # Материалы и фурнитура
│   │   ├── sheet_materials.py
│   │   ├── hardware.py
│   │   ├── edge.py
│   │   └── supports.py
│   └── cart.py           # Корзина (Cart, CartItem)
├── api/                  # API эндпоинты
│   └── v1/
│       ├── router.py     # Главный роутер v1
│       ├── configurator.py  # Конфигуратор (GET /options, POST /validate, POST /calculate)
│       └── goods/
│           ├── router.py          # Объединение товаров
│           ├── dependencies.py    # get_db()
│           ├── bookshelf/
│           │   ├── routes.py      # CRUD эндпоинты
│           │   └── schemas.py     # Pydantic схемы
│           ├── nightstand/
│           │   ├── routes.py
│           │   └── schemas.py
│           ├── dresser/
│           │   ├── routes.py
│           │   └── schemas.py
│           └── cart/
│               ├── dependencies.py    # Зависимости корзины (get_optional_session_id, get_cart, get_cart_id)
│               ├── routes/            # Эндпоинты по HTTP методам (SRP)
│               │   ├── __init__.py
│               │   ├── get.py         # GET /goods/cart
│               │   ├── post.py        # POST /goods/cart/items
│               │   ├── patch.py       # PATCH /goods/cart/items/{item_id}
│               │   ├── delete.py      # DELETE /goods/cart/items/{item_id}, DELETE /goods/cart
│               │   └── merge.py       # POST /goods/cart/merge
│               └── schemas.py         # Pydantic схемы корзины
├── services/             # Бизнес-логика
│   ├── configurator/         # Конфигуратор (рефакторинг 2025)
│   │   ├── __init__.py
│   │   ├── configurator_service.py  # Главный сервис (оркестрация)
│   │   ├── validators.py            # Валидаторы по типам мебели
│   │   ├── calculators/             # Калькуляторы стоимости
│   │   │   ├── furniture_calculator.py  # Универсальный калькулятор (общая логика)
│   │   │   ├── nightstand_calculator.py
│   │   │   ├── bookshelf_calculator.py
│   │   │   ├── dresser_calculator.py
│   │   │   └── README.md          # Документация по расчётам
│   │   ├── material_options.py      # Получение материалов
│   │   ├── constants.py             # Константы (размеры, проценты)
│   │   └── schemas.py               # Pydantic схемы
│   ├── cart_service.py          # Логика корзины
│   └── image_service.py         # Генерация URL изображений
└── core/                 # База, конфиг, DI
    ├── db_setup.py       # SQLAlchemy engine, SessionLocal, Base
    ├── config.py         # Конфигурация
    ├── dependencies.py   # Общий get_db()
    └── image_config.py   # Пути к frontend/public/images/
```

**PostgreSQL:**
- `.env.example` — пример конфигурации
- `POSTGRES_SETUP.md` — инструкция по настройке
- `DATABASE_URL` читается из переменных окружения

---

## API Endpoints

### Bookshelf (книжные полки)

| Метод | Путь | Описание |
|-------|------|----------|
| `POST` | `/v1/goods/bookshelf/` | Создать полку |
| `GET` | `/v1/goods/bookshelf/` | Список полок |
| `GET` | `/v1/goods/bookshelf/{id}` | Получить полку |
| `GET` | `/v1/goods/bookshelf/{id}/full` | Полка + детали |
| `PATCH` | `/v1/goods/bookshelf/{id}` | Обновить полку |
| `DELETE` | `/v1/goods/bookshelf/{id}` | Удалить полку |
| `POST` | `/v1/goods/bookshelf/{id}/parts` | Добавить деталь |
| `GET` | `/v1/goods/bookshelf/{id}/parts` | Список деталей |
| `GET` | `/v1/goods/bookshelf/{id}/parts/{part_id}` | Деталь по ID |
| `PATCH` | `/v1/goods/bookshelf/{id}/parts/{part_id}` | Обновить деталь |
| `DELETE` | `/v1/goods/bookshelf/{id}/parts/{part_id}` | Удалить деталь |

### Nightstand (прикроватные тумбы)

| Метод | Путь | Описание |
|-------|------|----------|
| `POST` | `/v1/goods/nightstand/` | Создать тумбу |
| `GET` | `/v1/goods/nightstand/` | Список тумб |
| `GET` | `/v1/goods/nightstand/{id}` | Получить тумбу |
| `GET` | `/v1/goods/nightstand/{id}/full` | Тумба + детали |
| `PATCH` | `/v1/goods/nightstand/{id}` | Обновить тумбу |
| `DELETE` | `/v1/goods/nightstand/{id}` | Удалить тумбу |
| `POST` | `/v1/goods/nightstand/{id}/parts` | Добавить деталь |
| `GET` | `/v1/goods/nightstand/{id}/parts` | Список деталей |
| `GET` | `/v1/goods/nightstand/{id}/parts/{part_id}` | Деталь по ID |
| `PATCH` | `/v1/goods/nightstand/{id}/parts/{part_id}` | Обновить деталь |
| `DELETE` | `/v1/goods/nightstand/{id}/parts/{part_id}` | Удалить деталь |

### Dresser (комоды)

| Метод | Путь | Описание |
|-------|------|----------|
| `POST` | `/v1/goods/dresser/` | Создать комод |
| `GET` | `/v1/goods/dresser/` | Список комодов |
| `GET` | `/v1/goods/dresser/{id}` | Получить комод |
| `GET` | `/v1/goods/dresser/{id}/full` | Комод + детали |
| `PATCH` | `/v1/goods/dresser/{id}` | Обновить комод |
| `DELETE` | `/v1/goods/dresser/{id}` | Удалить комод |
| `POST` | `/v1/goods/dresser/{id}/parts` | Добавить деталь |
| `GET` | `/v1/goods/dresser/{id}/parts` | Список деталей |
| `GET` | `/v1/goods/dresser/{id}/parts/{part_id}` | Деталь по ID |
| `PATCH` | `/v1/goods/dresser/{id}/parts/{part_id}` | Обновить деталь |
| `DELETE` | `/v1/goods/dresser/{id}/parts/{part_id}` | Удалить деталь |

### Configurator (конфигуратор)

| Метод | Путь | Описание |
|-------|------|----------|
| `GET` | `/v1/configurator/options` | Получить все материалы и фурнитуру |
| `POST` | `/v1/configurator/validate` | Валидация конфигурации |
| `POST` | `/v1/configurator/calculate` | Расчёт стоимости (nightstand) |

### Cart (корзина)

| Метод | Путь | Описание |
|-------|------|----------|
| `GET` | `/v1/goods/cart` | Получить корзину |
| `POST` | `/v1/goods/cart/items` | Добавить товар в корзину |
| `PATCH` | `/v1/goods/cart/items/{item_id}` | Обновить количество товара |
| `DELETE` | `/v1/goods/cart/items/{item_id}` | Удалить товар из корзины |
| `DELETE` | `/v1/goods/cart` | Очистить корзину |
| `POST` | `/v1/goods/cart/merge` | Объединить корзины (session → user) |

---

## Важные правила

1. **Не использовать старые `*Material` классы** — удалены в пользу единой системы материалов
2. **FurnitureMaterial** — универсальная связь, ссылается на все типы материалов
3. **EdgeMaterial** имеет уникальный `sheet_material_id` (связь 1:1)
4. **Товары** (Bookshelf, Nightstand, Dresser) имеют backref `product` на Product
5. **Drawer** — универсальный ящик, связь через `furniture_type` + `furniture_id`
6. **Ящики и детали** имеют ForeignKey с `ondelete="CASCADE"`
7. **Общие схемы** — `GoodsBase`, `GoodsCreate`, `GoodsUpdate`, `GoodsResponse` вынесены в `bookshelf/schemas.py` и импортируются в Nightstand и Dresser
8. **Документация** — доступна по `/docs` (Swagger) и `/redoc` (ReDoc)
9. **CartItem** — использует JSONB для конфигурации, FK на products и furniture_id для конкретной мебели
10. **Pydantic схемы корзины** — созданы по принципу SRP: CartBase, CartCreate, CartUpdate, CartResponse, CartItemBase, CartItemCreate, CartItemUpdate, CartItemResponse
11. **Конфигуратор** — рефакторинг 2025: полный переход на новый API в `app/services/configurator/`
12. **Использование конфигуратора:**
    ```python
    from app.services.configurator import create_configurator_service

    service = create_configurator_service(db)
    cost = service.calculate("nightstand", config)
    validation = service.validate("bookshelf", config)
    options = service.get_material_options()
    ```
13. **Изображения** — все модели имеют опциональное поле `image_url`. Если не задано, URL формируется автоматически через `app.services.image_service` на основе `app.core.image_config`.
14. **Статика изображений** — nginx раздаёт `/images/` из `frontend/public/images/`. Папки: `materials/`, `hardware/`, `products/`, `configurator/`, `ui/`, `uploads/`.

---

## Связи между таблицами

| Родитель | Потомок | Тип связи |
|----------|---------|-----------|
| `Product` | `Bookshelf/Nightstand/Dresser` | 1:1 (FK) |
| `Category` | `Product` | 1:n |
| `Bookshelf` | `BookshelfPart` | 1:n (CASCADE) |
| `Nightstand` | `NightstandPart` | 1:n (CASCADE) |
| `Dresser` | `DresserPart` | 1:n (CASCADE) |
| `SheetMaterial` | `EdgeMaterial` | 1:1 (unique) |
| `SheetMaterial` | `BookshelfPart/NightstandPart/DresserPart` | 1:n |
| `Drawer` | `SlideGuide` | many:1 |
| `FurnitureMaterial` | `SheetMaterial` | many:1 |
| `FurnitureMaterial` | `EdgeMaterial` | many:1 |
| `FurnitureMaterial` | `SlideGuide` | many:1 |
| `FurnitureMaterial` | `Hinge` | many:1 |
| `FurnitureMaterial` | `Support` | many:1 |
| `FurnitureMaterial` | `WallMount` | many:1 |
| `Cart` | `CartItem` | 1:n (CASCADE) |
| `Product` | `CartItem` | 1:n |

---

## Типы материалов (material_type в sheet_materials)

- `chipboard` — ДСП
- `ldsp` — ЛДСП
- `mdf` — МДФ
- `hdf` — ХДФ
- `plywood` — Фанера
- `solid_wood` — Массив

---

## Типы изделий (furniture_type)

**В FurnitureMaterial:**
- `bookshelf` — Книжная полка
- `nightstand` — Прикроватная тумба
- `dresser` — Комод

**В Drawer:**
- `nightstand` — Прикроватная тумба
- `dresser` — Комод

---

## Части изделий (part_type в furniture_materials)

- `body` — Корпус
- `shelf` — Полка
- `facade` — Фасад
- `top` — Столешница
- `legs` — Ножки
- `back` — Задняя стенка
- `drawer` — Ящик

---

## Конфигуратор (рефакторинг 2025)

### Архитектура

Монолитный сервис `app/services/configurator_service.py` (200+ строк) был разбит на модули по принципу разделения ответственности (SOLID):

```
app/services/configurator/
├── __init__.py                     # Экспорт главного сервиса
├── configurator_service.py         # Главный сервис (оркестрация)
├── validators.py                   # Валидация конфигураций
├── material_options.py             # Получение списка материалов
├── constants.py                    # Константы (размеры, проценты)
├── schemas.py                      # Pydantic схемы для конфигураций
└── calculators/
    ├── __init__.py                 # Фабрика калькуляторов
    ├── furniture_calculator.py          # Базовый класс для расчётов
    ├── nightstand_calculator.py    # Расчёт тумбы
    ├── bookshelf_calculator.py     # Расчёт полки
    ├── dresser_calculator.py       # Расчёт комода
    └── README.md                   # Документация по расчётам
```

### Принципы SOLID

**SRP** — каждый класс отвечает за одну задачу:
- `ConfiguratorService` — оркестрация (валидация + расчёт)
- `NightstandValidator/BookshelfValidator/DresserValidator` — валидация
- `NightstandCalculator/BookshelfCalculator/DresserCalculator` — расчёт стоимости
- `get_material_options` — получение материалов

**OCP** — добавление нового типа мебели:
1. Создать `new_furniture_calculator.py` наследуя `FurnitureCostCalculator`
2. Создать `NewFurnitureValidator` наследуя `BaseValidator`
3. Добавить в фабрики в `calculators/__init__.py` и `validators.py`

**LSP** — все калькуляторы и валидаторы заменяемы через базовые классы.

**ISP** — минимальные интерфейсы:
- `FurnitureCostCalculator` — только методы расчёта
- `BaseValidator` — только метод валидации

**DIP** — инъекция зависимости через `db: Session`, фабрики создают объекты динамически.

### Использование

**Новый API:**
```python
from app.services.configurator import create_configurator_service
from sqlalchemy.orm import Session

# Создание сервиса
db: Session = SessionLocal()
service = create_configurator_service(db)

# Валидация
result = service.validate("nightstand", config)
if not result["valid"]:
    print("Errors:", result["errors"])

# Расчёт стоимости
cost = service.calculate("nightstand", config)
print(f"Total: {cost['total_price']} руб.")
print(f"Materials: {cost['materials_cost']} руб.")
print(f"Hardware: {cost['hardware_cost']} руб.")
print(f"Work: {cost['work_cost']} руб.")

# Получение материалов
options = service.get_material_options()
sheet_materials = options["sheet_materials"]
```

**Фабрики:**
```python
# Валидатор
from app.services.configurator.validators import get_validator

validator = get_validator("nightstand")
result = validator.validate(config)

# Калькулятор
from app.services.configurator.calculators import get_calculator

calculator = get_calculator("bookshelf", db)
cost = calculator.calculate(config)
```

**Константы:**
```python
from app.services.configurator.constants import DIMENSION_LIMITS, WORK_COST_MULTIPLIER

limits = DIMENSION_LIMITS["nightstand"]
print(f"Width: {limits['width']['min']} - {limits['width']['max']} мм")
```

**Pydantic схемы:**
```python
from app.services.configurator.schemas import NightstandConfig, CostBreakdown

config = NightstandConfig(width=500, height=500, depth=400)
cost = CostBreakdown(**cost_dict)
```

**BOM (Bill of Materials):**

BOM формируется отдельно при оформлении и оплате заказа, а не на этапе расчёта стоимости.

```python
from app.services.configurator import BOM, Part, HardwareItem
from app.services.configurator.calculators.furniture_calculator import FurnitureCostCalculator

# Получение BOM через калькулятор (после оплаты заказа)
calculator = get_calculator("nightstand", db)
parts = calculator.generate_parts_list(width=500, height=600, depth=400, ...)
edges = calculator.generate_edge_list(parts)
bom = calculator.generate_bom(
    furniture_type="nightstand",
    parts=parts,
    edges=edges,
    hardware_items=[...]
)

# Экспорт в JSON для производства
json_output = bom.to_production_json()

# Структура BOM:
# - sheet_materials: детали с размерами и кромкой
# - edge_materials: список отрезков кромки по длинам
# - hardware: фурнитура с ценами
# - total_sheet_area_m2: общая площадь материалов
# - estimated_sheets: количество листов для раскроя
```

---

## Тестирование

### Бэкенд

**Структура:**
```
tests/
├── catalog/              # Тесты каталога
│   └── test_catalog.py
├── components/           # Тесты компонентов
│   └── test_drawer.py
├── goods/                # Тесты товаров (модели)
│   ├── test_bookshelf.py
│   ├── test_dresser.py
│   └── test_nightstand.py
├── integration/          # Интеграционные тесты
│   ├── placeholder/      # Заглушки (skip)
│   │   └── test_configurator_placeholder.py
│   ├── configurator_conftest.py
│   ├── test_cart_integration.py
│   ├── test_configurator_validation.py
│   ├── test_configurator_calculation.py
│   └── test_configurator_performance.py
├── materials/            # Тесты материалов
│   └── test_materials.py
├── schemas/              # Тесты Pydantic схем
│   ├── test_bookshelf_schema.py
│   ├── test_dresser_schema.py
│   ├── test_nightstand_schema.py
│   ├── test_part_schema.py
│   ├── test_cart_item.py
│   └── test_cart_schemas.py
├── conftest.py           # Глобальные фикстуры
└── pytest.ini
```

**Запуск:**
```bash
python3 -m pytest tests/ -v
python3 -m pytest tests/ -v --coverage
```

**Статистика:**
- **176 тестов проходят** ✅

### Фронтенд

**Статистика фронтенд тестов:**
- 113 unit тестов утилит проходят ✅
- 148 API тестов (client, endpoints, services) проходят ✅
- 200 тестов сторов (UI, Cart, Configurator) проходят ✅
- 36 тестов кастомных хуков проходят ✅
- **Всего: 497 тестов** ✅

---

## PostgreSQL

**Настройка:**
1. Создать `.env` из `.env.example`:
```bash
cp .env.example .env
```

2. Отредактировать `DATABASE_URL`:
```env
DATABASE_URL=postgresql://username:password@localhost:5432/yartumba
```

3. Установить зависимости:
```bash
pip install psycopg2-binary
```

4. Запустить миграции Alembic:
```bash
alembic upgrade head
```

**Миграции:**
```bash
# Создание новой миграции
alembic revision --autogenerate -m "description"

# Применение миграций
alembic upgrade head

# Откат миграции
alembic downgrade -1
```

---

## Фронтенд Архитектура

```
frontend/src/
├── main.jsx                  # Точка входа (с BrowserRouter)
├── App.jsx                   # Главный компонент (с CatalogProvider)
├── core/
│   ├── styles/
│   │   └── global.css        # Глобальные стили
│   ├── types/
│   │   ├── catalog.types.ts  # Типы каталога
│   │   ├── common.types.ts   # Общие типы (UUID)
│   │   └── api.types.ts      # API типы
│   ├── constants/
│   │   ├── product.constants.ts  # Типы мебели, иконки
│   │   └── configurator.constants.ts
│   └── config/
│       ├── routes.config.ts  # Маршруты (ROUTES)
│       └── app.config.ts
├── api/
│   ├── client.ts             # HTTP клиент
│   ├── endpoints/            # Эндпоинты API
│   └── services/
│       ├── catalog.service.ts    # API каталога
│       ├── cart.service.ts       # API корзины
│       └── configurator.service.ts
├── stores/
│   ├── catalog/
│   │   ├── catalog.store.ts      # React hook с состоянием
│   │   ├── catalog.context.tsx   # React Context для каталога
│   │   └── index.ts              # Экспорт (CatalogProvider, useCatalog)
│   ├── cart/                 # Корзина (MobX)
│   ├── configurator/         # Конфигуратор (MobX)
│   └── ui/                   # UI сторы (MobX)
├── components/
│   ├── catalog/
│   │   ├── ProductCard.jsx       # Карточка товара
│   │   ├── ProductFilters.jsx    # Фильтры
│   │   ├── ProductList.jsx       # Список товаров
│   │   └── ProductSkeleton.jsx   # Загрузка
│   ├── common/               # Общие компоненты
│   └── ui/                   # UI Kit
├── pages/
│   ├── catalog/
│   │   └── CatalogPage.jsx       # Страница каталога
│   ├── configurator/
│   │   └── ConfiguratorPage.jsx  # Страница конфигуратора
│   ├── cart/
│   │   └── CartPage.jsx          # Корзина
│   └── auth/
│       ├── LoginPage.jsx
│       └── RegisterPage.jsx
└── routes/
    └── AppRoutes.jsx         # Роутер (Routes, Route)
```

**Frontend зависимости:**
- `react-router-dom` — роутинг
- `mobx` + `mobx-react-lite` — управление состоянием (MobX для сложных стор)
- `axios` — HTTP запросы

**Управление состоянием:**
- **Каталог** — React Context + useState (простое состояние)
- **Корзина** — MobX (сложная логика, асинхронность)
- **Конфигуратор** — MobX (сложные вычисления)
- **UI** — MobX (модальные окна, уведомления)

---

## Статус проекта

| Компонент | Статус |
|-----------|--------|
| Модели БД | ✅ Готово |
| API Routes (CRUD) | ✅ Готово |
| Конфигуратор | ✅ Готово |
| Корзина | ✅ API + Frontend готово |
| Заказы | ⏸️ Не реализовано |
| Авторизация | ⏸️ Не реализовано |
| Фронтенд (каталог) | ✅ Готово |
| Фронтенд (конфигуратор) | 🟡 Заглушка |
| Фронтенд (корзина) | ✅ Готово (MobX + API) |
| Тесты бэкенда | ✅ 176 тестов |
| Тесты фронтенда | ✅ 497 тестов |

**Общий прогресс:** ~65-70%

---

*Yartumba — создавай мебель своей мечты* 🪵
