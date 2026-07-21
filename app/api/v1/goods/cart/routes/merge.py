"""
Merge эндпоинты корзины
SRP: Только POST /cart/merge
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.api.v1.goods.dependencies import get_db
from app.api.v1.goods.cart.dependencies import get_current_user_id
from app.api.v1.goods.cart.schemas import (
    CartItemResponse,
    CartResponse,
    MergeCartsRequest,
)
from app.models.cart import Cart
from app.services.cart_service import CartService

router = APIRouter(tags=["Cart"])


@router.post("/merge", response_model=CartResponse, summary="Объединить корзины")
async def merge_carts(
    request: MergeCartsRequest,
    user_id: str = Depends(get_current_user_id),
    db: Session = Depends(get_db),
):
    """
    Объединить гостевую корзину с пользовательской (при логине).
    
    **Auth:** Required
    
    **Request:** MergeCartsRequest (session_id)
    
    **Response:** CartResponse
    
    **Status:** 200 OK
    
    **Errors:**
    - 401: пользователь не авторизован
    - 400: не указан session_id
    """
    cart_service = CartService()
    merged_cart = cart_service.merge_carts(
        db=db,
        guest_session_id=request.session_id,
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
            configuration=item.configuration,
            item_total=item.total_price,
            furniture_name=item.product.name if item.product else None,
            created_at=item.created_at,
            updated_at=item.updated_at,
        ))

    total_items = sum(item.quantity for item in merged_cart.items)
    total_price = sum(item.total_price for item in merged_cart.items)

    return CartResponse(
        id=str(merged_cart.id),
        user_id=str(merged_cart.user_id) if merged_cart.user_id else None,
        session_id=merged_cart.session_id,
        items=items,
        total_items=total_items,
        total_price=total_price,
        created_at=merged_cart.created_at,
        updated_at=merged_cart.updated_at,
    )
