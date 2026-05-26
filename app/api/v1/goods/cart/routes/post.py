"""
POST эндпоинты корзины
SRP: Только POST запросы
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.v1.goods.dependencies import get_db
from app.api.v1.goods.cart.dependencies import get_cart
from app.api.v1.goods.cart.schemas import (
    CartItemCreate,
    CartItemResponse,
    CartSummary,
    AddToCartRequest,
    AddToCartResponse,
)
from app.models.cart import Cart
from app.services.cart_service import CartService

router = APIRouter(tags=["Cart"])


@router.post("/items", response_model=AddToCartResponse, status_code=status.HTTP_201_CREATED, summary="Добавить товар в корзину")
async def add_item_to_cart(
    request: AddToCartRequest,
    cart: Cart = Depends(get_cart),
    db: Session = Depends(get_db),
):
    """
    Добавить товар в корзину.
    
    **Auth:** Optional
    
    **Request:** AddToCartRequest (furniture_type, furniture_id, configuration, quantity)
    
    **Response:** AddToCartResponse
    
    **Status:** 201 Created
    
    **Errors:**
    - 404: товар не найден
    - 400: невалидные данные
    """
    cart_service = CartService()
    
    try:
        # Создаём CartItemCreate из запроса
        item_data = CartItemCreate(
            furniture_type=request.furniture_type,
            furniture_id=request.furniture_id,
            configuration_id=None,  # TODO: получить из конфигурации
            quantity=request.quantity,
            configuration=request.configuration,
        )
        
        updated_cart = cart_service.add_item(
            db=db,
            cart_id=str(cart.id),
            item_data=item_data,
            configuration=request.configuration,
        )
        
        # Получаем созданный/обновлённый элемент
        cart_item = None
        for item in updated_cart.items:
            if (item.furniture_type == request.furniture_type and 
                item.furniture_id == request.furniture_id):
                cart_item = item
                break
        
        if not cart_item:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Ошибка при добавлении товара"
            )
        
        cart_item_response = CartItemResponse(
            id=str(cart_item.id),
            cart_id=str(cart_item.cart_id),
            furniture_type=cart_item.furniture_type,
            furniture_id=str(cart_item.furniture_id),
            configuration_id=str(cart_item.configuration_id) if cart_item.configuration_id else None,
            quantity=cart_item.quantity,
            unit_price=cart_item.unit_price,
            configuration=cart_item.configuration,
            item_total=cart_item.total_price,
            furniture_name=cart_item.product.name if cart_item.product else None,
            created_at=cart_item.created_at,
            updated_at=cart_item.updated_at,
        )
        
        total_items = sum(item.quantity for item in updated_cart.items)
        total_price = sum(item.total_price for item in updated_cart.items)
        
        cart_summary = CartSummary(
            total_items=total_items,
            total_price=total_price,
        )
        
        return AddToCartResponse(
            cart_item=cart_item_response,
            cart_summary=cart_summary,
        )

    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
