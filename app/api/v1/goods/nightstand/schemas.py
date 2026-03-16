"""
Схемы Pydantic для прикроватных тумб
"""
from uuid import UUID
from typing import Optional
from pydantic import BaseModel, Field

# Импорт базовых схем из bookshelf (они общие)
from app.api.v1.goods.bookshelf.schemas import (
    GoodsBase,
    GoodsCreate,
    GoodsUpdate,
    GoodsResponse,
)


# === Схемы для Nightstand ===
class NightstandCreate(GoodsCreate):
    """Создание прикроватной тумбы"""
    drawer_count: int = Field(default=1, ge=1, le=10, description="Количество ящиков")
    has_open_shelf: bool = Field(default=False, description="Есть открытая полка")
    leg_type: str = Field(default="standard", description="Тип ножек: standard, metal, wooden")


class NightstandUpdate(GoodsUpdate):
    """Обновление прикроватной тумбы"""
    drawer_count: Optional[int] = Field(None, ge=1, le=10)
    has_open_shelf: Optional[bool] = None
    leg_type: Optional[str] = None


class NightstandResponse(GoodsResponse):
    """Ответ с прикроватной тумбой"""
    drawer_count: int
    has_open_shelf: bool
    leg_type: str

    class Config:
        from_attributes = True


# === Схемы для деталей NightstandPart ===
class NightstandPartBase(BaseModel):
    """Базовая схема детали"""
    name: str = Field(..., description="Название детали: боковина, полка, верх, низ, задняя стенка, фасад")
    part_width: Optional[int] = Field(None, gt=0, description="Ширина детали в мм")
    part_height: Optional[int] = Field(None, gt=0, description="Высота детали в мм")
    part_depth: Optional[int] = Field(None, gt=0, description="Глубина детали в мм")
    quantity: int = Field(default=1, ge=1, description="Количество таких деталей")


class NightstandPartCreate(NightstandPartBase):
    """Создание детали"""
    sheet_material_id: Optional[UUID] = None


class NightstandPartUpdate(BaseModel):
    """Обновление детали"""
    name: Optional[str] = None
    part_width: Optional[int] = Field(None, gt=0)
    part_height: Optional[int] = Field(None, gt=0)
    part_depth: Optional[int] = Field(None, gt=0)
    quantity: Optional[int] = Field(None, ge=1)
    sheet_material_id: Optional[UUID] = None


class NightstandPartResponse(NightstandPartBase):
    """Ответ с деталью"""
    id: UUID
    nightstand_id: UUID
    sheet_material_id: Optional[UUID]

    class Config:
        from_attributes = True


# === Схема для списка деталей ===
class NightstandWithParts(NightstandResponse):
    """Прикроватная тумба с деталями"""
    parts: list[NightstandPartResponse] = []

    class Config:
        from_attributes = True

