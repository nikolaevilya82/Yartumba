# Как добавить новый тип мебели

## Быстрый чеклист

| # | Файл | Что делать |
|---|------|------------|
| 1 | `app/models/goods/<product>.py` | Создать модель (по аналогии с `bookshelf.py`) |
| 2 | `app/models/goods/<product>_part.py` | Создать модель деталей |
| 3 | `app/models/goods/__init__.py` | Экспортировать модели |
| 4 | `app/models/__init__.py` | Добавить импорт модели |
| 5 | `app/models/materials/` | Добавить материалы если нужны |
| 6 | `app/api/v1/goods/<product>/schemas.py` | Pydantic схемы |
| 7 | `app/api/v1/goods/<product>/routes.py` | API эндпоинты |
| 8 | `app/api/v1/goods/router.py` | Подключить роутер |
| 9 | `app/api/v1/router.py` | Подключить если новый раздел |
| 10 | `app/services/configurator/calculators/<product>_calculator.py` | Добавить калькулятор (наследовать `BaseCostCalculator`) |
| 11 | `app/services/configurator/validators.py` | Добавить валидатор (наследовать `BaseValidator`) |
| 12 | `app/services/configurator/calculators/__init__.py` | Добавить в фабрику `CALCULATORS` |
| 13 | `app/services/configurator/validators.py` | Добавить в фабрику `VALIDATORS` |
| 11 | `tests/goods/test_<product>.py` | Unit тесты модели |
| 12 | `tests/schemas/test_<product>_schema.py` | Тесты Pydantic схем |
| 13 | `tests/integration/placeholder/` | Добавить placeholder тесты |
| 14 | `frontend/src/core/constants/product.constants.ts` | Добавить тип в `FurnitureType` |
| 15 | `frontend/src/core/types/product.types.ts` | Добавить TypeScript типы |
| 16 | `frontend/src/api/endpoints/products/<product>.endpoints.ts` | Создать эндпоинты |
| 17 | `frontend/src/api/services/<product>.service.ts` | Создать API сервис |
| 18 | `frontend/src/modules/<product>/` | Создать модуль (компоненты, страницы) |
| 19 | `frontend/src/core/config/routes.config.ts` | Добавить маршруты |
| 20 | `KODA.md` | Обновить документацию |

## Примеры для копирования

### Backend

- **Модель**: `app/models/goods/bookshelf.py`
- **Детали**: `app/models/goods/nightstand_part.py`
- **Pydantic схемы**: `app/api/v1/goods/bookshelf/schemas.py`
- **API роуты**: `app/api/v1/goods/nightstand/routes.py`

### Frontend

- **Эндпоинты**: `frontend/src/api/endpoints/products/bookshelf.endpoints.ts`
- **Сервис**: `frontend/src/api/services/bookshelf.service.ts`
- **Типы**: `frontend/src/core/types/product.types.ts`
- **Константы**: `frontend/src/core/constants/product.constants.ts`

### Тесты

- **Unit**: `tests/goods/test_bookshelf.py`
- **Schema**: `tests/schemas/test_bookshelf_schema.py`
- **Integration**: `tests/integration/placeholder/`

## PostgreSQL

После добавления модели:

```bash
# Создать миграцию
alembic revision --autogenerate -m "Add <product> table"

# Применить миграцию
alembic upgrade head
```

## Конфигуратор

Новый API конфигуратора использует паттерн Factory и SRP:

**1. Создать калькулятор:**
```python
# app/services/configurator/calculators/<product>_calculator.py
from app.services.configurator.calculators.base_calculator import BaseCostCalculator

class ProductCalculator(BaseCostCalculator):
    def calculate(self, config: Dict[str, Any]) -> Dict[str, Any]:
        # Расчёт стоимости
        pass
```

**2. Создать валидатор:**
```python
# app/services/configurator/validators.py
from app.services.configurator.validators import BaseValidator

class ProductValidator(BaseValidator):
    def validate(self, config: Dict[str, Any]) -> Dict[str, Any]:
        # Валидация
        pass
```

**3. Добавить в фабрики:**
```python
# calculators/__init__.py
CALCULATORS = {
    # ...
    "product": ProductCalculator,
}

# validators.py
VALIDATORS = {
    # ...
    "product": ProductValidator(),
}
```

**Использование:**
```python
from app.services.configurator import create_configurator_service

service = create_configurator_service(db)
cost = service.calculate("product", config)
validation = service.validate("product", config)
```

## Проверка

```bash
# Backend
python -m pytest tests/ -v

# Frontend
cd frontend && npm run build

# API тесты
curl http://localhost:8000/v1/configurator/options
```

## Обновление документации

Не забыть обновить:
- `KODA.md` — добавить новый тип мебели
- `README.md` — если есть список функционала
- `api/v1/configurator.py` — если новые эндпоинты

