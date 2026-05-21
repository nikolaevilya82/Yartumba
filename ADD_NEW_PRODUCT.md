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
| 10 | `app/services/configurator/calculators/<product>_calculator.py` | Добавить калькулятор (наследовать `FurnitureCostCalculator`) |
| 11 | `app/services/configurator/validators.py` | Добавить валидатор (наследовать `BaseValidator`) |
| 12 | `app/services/configurator/calculators/__init__.py` | Добавить в фабрику `CALCULATORS` |
| 13 | `app/services/configurator/validators.py` | Добавить в фабрику `VALIDATORS` |
| 14 | `tests/goods/test_<product>.py` | Unit тесты модели |
| 12 | `tests/schemas/test_<product>_schema.py` | Тесты Pydantic схем |
| 13 | `tests/integration/placeholder/` | Добавить placeholder тесты |
| 14 | `frontend/src/core/constants/product.constants.ts` | Добавить тип в `FurnitureType` |
| 15 | `frontend/src/core/types/catalog.types.ts` | Добавить TypeScript типы |
| 16 | `frontend/src/stores/catalog/catalog.store.ts` | Добавить React hook с состоянием |
| 17 | `frontend/src/stores/catalog/catalog.context.tsx` | Создать Context для каталога |
| 18 | `frontend/src/stores/catalog/index.ts` | Экспорт Provider и hook |
| 19 | `frontend/src/components/catalog/` | Создать компоненты (ProductCard, ProductList, ProductFilters) |
| 20 | `frontend/src/pages/catalog/` | Создать страницу каталога |
| 21 | `frontend/src/routes/AppRoutes.jsx` | Добавить маршруты |
| 22 | `frontend/src/App.jsx` | Добавить CatalogProvider |
| 23 | `KODA.md` | Обновить документацию |

## Примеры для копирования

### Backend

- **Модель**: `app/models/goods/bookshelf.py`
- **Детали**: `app/models/goods/nightstand_part.py`
- **Pydantic схемы**: `app/api/v1/goods/bookshelf/schemas.py`
- **API роуты**: `app/api/v1/goods/nightstand/routes.py`

### Frontend

- **Эндпоинты**: `frontend/src/api/endpoints/products/bookshelf.endpoints.ts`
- **Сервис**: `frontend/src/api/services/bookshelf.service.ts`
- **Типы**: `frontend/src/core/types/catalog.types.ts`
- **Константы**: `frontend/src/core/constants/product.constants.ts`
- **Store**: `frontend/src/stores/catalog/catalog.store.ts`
- **Context**: `frontend/src/stores/catalog/catalog.context.tsx`
- **Компоненты**: `frontend/src/components/catalog/ProductCard.jsx`

### React Context для каталога

**Пример создания:**

```typescript
// frontend/src/stores/catalog/catalog.store.ts
import { useState, useCallback } from 'react';

export function useCatalogStore() {
  const [products, setProducts] = useState<Product[]>([]);
  const [filteredProducts, setFilteredProducts] = useState<Product[]>([]);
  
  const setSelectedType = useCallback((type: FurnitureType | null) => {
    // Логика фильтрации
  }, []);
  
  return { products, filteredProducts, setSelectedType };
}
```

```typescript
// frontend/src/stores/catalog/catalog.context.tsx
import React, { createContext, useContext } from 'react';
import { useCatalogStore } from './catalog.store';

const CatalogContext = createContext<ReturnType<typeof useCatalogStore> | undefined>(undefined);

export function CatalogProvider({ children }) {
  const store = useCatalogStore();
  return <CatalogContext.Provider value={store}>{children}</CatalogContext.Provider>;
}

export function useCatalog() {
  const context = useContext(CatalogContext);
  if (!context) throw new Error('useCatalog must be used within CatalogProvider');
  return context;
}
```

**Использование в компонентах:**

```jsx
import { useCatalog } from '../../stores/catalog';

const ProductFilters = () => {
  const { selectedType, setSelectedType } = useCatalog();
  
  return (
    <button onClick={() => setSelectedType('bookshelf')}>
      Полки
    </button>
  );
};
```

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
from app.services.configurator.calculators.furniture_calculator import FurnitureCostCalculator

class ProductCalculator(FurnitureCostCalculator):
    def calculate(self, config: Dict[str, Any]) -> Dict[str, Any]:
        # Используем универсальные методы:
        # - calculate_body_area() - площадь материалов
        # - calculate_edge_length() - длина кромки
        # - calculate_sheet_cost() - стоимость материала
        # - calculate_edge_cost() - стоимость кромки
        # - calculate_hinge_cost() - стоимость петель
        # - calculate_slide_cost() - стоимость направляющих
        # - add_work_cost() - стоимость работы
        # - format_result() - форматирование результата
        
        total_area, area_details = self.calculate_body_area(
            width=config["width"],
            height=config["height"],
            depth=config["depth"],
            shelf_count=config.get("shelf_count", 0),
            facade_count=config.get("facade_count", 0),
            has_back_panel=config.get("has_back_panel", False)
        )
        
        total_edge, edge_details = self.calculate_edge_length(
            width=config["width"],
            height=config["height"],
            depth=config["depth"],
            shelf_count=config.get("shelf_count", 0),
            facade_count=config.get("facade_count", 0),
            has_back_panel=config.get("has_back_panel", False)
        )
        
        sheet_cost = self.calculate_sheet_cost(total_area, material_id)
        edge_cost = self.calculate_edge_cost(total_edge, edge_id)
        materials_cost = sheet_cost + edge_cost
        
        hardware_cost = self.calculate_hinge_cost(count, hinge_id)
        
        work_cost = self.add_work_cost(materials_cost, hardware_cost, rate=0.3)
        
        total_cost = self.calculate_total(materials_cost, hardware_cost, work_cost)
        
        return self.format_result(
            materials_cost=materials_cost,
            hardware_cost=hardware_cost,
            work_cost=work_cost,
            total_cost=total_cost,
            details={...}
        )
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

