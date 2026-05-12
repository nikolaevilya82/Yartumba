"""
GET эндпоинты корзины
SRP: Только GET запросы
"""
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.v1.goods.dependencies import get_db
from app.api.v1.goods.cart.dependencies import get_cart
from app.api.v1.goods.cart.schemas import CartItemResponse, CartResponse, CartSummary
from app.models.cart import Cart

router = APIRouter(prefix="/cart", tags=["Cart"])


@router.get("/", response_model=CartResponse, summary="Получить корзину")
async def get_cart_endpoint(
    cart: Cart = Depends(get_cart),
    db: Session = Depends(get_db),
):
    """
    Получить текущую корзину пользователя.
    
    **Auth:** Optional (авторизован → через user_id, иначе → через session_id)
    
    **Response:** CartResponse
    
    **Status:** 200 OK
    """
    # Сбор данных корзины
    items = []
    for item in cart.items:
        items.append(CartItemResponse(
            id=str(item.id),
            cart_id=str(item.cart_id),
            furniture_type=item.furniture_type,
            furniture_id=str(item.furniture_id),
            configuration_id=str(item.configuration_id) if item.configuration_id else None,
            quantity=item.quantity,
            unit_price=item.unit_price,
            saved_configuration_snapshot=item.saved_configuration_snapshot,
            item_total=item.total_price,
            furniture_name=None,  # TODO: получить из товара
            created_at=item.created_at,
            updated_at=item.updated_at,
        ))
    
    items_count = sum(item.quantity for item in cart.items)
    subtotal = sum(item.total_price for item in cart.items)
    
    return CartResponse(
        id=str(cart.id),
        user_id=str(cart.user_id) if cart.user_id else None,
        session_id=cart.session_id,
        items=items,
        items_count=items_count,
        subtotal=subtotal,
        created_at=cart.created_at,
        updated_at=cart.updated_at,
    )
