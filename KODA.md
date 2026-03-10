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
├── models/
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
│   │   ├── bookshelf_part.py
│   │   ├── nightstand.py
│   │   ├── nightstand_part.py
│   │   ├── dresser.py
│   │   └── dresser_part.py
│   ├── components/       # Компоненты
│   │   └── drawer.py     # Универсальные ящики
│   └── materials/        # Материалы и фурнитура
│       ├── sheet_materials.py
│       ├── hardware.py
│       ├── edge.py
│       └── supports.py
├── api/                  # API эндпоинты
├── services/             # Бизнес-логика
└── core/                 # База, конфиг, DI
```

---

## Важные правила

1. **Не использовать старые `*Material` классы** — удалены в пользу единой системы материалов
2. **FurnitureMaterial** — универсальная связь, ссылается на все типы материалов
3. **EdgeMaterial** имеет уникальный `sheet_material_id` (связь 1:1)
4. **Товары** (Bookshelf, Nightstand, Dresser) имеют backref `product` на Product
5. **Drawer** — универсальный ящик, связь через `furniture_type` + `furniture_id`
6. **Ящики и детали** имеют ForeignKey с `ondelete="CASCADE"`

---

## Связи между таблицами

| Родитель | Потомок | Тип связи |
|----------|---------|-----------|
| `Product` | `Bookshelf/Nightstand/Dresser` | 1:1 (FK) |
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
