"""
Pydantic схемы для корзины
Отвечает за валидацию запросов и ответов API корзины
"""
from typing import List, Optional, Any, Dict
from pydantic import BaseModel, Field


class CartItemCreate(BaseModel):
    """Схема создания товара в корзине"""
    product_type: str = Field(..., description="Тип товара: bookshelf, nightstand, dresser")
    product_id: str = Field(..., description="ID товара")
    configuration: Dict[str, Any] = Field(..., description="Конфигурация товара")
    quantity: int = Field(1, ge=1, le=99, description="Количество")


class CartItemResponse(BaseModel):
    """Схема ответа товара в корзине"""
    id: str
    cart_id: str
    product_type: str
    product_id: str
    configuration: Dict[str, Any]
    quantity: int
    unit_price: float
    total_price: float

    class Config:
        from_attributes = True


class CartResponse(BaseModel):
    """Схема ответа корзины"""
    id: str
    user_id: Optional[str] = None
    session_id: Optional[str] = None
    items: List[CartItemResponse] = []
    total_items: int = 0
    total_price: float = 0.0

    class Config:
        from_attributes = True


class CartUpdateQuantity(BaseModel):
    """Схема обновления количества товара"""
    quantity: int = Field(..., ge=1, le=99)


class CartItemUpdate(BaseModel):
    """Схема обновления товара в корзине"""
    configuration: Optional[Dict[str, Any]] = None
    quantity: Optional[int] = Field(None, ge=1, le=99)


class CartSummary(BaseModel):
    """Схема резюме корзины"""
    total_items: int = 0
    total_price: float = 0.0
    item_count: int = 0
