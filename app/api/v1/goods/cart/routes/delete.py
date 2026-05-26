"""
DELETE эндпоинты корзины
SRP: Только DELETE запросы
"""
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.v1.goods.dependencies import get_db
from app.api.v1.goods.cart.dependencies import get_cart
from app.api.v1.goods.cart.schemas import CartSummary, RemoveFromCartResponse
from app.models.cart import Cart
from app.services.cart_service import CartService

router = APIRouter(tags=["Cart"])


@router.delete("/items/{item_id}", summary="Удалить товар из корзины")
async def remove_item_from_cart(
    item_id: str,
    cart: Cart = Depends(get_cart),
    db: Session = Depends(get_db),
):
    """
    Удалить товар из корзины.
    
    **Auth:** Optional
    
    **Response:** RemoveFromCartResponse
    
    **Status:** 200 OK
    
    **Errors:**
    - 404: товар не в корзине
    """
    from fastapi import HTTPException
    
    cart_service = CartService()
    
    try:
        updated_cart = cart_service.remove_item(
            db=db,
            cart_id=str(cart.id),
            item_id=item_id,
        )
        
        total_items = sum(item.quantity for item in updated_cart.items)
        total_price = sum(item.total_price for item in updated_cart.items)
        
        cart_summary = CartSummary(
            total_items=total_items,
            total_price=total_price,
        )
        
        return RemoveFromCartResponse(
            removed_item_id=item_id,
            cart_summary=cart_summary,
        )
        
    except ValueError as e:
        raise HTTPException(
            status_code=404,
            detail=str(e)
        )


@router.delete("/", summary="Очистить корзину")
async def clear_cart(
    cart: Cart = Depends(get_cart),
    db: Session = Depends(get_db),
):
    """
    Очистить всю корзину.
    
    **Auth:** Optional
    
    **Response:** { "message": "Cart cleared" }
    
    **Status:** 200 OK
    """
    cart_service = CartService()
    cart_service.clear_cart(db, str(cart.id))
    
    return {"message": "Cart cleared"}
