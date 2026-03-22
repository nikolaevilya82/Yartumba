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
│   └── materials/        # Материалы и фурнитура
│       ├── sheet_materials.py
│       ├── hardware.py
│       ├── edge.py
│       └── supports.py
├── api/                  # API эндпоинты
│   └── v1/
│       ├── router.py     # Главный роутер v1
│       └── goods/
│           ├── router.py          # Объединение товаров
│           ├── dependencies.py    # get_db()
│           ├── bookshelf/
│           │   ├── routes.py      # CRUD эндпоинты
│           │   └── schemas.py     # Pydantic схемы
│           ├── nightstand/
│           │   ├── routes.py
│           │   └── schemas.py
│           └── dresser/
│               ├── routes.py
│               └── schemas.py
├── services/             # Бизнес-логика
└── core/                 # База, конфиг, DI
```

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

## Фронтенд (React + Vite)

### Структура

```
frontend/
├── src/
│   ├── core/               # Ядро (конфиги, типы, утилиты, константы)
│   │   ├── config/         # Конфигурация
│   │   │   ├── app.config.ts      # Настройки приложения
│   │   │   ├── api.config.ts      # URL API, эндпоинты
│   │   │   └── routes.config.ts   # Маршруты
│   │   ├── constants/      # Константы
│   │   │   ├── product.constants.ts      # Типы товаров, категории
│   │   │   ├── configurator.constants.ts # Опции конфигуратора
│   │   │   └── validation.constants.ts   # Валидация
│   │   ├── types/          # TypeScript типы
│   │   │   ├── product.types.ts        # Product, Furniture, Bookshelf...
│   │   │   ├── configurator.types.ts   # Опции, Configuration
│   │   │   ├── cart.types.ts           # Cart, CartItem, Order
│   │   │   └── api.types.ts            # ApiResponse, Pagination
│   │   ├── utils/          # Утилиты
│   │   │   ├── price.utils.ts      # Форматирование цен
│   │   │   ├── validation.utils.ts # Валидация форм
│   │   │   ├── storage.utils.ts    # localStorage
│   │   │   └── helpers.utils.ts    # Общие функции
│   │   ├── assets/         # Статика
│   │   ├── main.jsx        # Точка входа
│   │   └── index.css       # Глобальные стили
│   ├── api/                # API клиент и сервисы
│   │   ├── client.ts       # Базовый HTTP клиент (fetch)
│   │   ├── index.ts        # Главный экспорт
│   │   ├── endpoints/      # Эндпоинты API
│   │   │   ├── index.ts              # Ре-экспорт
│   │   │   ├── types/                # Типы эндпоинтов
│   │   │   ├── helpers/              # Утилиты для эндпоинтов
│   │   │   ├── common.endpoints.ts   # Категории, материалы
│   │   │   ├── configurator.endpoints.ts
│   │   │   ├── cart.endpoints.ts
│   │   │   ├── orders.endpoints.ts
│   │   │   └── products/             # Товары
│   │   │       ├── bookshelf.endpoints.ts
│   │   │       ├── nightstand.endpoints.ts
│   │   │       └── dresser.endpoints.ts
│   │   └── services/        # API сервисы
│   │       ├── bookshelf.service.ts
│   │       ├── nightstand.service.ts
│   │       ├── dresser.service.ts
│   │       ├── configurator.service.ts
│   │       ├── cart.service.ts
│   │       └── order.service.ts
│   ├── hooks/              # Глобальные кастомные хуки
│   ├── stores/             # Глобальное состояние
│   ├── components/         # Переиспользуемые компоненты
│   │   ├── ui/             # Базовые (Button, Input...)
│   │   └── common/         # Общие приложения
│   ├── modules/            # Функциональные модули
│   │   ├── catalog/        # Каталог
│   │   ├── bookshelf/      # Книжные полки
│   │   ├── nightstand/     # Тумбы
│   │   ├── dresser/        # Комоды
│   │   └── cart/           # Корзина
│   ├── layouts/            # Компоненты макетов
│   ├── pages/              # Страницы
│   │   ├── App.jsx         # Главный компонент
│   │   └── App.css         # Стили App
│   └── routes/             # Маршрутизация
├── public/                 # Публичные файлы
├── package.json            # Зависимости
└── vite.config.js          # Конфиг Vite
```

### Импорты из core

```typescript
// Конфиги
import { appConfig } from 'core/config/app.config';
import { apiConfig } from 'core/config/api.config';
import { routes, routeNames } from 'core/config/routes.config';

// Константы
import { 
  FurnitureType, 
  furnitureTypeNames,
  PartType,
  CategorySlug 
} from 'core/constants/product.constants';
import { 
  MaterialType, 
  materialTypeNames,
  configuratorDefaults 
} from 'core/constants/configurator.constants';

// Типы
import type { 
  Product, 
  Bookshelf, 
  Nightstand, 
  Dresser,
  FurniturePart 
} from 'core/types/product.types';
import type { 
  MaterialOption, 
  FurnitureConfiguration,
  ConfiguratorOptions 
} from 'core/types/configurator.types';
import type { 
  Cart, 
  CartItem, 
  Order 
} from 'core/types/cart.types';
import type { 
  ApiResponse, 
  PaginatedResponse,
  PaginationParams 
} from 'core/types/api.types';

// Утилиты
import { formatPrice, calculateDiscount } from 'core/utils/price.utils';
import { isValidEmail, combineValidators } from 'core/utils/validation.utils';
import { setItem, getItem, storageKeys } from 'core/utils/storage.utils';
import { generateId, formatDate, debounce, clamp } from 'core/utils/helpers.utils';
```

### Импорты из api

```typescript
// API клиент
import { apiClient, createApiClient } from 'api/client';

// Эндпоинты
import { 
  bookshelfEndpoints, 
  nightstandEndpoints, 
  dresserEndpoints,
  configuratorEndpoints, 
  cartEndpoints, 
  orderEndpoints,
  goodsEndpoints,
  queryParams 
} from 'api/endpoints';

// Сервисы товаров
import * as bookshelfService from 'api/services/bookshelf.service';
import * as nightstandService from 'api/services/nightstand.service';
import * as dresserService from 'api/services/dresser.service';

// Сервисы
import * as configuratorService from 'api/services/configurator.service';
import * as cartService from 'api/services/cart.service';
import * as orderService from 'api/services/order.service';
```

### Запуск

```bash
cd frontend
npm install
npm run dev      # Dev-сервер (http://localhost:5173)
npm run build    # Сборка в prod
npm run preview  # Превью prod-сборки
```

### Текущие товары на главной

| Товар | Тип | Цена |
|-------|-----|------|
| Книжная полка | bookshelf | 8 500 ₽ |
| Прикроватная тумба | nightstand | 5 200 ₽ |
| Комод | dresser | 12 500 ₽ |

### API для фронтенда

Бэкенд API: `http://localhost:8000`

- Bookshelf: `/v1/goods/bookshelf/`
- Nightstand: `/v1/goods/nightstand/`
- Dresser: `/v1/goods/dresser/`

Документация: `/docs`
