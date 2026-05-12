"""
Merge эндпоинты корзины
SRP: Только POST /cart/merge
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.api.v1.goods.dependencies import get_db
from app.api.v1.goods.cart.schemas import CartItemResponse, CartResponse
from app.models.cart import Cart
from app.services.cart_service import CartService

router = APIRouter(prefix="/cart", tags=["Cart"])


@router.post("/merge", response_model=CartResponse, summary="Объединить корзины")
async def merge_carts(
    request: dict,
    user_id: str,  # TODO: получить из токена авторизации через dependency
    db: Session = Depends(get_db),
):
    """
    Объединить гостевую корзину с пользовательской (при логине).
    
    **Auth:** Required
    
    **Request:** { "session_id": "uuid-string" }
    
    **Response:** CartResponse
    
    **Status:** 200 OK
    """
    if not user_id:
        raise HTTPException(
            status_code=401,
            detail="Требуется авторизация"
        )
    
    guest_session_id = request.get("session_id")
    if not guest_session_id:
        raise HTTPException(
            status_code=400,
            detail="Требуется session_id"
        )
    
    cart_service = CartService()
    merged_cart = cart_service.merge_carts(
        db=db,
        guest_session_id=guest_session_id,
        user_id=user_id,
    )
    
    # Формируем ответ
    items = []
    for item in merged_cart.items:
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
            furniture_name=None,
            created_at=item.created_at,
            updated_at=item.updated_at,
        ))
    
    items_count = sum(item.quantity for item in merged_cart.items)
    subtotal = sum(item.total_price for item in merged_cart.items)
    
    return CartResponse(
        id=str(merged_cart.id),
        user_id=str(merged_cart.user_id) if merged_cart.user_id else None,
        session_id=merged_cart.session_id,
        items=items,
        items_count=items_count,
        subtotal=subtotal,
        created_at=merged_cart.created_at,
        updated_at=merged_cart.updated_at,
    )
