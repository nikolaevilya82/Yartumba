"""
Схемы Pydantic для комодов
"""
from uuid import UUID
from typing import Optional
from pydantic import BaseModel, Field

# Импорт базовых схем
from app.api.v1.goods.bookshelf.schemas import (
    GoodsBase,
    GoodsCreate,
    GoodsUpdate,
    GoodsResponse,
)


# === Схемы для Dresser ===
class DresserCreate(GoodsCreate):
    """Создание комода"""
    drawer_count: int = Field(default=4, ge=1, le=20, description="Количество ящиков")
    drawer_rows: int = Field(default=2, ge=1, le=10, description="Количество рядов ящиков")
    dresser_type: str = Field(default="standard", description="Тип: standard, tall, wide")
    has_legs: bool = Field(default=True, description="Есть ножки")


class DresserUpdate(GoodsUpdate):
    """Обновление комода"""
    drawer_count: Optional[int] = Field(None, ge=1, le=20)
    drawer_rows: Optional[int] = Field(None, ge=1, le=10)
    dresser_type: Optional[str] = None
    has_legs: Optional[bool] = None


class DresserResponse(GoodsResponse):
    """Ответ с комодом"""
    drawer_count: int
    drawer_rows: int
    dresser_type: str
    has_legs: bool

    class Config:
        from_attributes = True


# === Схемы для деталей DresserPart ===
class DresserPartBase(BaseModel):
    """Базовая схема детали"""
    name: str = Field(..., description="Название детали: боковина, полка, верх, низ, задняя стенка, фасад")
    part_width: Optional[int] = Field(None, gt=0, description="Ширина детали в мм")
    part_height: Optional[int] = Field(None, gt=0, description="Высота детали в мм")
    part_depth: Optional[int] = Field(None, gt=0, description="Глубина детали в мм")
    quantity: int = Field(default=1, ge=1, description="Количество таких деталей")


class DresserPartCreate(DresserPartBase):
    """Создание детали"""
    sheet_material_id: Optional[UUID] = None


class DresserPartUpdate(BaseModel):
    """Обновление детали"""
    name: Optional[str] = None
    part_width: Optional[int] = Field(None, gt=0)
    part_height: Optional[int] = Field(None, gt=0)
    part_depth: Optional[int] = Field(None, gt=0)
    quantity: Optional[int] = Field(None, ge=1)
    sheet_material_id: Optional[UUID] = None


class DresserPartResponse(DresserPartBase):
    """Ответ с деталью"""
    id: UUID
    dresser_id: UUID
    sheet_material_id: Optional[UUID]

    class Config:
        from_attributes = True


# === Схема для списка деталей ===
class DresserWithParts(DresserResponse):
    """Комод с деталями"""
    parts: list[DresserPartResponse] = []

    class Config:
        from_attributes = True

