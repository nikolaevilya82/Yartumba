"""
Схемы Pydantic для комодов
"""
from uuid import UUID
from typing import Optional
from pydantic import Field

# Импорт общих схем
from app.api.v1.goods.schemas import (
    GoodsBase,
    GoodsCreate,
    GoodsUpdate,
    GoodsResponse,
    PartBase,
    PartCreate,
    PartUpdate,
    PartResponse,
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
class DresserPartBase(PartBase):
    """Базовая схема детали"""
    name: str = Field(..., description="Название детали: боковина, полка, верх, низ, задняя стенка, фасад")


class DresserPartCreate(PartCreate):
    """Создание детали"""
    pass


class DresserPartUpdate(PartUpdate):
    """Обновление детали"""
    pass


class DresserPartResponse(PartResponse):
    """Ответ с деталью"""
    dresser_id: UUID

    class Config:
        from_attributes = True


# === Схема для списка деталей ===
class DresserWithParts(DresserResponse):
    """Комод с деталями"""
    parts: list[DresserPartResponse] = []

    class Config:
        from_attributes = True

