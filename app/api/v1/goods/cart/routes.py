"""
API эндпоинты корзины
Отвечает за HTTP маршруты корзины
"""
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.api.v1.goods.dependencies import get_db
from app.api.v1.goods.cart.schemas import (
    CartItemCreate,
    CartItemResponse,
    CartResponse,
    CartUpdateQuantity,
    CartSummary,
)
from app.models.cart import Cart, CartItem
from app.services.cart_service import CartService

router = APIRouter(prefix="/cart", tags=["Cart"])


@router.get("/", response_model=CartResponse, summary="Получить корзину")
def get_cart(
    user_id: Optional[str] = None,
    session_id: Optional[str] = None,
    db: Session = Depends(get_db),
):
    """
    Получить корзину пользователя или гостя.
    
    - **user_id**: ID пользователя (для авторизованных)
    - **session_id**: ID сессии (для гостей)
    """
    if not user_id and not session_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Требуется user_id или session_id"
        )
    
    cart_service = CartService(db)
    cart = cart_service.get_or_create_cart(user_id=user_id, session_id=session_id)
    items = cart_service.get_cart_items(cart)
    summary = cart_service.get_cart_summary(cart)
    
    return CartResponse(
        id=str(cart.id),
        user_id=str(cart.user_id) if cart.user_id else None,
        session_id=cart.session_id,
        items=[
            CartItemResponse(
                id=str(item.id),
                cart_id=str(item.cart_id),
                product_type=item.product_type,
                product_id=str(item.product_id),
                configuration=item.configuration,
                quantity=item.quantity,
                unit_price=item.unit_price,
                total_price=item.total_price,
            )
            for item in items
        ],
        total_items=summary["total_items"],
        total_price=summary["total_price"],
    )


@router.post("/items", response_model=CartItemResponse, summary="Добавить товар в корзину")
def add_to_cart(
    item_data: CartItemCreate,
    user_id: Optional[str] = None,
    session_id: Optional[str] = None,
    db: Session = Depends(get_db),
):
    """
    Добавить товар в корзину.
    
    - **product_type**: bookshelf, nightstand, dresser
    - **product_id**: ID товара
    - **configuration**: Конфигурация товара (JSON)
    - **quantity**: Количество (по умолчанию 1)
    """
    if not user_id and not session_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Требуется user_id или session_id"
        )
    
    cart_service = CartService(db)
    cart = cart_service.get_or_create_cart(user_id=user_id, session_id=session_id)
    
    try:
        cart_item = cart_service.add_item(
            cart=cart,
            product_type=item_data.product_type,
            product_id=item_data.product_id,
            configuration=item_data.configuration,
            quantity=item_data.quantity,
        )
        
        return CartItemResponse(
            id=str(cart_item.id),
            cart_id=str(cart_item.cart_id),
            product_type=cart_item.product_type,
            product_id=str(cart_item.product_id),
            configuration=cart_item.configuration,
            quantity=cart_item.quantity,
            unit_price=cart_item.unit_price,
            total_price=cart_item.total_price,
        )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )


@router.get("/summary", response_model=CartSummary, summary="Получить резюме корзины")
def get_cart_summary(
    user_id: Optional[str] = None,
    session_id: Optional[str] = None,
    db: Session = Depends(get_db),
):
    """
    Получить резюме корзины (общее количество и цена).
    """
    if not user_id and not session_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Требуется user_id или session_id"
        )
    
    cart_service = CartService(db)
    cart = cart_service.get_or_create_cart(user_id=user_id, session_id=session_id)
    summary = cart_service.get_cart_summary(cart)
    
    return CartSummary(
        total_items=summary["total_items"],
        total_price=summary["total_price"],
        item_count=summary["item_count"],
    )


@router.patch("/items/{item_id}", response_model=CartItemResponse, summary="Обновить количество товара")
def update_item_quantity(
    item_id: str,
    quantity_data: CartUpdateQuantity,
    db: Session = Depends(get_db),
):
    """
    Обновить количество товара в корзине.
    
    - **item_id**: ID товара в корзине
    - **quantity**: Новое количество
    """
    cart_service = CartService(db)
    cart_item = db.query(CartItem).filter(CartItem.id == item_id).first()
    
    if not cart_item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Товар в корзине не найден"
        )
    
    updated_item = cart_service.update_item_quantity(cart_item, quantity_data.quantity)
    
    return CartItemResponse(
        id=str(updated_item.id),
        cart_id=str(updated_item.cart_id),
        product_type=updated_item.product_type,
        product_id=str(updated_item.product_id),
        configuration=updated_item.configuration,
        quantity=updated_item.quantity,
        unit_price=updated_item.unit_price,
        total_price=updated_item.total_price,
    )


@router.delete("/items/{item_id}", response_model=dict, summary="Удалить товар из корзины")
def remove_from_cart(
    item_id: str,
    db: Session = Depends(get_db),
):
    """
    Удалить товар из корзины.
    
    - **item_id**: ID товара в корзине
    """
    cart_service = CartService(db)
    cart_item = db.query(CartItem).filter(CartItem.id == item_id).first()
    
    if not cart_item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Товар в корзине не найден"
        )
    
    cart_service.remove_item(cart_item)
    
    return {"message": "Товар удалён из корзины"}


@router.delete("/", response_model=dict, summary="Очистить корзину")
def clear_cart(
    user_id: Optional[str] = None,
    session_id: Optional[str] = None,
    db: Session = Depends(get_db),
):
    """
    Очистить всю корзину.
    """
    if not user_id and not session_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Требуется user_id или session_id"
        )
    
    cart_service = CartService(db)
    cart = cart_service.get_or_create_cart(user_id=user_id, session_id=session_id)
    cart_service.clear_cart(cart)
    
    return {"message": "Корзина очищена"}
