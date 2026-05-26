"""
Pydantic схемы для корзины
Отвечает за валидацию запросов и ответов API корзины

Принцип SRP: каждая схема отвечает только за одну конкретную задачу
"""
from datetime import datetime
from decimal import Decimal
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field, field_validator


# ============================================================================
# CART SCHEMAS
# ============================================================================

class CartBase(BaseModel):
    """Базовая схема корзины - общие поля"""
    user_id: Optional[str] = Field(None, description="ID пользователя")
    session_id: Optional[str] = Field(None, description="ID сессии для гостей")


class CartCreate(CartBase):
    """Схема создания корзины - минимальные обязательные поля"""
    pass  # user_id или session_id могут быть None


class CartUpdate(BaseModel):
    """Схема обновления корзины - только изменяемые поля"""
    session_id: Optional[str] = Field(None, description="Обновить session_id")


class CartResponse(BaseModel):
    """Схема ответа корзины - полная информация с вычисляемыми полями"""
    id: str = Field(..., description="ID корзины")
    user_id: Optional[str] = Field(None, description="ID пользователя")
    session_id: Optional[str] = Field(None, description="ID сессии")
    items: List["CartItemResponse"] = Field(default_factory=list, description="Элементы корзины")
    
    # Вычисляемые поля
    total_items: int = Field(..., description="Общее количество товаров")
    total_price: Decimal = Field(..., description="Итоговая сумма (без скидок)")
    created_at: datetime = Field(..., description="Дата создания")
    updated_at: datetime = Field(..., description="Дата обновления")
    
    class Config:
        from_attributes = True


# ============================================================================
# CART ITEM SCHEMAS
# ============================================================================

class CartItemBase(BaseModel):
    """Базовая схема позиции корзины - общие поля"""
    furniture_type: str = Field(..., description="Тип мебели: bookshelf, nightstand, dresser")
    furniture_id: str = Field(..., description="ID конкретной мебели")
    configuration_id: Optional[str] = Field(None, description="ID конфигурации из каталога")
    quantity: int = Field(..., ge=1, le=99, description="Количество")
    unit_price: Decimal = Field(..., ge=0, description="Цена за единицу")
    configuration: Optional[Dict[str, Any]] = Field(
        None, 
        description="Конфигурация товара (размеры, материалы)"
    )


class CartItemCreate(BaseModel):
    """Схема создания позиции корзины - только обязательные поля для создания"""
    furniture_type: str = Field(..., description="Тип мебели: bookshelf, nightstand, dresser")
    furniture_id: str = Field(..., description="ID конкретной мебели")
    configuration_id: Optional[str] = Field(None, description="ID конфигурации из каталога")
    quantity: int = Field(1, ge=1, le=99, description="Количество")
    configuration: Optional[Dict[str, Any]] = Field(
        None,
        description="Конфигурация товара (размеры, материалы)"
    )
    
    @field_validator('furniture_type')
    @classmethod
    def validate_furniture_type(cls, v: str) -> str:
        """Валидация типа мебели"""
        valid_types = ['bookshelf', 'nightstand', 'dresser']
        if v not in valid_types:
            raise ValueError(f'Неверный тип мебели. Допустимые: {", ".join(valid_types)}')
        return v


class CartItemUpdate(BaseModel):
    """Схема обновления позиции корзины - только изменяемые поля"""
    quantity: Optional[int] = Field(None, ge=1, le=99, description="Новое количество")


class CartItemResponse(BaseModel):
    """Схема ответа позиции корзины - полная информация с вычисляемыми полями"""
    id: str = Field(..., description="ID позиции")
    cart_id: str = Field(..., description="ID корзины")
    
    # Основные данные
    furniture_type: str = Field(..., description="Тип мебели")
    furniture_id: str = Field(..., description="ID мебели")
    configuration_id: Optional[str] = Field(None, description="ID конфигурации")
    quantity: int = Field(..., description="Количество")
    unit_price: Decimal = Field(..., description="Цена за единицу")
    configuration: Optional[Dict[str, Any]] = Field(None, description="Конфигурация товара")
    
    # Вычисляемые поля
    item_total: Decimal = Field(..., description="Сумма позиции (quantity * unit_price)")
    furniture_name: Optional[str] = Field(None, description="Название мебели")
    created_at: datetime = Field(..., description="Дата добавления")
    updated_at: datetime = Field(..., description="Дата обновления")
    
    class Config:
        from_attributes = True


# ============================================================================
# CART SUMMARY SCHEMAS
# ============================================================================

class CartSummary(BaseModel):
    """Схема резюме корзины - краткая информация для UI"""
    total_items: int = Field(..., description="Количество товаров")
    total_price: Decimal = Field(..., description="Подытог")
    
    class Config:
        from_attributes = True


# ============================================================================
# REQUEST/RESPONSE WRAPPERS
# ============================================================================

class AddToCartRequest(BaseModel):
    """Запрос добавления товара в корзину"""
    furniture_type: str = Field(..., description="Тип мебели")
    furniture_id: str = Field(..., description="ID мебели")
    configuration: Optional[Dict[str, Any]] = Field(None, description="Конфигурация")
    quantity: int = Field(1, ge=1, le=99, description="Количество")


class AddToCartResponse(BaseModel):
    """Ответ добавления товара в корзину"""
    success: bool = True
    message: str = "Товар добавлен в корзину"
    cart_item: CartItemResponse
    cart_summary: CartSummary


class RemoveFromCartResponse(BaseModel):
    """Ответ удаления товара из корзины"""
    success: bool = True
    message: str = "Товар удалён из корзины"
    removed_item_id: str
    cart_summary: CartSummary


class UpdateCartItemResponse(BaseModel):
    """Ответ обновления товара в корзине"""
    success: bool = True
    message: str = "Данные корзины обновлены"
    cart_item: CartItemResponse
    cart_summary: CartSummary
