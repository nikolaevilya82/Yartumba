"""
Pydantic схемы для конфигураций
"""
from typing import Dict, Any, List, Optional
from pydantic import BaseModel, Field, field_validator


class NightstandConfig(BaseModel):
    """Конфигурация прикроватной тумбы"""
    width: int = Field(..., ge=300, le=800)
    height: int = Field(..., ge=300, le=800)
    depth: int = Field(..., ge=300, le=600)
    drawers: Dict[str, Any] = Field(default_factory=dict)
    bodyMaterial: Dict[str, Any] = Field(default_factory=dict)
    hardware: Dict[str, Any] = Field(default_factory=dict)


class BookshelfConfig(BaseModel):
    """Конфигурация книжной полки"""
    width: int = Field(..., ge=400, le=2000)
    height: int = Field(..., ge=400, le=2400)
    depth: int = Field(..., ge=200, le=600)
    shelf_count: int = Field(..., ge=1, le=10)
    shelf_type: str = Field(default="closed")
    bodyMaterial: Dict[str, Any] = Field(default_factory=dict)


class DresserConfig(BaseModel):
    """Конфигурация комода"""
    width: int = Field(..., ge=600, le=1600)
    height: int = Field(..., ge=600, le=1200)
    depth: int = Field(..., ge=400, le=700)
    drawer_count: int = Field(..., ge=1, le=6)
    bodyMaterial: Dict[str, Any] = Field(default_factory=dict)
    hardware: Dict[str, Any] = Field(default_factory=dict)


class ValidationResponse(BaseModel):
    """Ответ валидации"""
    valid: bool
    errors: List[str] = Field(default_factory=list)


class CostBreakdown(BaseModel):
    """Детализация стоимости"""
    materials_cost: int
    hardware_cost: int
    work_cost: int
    total_price: int
    details: Dict[str, Any]
