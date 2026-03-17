"""
Схемы Pydantic для прикроватных тумб
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
class NightstandPartBase(PartBase):
    """Базовая схема детали"""
    name: str = Field(..., description="Название детали: боковина, полка, верх, низ, задняя стенка, фасад")


class NightstandPartCreate(PartCreate):
    """Создание детали"""
    pass


class NightstandPartUpdate(PartUpdate):
    """Обновление детали"""
    pass


class NightstandPartResponse(PartResponse):
    """Ответ с деталью"""
    nightstand_id: UUID

    class Config:
        from_attributes = True


# === Схема для списка деталей ===
class NightstandWithParts(NightstandResponse):
    """Прикроватная тумба с деталями"""
    parts: list[NightstandPartResponse] = []

    class Config:
        from_attributes = True

