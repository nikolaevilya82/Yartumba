# Как добавить новый тип мебели

## Быстрый чеклист

### Backend

| # | Файл | Что делать |
|---|------|------------|
| 1 | `app/models/goods/<product>.py` | Создать модель + детали в одном файле |
| 2 | `app/models/goods/__init__.py` | Экспортировать модели |
| 3 | `app/core/image_config.py` | Добавить путь в `FURNITURE_IMAGE_PATHS` |
| 4 | `app/api/v1/goods/<product>/schemas.py` | Pydantic схемы (наследовать `GoodsBase`) |
| 5 | `app/api/v1/goods/<product>/routes.py` | API эндпоинты |
| 6 | `app/api/v1/goods/router.py` | Подключить роутер |
| 7 | `app/services/configurator/calculators/<product>_calculator.py` | Калькулятор (наследовать `FurnitureCostCalculator`) |
| 8 | `app/services/configurator/validators.py` | Валидатор (наследовать `BaseValidator`) |
| 9 | `app/services/configurator/calculators/__init__.py` | Добавить в фабрику `CALCULATORS` |
| 10 | `app/services/configurator/validators.py` | Добавить в фабрику `VALIDATORS` |
| 11 | `tests/goods/test_<product>.py` | Unit тесты модели |
| 12 | `tests/schemas/test_<product>_schema.py` | Тесты Pydantic схем |
| 13 | `tests/integration/placeholder/` | Placeholder тесты |

### Frontend (минимум)

| # | Файл | Что делать |
|---|------|------------|
| 14 | `frontend/src/core/constants/product.constants.ts` | Добавить тип в `FurnitureType` |
| 15 | `frontend/src/core/types/catalog.types.ts` | Добавить TypeScript тип (если отличается) |
| 16 | `KODA.md` | Обновить документацию |
| 17 | `README.md` | Обновить статус/описание |

## Примеры для копирования

### Backend

#### 1. Модель (app/models/goods/<product>.py)

Обе модели — изделие и детали — в **одном файле**:

```python
import uuid
from sqlalchemy import Column, Integer, String, ForeignKey, Boolean
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from app.core.db_setup import Base


class NewProduct(Base):
    """Новый тип мебели. Заменить NewProduct на реальное название."""
    __tablename__ = "new_products"  # уникальное имя таблицы

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    product_id = Column(
        UUID(as_uuid=True),
        ForeignKey("products.id", ondelete="SET NULL"),
        nullable=True,
        index=True
    )

    width = Column(Integer, nullable=False)
    height = Column(Integer, nullable=False)
    depth = Column(Integer, nullable=False)

    # Специфичные поля
    drawer_count = Column(Integer, nullable=False, default=1)
    has_open_shelf = Column(Boolean, default=False)

    # Изображение (опционально — если не задано, генерируется через image_service)
    image_url = Column(String(500), nullable=True)

    product = relationship("Product", backref="new_product")

    # Связь с материалами через FurnitureMaterial
    materials = relationship(
        "FurnitureMaterial",
        primaryjoin="and_(NewProduct.id==foreign(FurnitureMaterial.furniture_id), "
                    "FurnitureMaterial.furniture_type=='new_product')",
        backref="new_product_ref",
        cascade="all, delete-orphan",
        viewonly=True
    )
    parts = relationship("NewProductPart", back_populates="new_product", cascade="all, delete-orphan")


class NewProductPart(Base):
    """Детали изделия."""
    __tablename__ = "new_product_parts"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    new_product_id = Column(
        UUID(as_uuid=True),
        ForeignKey("new_products.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )

    name = Column(String(100), nullable=False)
    part_width = Column(Integer, nullable=True)
    part_height = Column(Integer, nullable=True)
    part_depth = Column(Integer, nullable=True)
    quantity = Column(Integer, nullable=False, default=1)

    sheet_material_id = Column(
        UUID(as_uuid=True),
        ForeignKey("sheet_materials.id", ondelete="SET NULL"),
        nullable=True,
        index=True
    )

    new_product = relationship("NewProduct", back_populates="parts")
    sheet_material = relationship("SheetMaterial")
```

#### 2. Pydantic схемы (app/api/v1/goods/<product>/schemas.py)

```python
from uuid import UUID
from typing import Optional
from pydantic import Field

from app.api.v1.goods.schemas import (
    GoodsBase, GoodsCreate, GoodsUpdate, GoodsResponse,
    PartBase, PartCreate, PartUpdate, PartResponse,
)


class ProductCreate(GoodsCreate):
    """Создание."""
    drawer_count: int = Field(default=1, ge=1, le=10)
    has_open_shelf: bool = Field(default=False)


class ProductUpdate(GoodsUpdate):
    """Обновление."""
    drawer_count: Optional[int] = Field(None, ge=1, le=10)
    has_open_shelf: Optional[bool] = None


class ProductResponse(GoodsResponse):
    """Ответ."""
    drawer_count: int
    has_open_shelf: bool

    class Config:
        from_attributes = True


class ProductPartBase(PartBase):
    name: str = Field(..., description="Название детали")


class ProductPartCreate(PartCreate):
    pass


class ProductPartUpdate(PartUpdate):
    pass


class ProductPartResponse(PartResponse):
    product_id: UUID

    class Config:
        from_attributes = True


class ProductWithParts(ProductResponse):
    parts: list[ProductPartResponse] = []

    class Config:
        from_attributes = True
```

#### 3. Роуты (app/api/v1/goods/<product>/routes.py)

По аналогии с `app/api/v1/goods/bookshelf/routes.py`. Обязательно передать `image_url` при создании:

```python
new_product = NewProduct(
    width=data.width,
    height=data.height,
    depth=data.depth,
    drawer_count=data.drawer_count,
    has_open_shelf=data.has_open_shelf,
    product_id=data.product_id,
    image_url=data.image_url,
)
```

#### 4. image_config.py

```python
# app/core/image_config.py
PRODUCTS_PATH = f"{IMAGES_BASE_URL}/products"
# Добавить:
NEW_PRODUCT_IMAGE_PATH = f"{PRODUCTS_PATH}/new_product"

FURNITURE_IMAGE_PATHS = {
    # ... существующие типы
    "new_product": NEW_PRODUCT_IMAGE_PATH,
}
```

### Frontend

Каталог уже универсальный. Достаточно:

1. **Константы** (`frontend/src/core/constants/product.constants.ts`):
```typescript
export const FURNITURE_TYPES = {
  // ...
  new_product: { label: 'Новый тип', icon: 'ProductIcon' },
} as const;
```

2. **Типы** (`frontend/src/core/types/catalog.types.ts`):
```typescript
export type FurnitureType = 'bookshelf' | 'nightstand' | 'dresser' | 'new_product';
```

Компоненты `ProductCard`, `ProductList`, `CatalogPage` уже поддерживают любой тип через `furniture_type`.

### Тесты

- **Unit**: `tests/goods/test_<product>.py`
- **Schema**: `tests/schemas/test_<product>_schema.py`
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
# app/services/configurator/calculators/new_product_calculator.py
from app.services.configurator.calculators.furniture_calculator import FurnitureCostCalculator

class NewProductCalculator(FurnitureCostCalculator):
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

**2. Добавить валидатор в `validators.py`:**
```python
# app/services/configurator/validators.py

class NewProductValidator(BaseValidator):
    def validate(self, config: Dict[str, Any]) -> Dict[str, Any]:
        errors = []
        # Валидация размеров
        if config.get("width", 0) < 300:
            errors.append("Width too small")
        return {"valid": len(errors) == 0, "errors": errors}

# Добавить в фабрику:
VALIDATORS = {
    # ... существующие
    "new_product": NewProductValidator(),
}
```

**3. Добавить калькулятор в фабрику:**
```python
# app/services/configurator/calculators/__init__.py
CALCULATORS = {
    # ... существующие
    "new_product": NewProductCalculator,
}
```

**Использование:**
```python
from app.services.configurator import create_configurator_service

service = create_configurator_service(db)
cost = service.calculate("new_product", config)
validation = service.validate("new_product", config)
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
- `KODA.md` — добавить новый тип мебели в таблицы, связи, примеры
- `README.md` — обновить статус, добавить в список поддерживаемой мебели
- `ADD_NEW_PRODUCT.md` — если появились новые паттерны
- `app/core/image_config.py` — добавить путь для изображений нового типа

