"""
Схемы Pydantic для книжных полок
"""
from uuid import UUID
from typing import Optional
from datetime import datetime
from pydantic import BaseModel, Field


# === Базовая схема товара (общая для всех) ===
class GoodsBase(BaseModel):
    """Базовая схема товара"""
    width: int = Field(..., gt=0, description="Ширина в мм")
    height: int = Field(..., gt=0, description="Высота в мм")
    depth: int = Field(..., gt=0, description="Глубина в мм")


class GoodsCreate(GoodsBase):
    """Создание товара"""
    product_id: Optional[UUID] = None


class GoodsUpdate(BaseModel):
    """Обновление товара - все поля опциональны"""
    width: Optional[int] = Field(None, gt=0)
    height: Optional[int] = Field(None, gt=0)
    depth: Optional[int] = Field(None, gt=0)


class GoodsResponse(GoodsBase):
    """Ответ с товаром"""
    id: UUID
    product_id: Optional[UUID]
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


# === Схемы для Bookshelf ===
class BookshelfCreate(GoodsCreate):
    """Создание книжной полки"""
    shelf_count: int = Field(default=3, ge=1, le=20, description="Количество полок")
    shelf_type: str = Field(default="open", description="Тип: open, closed, mixed")


class BookshelfUpdate(GoodsUpdate):
    """Обновление книжной полки"""
    shelf_count: Optional[int] = Field(None, ge=1, le=20)
    shelf_type: Optional[str] = None


class BookshelfResponse(GoodsResponse):
    """Ответ с книжной полкой"""
    shelf_count: int
    shelf_type: str

    class Config:
        from_attributes = True


# === Схемы для деталей BookshelfPart ===
class BookshelfPartBase(BaseModel):
    """Базовая схема детали"""
    name: str = Field(..., description="Название детали: боковина, полка, верх, низ, задняя стенка")
    part_width: Optional[int] = Field(None, gt=0, description="Ширина детали в мм")
    part_height: Optional[int] = Field(None, gt=0, description="Высота детали в мм")
    part_depth: Optional[int] = Field(None, gt=0, description="Глубина детали в мм")
    quantity: int = Field(default=1, ge=1, description="Количество таких деталей")


class BookshelfPartCreate(BookshelfPartBase):
    """Создание детали"""
    sheet_material_id: Optional[UUID] = None


class BookshelfPartUpdate(BaseModel):
    """Обновление детали"""
    name: Optional[str] = None
    part_width: Optional[int] = Field(None, gt=0)
    part_height: Optional[int] = Field(None, gt=0)
    part_depth: Optional[int] = Field(None, gt=0)
    quantity: Optional[int] = Field(None, ge=1)
    sheet_material_id: Optional[UUID] = None


class BookshelfPartResponse(BookshelfPartBase):
    """Ответ с деталью"""
    id: UUID
    bookshelf_id: UUID
    sheet_material_id: Optional[UUID]

    class Config:
        from_attributes = True


# === Схема для списка деталей ===
class BookshelfWithParts(BookshelfResponse):
    """Книжная полка с деталями"""
    parts: list[BookshelfPartResponse] = []

    class Config:
        from_attributes = True

