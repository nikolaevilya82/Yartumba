"""
Общие схемы Pydantic для всех типов товаров
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


# === Базовая схема детали (общая для всех) ===
class PartBase(BaseModel):
    """Базовая схема детали"""
    name: str = Field(..., description="Название детали")
    part_width: Optional[int] = Field(None, gt=0, description="Ширина детали в мм")
    part_height: Optional[int] = Field(None, gt=0, description="Высота детали в мм")
    part_depth: Optional[int] = Field(None, gt=0, description="Глубина детали в мм")
    quantity: int = Field(default=1, ge=1, description="Количество таких деталей")


class PartCreate(PartBase):
    """Создание детали"""
    sheet_material_id: Optional[UUID] = None


class PartUpdate(BaseModel):
    """Обновление детали"""
    name: Optional[str] = None
    part_width: Optional[int] = Field(None, gt=0)
    part_height: Optional[int] = Field(None, gt=0)
    part_depth: Optional[int] = Field(None, gt=0)
    quantity: Optional[int] = Field(None, ge=1)
    sheet_material_id: Optional[UUID] = None


class PartResponse(PartBase):
    """Ответ с деталью"""
    id: UUID
    sheet_material_id: Optional[UUID]

    class Config:
        from_attributes = True

