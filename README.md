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
- **Frontend:** (в разработке)

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
└── KODA.md              # Контекст для AI-ассистента
```

## 🔌 API Endpoints

### Каталог
- `GET /api/v1/categories` — список категорий
- `GET /api/v1/products` — товары каталога
- `GET /api/v1/products/{id}` — карточка товара

### Конфигуратор
- `POST /api/v1/configurator/bookshelf` — создать полку
- `POST /api/v1/configurator/nightstand` — создать тумбу
- `POST /api/v1/configurator/dresser` — создать комод
- `PUT /api/v1/configurator/{id}/materials` — изменить материалы
- `GET /api/v1/configurator/{id}/price` — получить цену

### Материалы
- `GET /api/v1/materials/sheet` — листовые материалы
- `GET /api/v1/materials/edges` — кромка
- `GET /api/v1/materials/hardware` — фурнитура

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

*Yartumba — создавай мебель своей мечты* 🪵
