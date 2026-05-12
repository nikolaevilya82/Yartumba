"""
PATCH эндпоинты корзины
SRP: Только PATCH запросы
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.api.v1.goods.dependencies import get_db
from app.api.v1.goods.cart.dependencies import get_cart
from app.api.v1.goods.cart.schemas import (
    CartItemUpdate,
    CartItemResponse,
    CartSummary,
    UpdateCartItemResponse,
)
from app.models.cart import Cart
from app.services.cart_service import CartService

router = APIRouter(prefix="/cart", tags=["Cart"])


@router.patch("/items/{item_id}", response_model=UpdateCartItemResponse, summary="Обновить количество товара")
async def update_cart_item_quantity(
    item_id: str,
    request: CartItemUpdate,
    cart: Cart = Depends(get_cart),
    db: Session = Depends(get_db),
):
    """
    Обновить количество товара в корзине.
    
    **Auth:** Optional
    
    **Request:** CartItemUpdate (quantity)
    
    **Response:** UpdateCartItemResponse
    
    **Status:** 200 OK
    
    **Errors:**
    - 404: товар не в корзине
    - 400: quantity < 1
    """
    cart_service = CartService()
    
    try:
        updated_cart = cart_service.update_item_quantity(
            db=db,
            cart_id=str(cart.id),
            item_id=item_id,
            quantity=request.quantity,
        )
        
        # Получаем обновлённый элемент
        cart_item = None
        for item in updated_cart.items:
            if str(item.id) == item_id:
                cart_item = item
                break
        
        if not cart_item:
            raise HTTPException(
                status_code=HTTPException.status_code,
                detail="Товар не найден в корзине"
            )
        
        cart_item_response = CartItemResponse(
            id=str(cart_item.id),
            cart_id=str(cart_item.cart_id),
            furniture_type=cart_item.furniture_type,
            furniture_id=str(cart_item.furniture_id),
            configuration_id=str(cart_item.configuration_id) if cart_item.configuration_id else None,
            quantity=cart_item.quantity,
            unit_price=cart_item.unit_price,
            saved_configuration_snapshot=cart_item.saved_configuration_snapshot,
            item_total=cart_item.total_price,
            furniture_name=None,
            created_at=cart_item.created_at,
            updated_at=cart_item.updated_at,
        )
        
        items_count = sum(item.quantity for item in updated_cart.items)
        subtotal = sum(item.total_price for item in updated_cart.items)
        
        cart_summary = CartSummary(
            items_count=items_count,
            subtotal=subtotal,
        )
        
        return UpdateCartItemResponse(
            cart_item=cart_item_response,
            cart_summary=cart_summary,
        )
        
    except ValueError as e:
        if "не найдена" in str(e):
            raise HTTPException(
                status_code=404,
                detail=str(e)
            )
        raise HTTPException(
            status_code=400,
            detail=str(e)
        )
