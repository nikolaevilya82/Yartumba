# Как добавить новый тип мебели

## Быстрый чеклист

| # | Файл | Что делать |
|---|------|------------|
| 1 | `app/models/goods/<product>.py` | Создать модель (по аналогии с `bookshelf.py`) |
| 2 | `app/models/goods/<product>_part.py` | Создать модель деталей |
| 3 | `app/models/goods/__init__.py` | Экспортировать модели |
| 4 | `api/v1/goods/<product>/schemas.py` | Pydantic схемы |
| 5 | `api/v1/goods/<product>/routes.py` | API эндпоинты |
| 6 | `api/v1/goods/router.py` | Подключить роутер |
| 7 | `core/constants/product.constants.ts` | Добавить тип в `FurnitureType` |
| 8 | `stores/configurator/configurator.data.ts` | Добавить дефолтный конфиг |
| 9 | `api/endpoints/products/<product>.endpoints.ts` | Создать эндпоинты |
| 10 | `api/services/<product>.service.ts` | Создать API сервис |
| 11 | `core/types/product.types.ts` | Добавить TypeScript типы |

## Примеры для копирования

- **Backend модель**: `app/models/goods/bookshelf.py`
- **Backend детали**: `app/models/goods/nightstand_part.py`
- **Pydantic схемы**: `api/v1/goods/bookshelf/schemas.py`
- **API роутеры**: `api/v1/goods/nightstand/routes.py`
- **Frontend эндпоинты**: `api/endpoints/products/bookshelf.endpoints.ts`
- **Frontend сервис**: `api/services/bookshelf.service.ts`

## Проверка

```bash
# Backend
python -m pytest tests/

# Frontend
cd frontend && npm run build
```

