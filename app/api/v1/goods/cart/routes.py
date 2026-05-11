"""
API эндпоинты корзины
Отвечает за HTTP маршруты корзины
"""
from typing import Optional
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.v1.goods.dependencies import get_db
from app.api.v1.goods.cart.schemas import (
    CartItemCreate,
    CartItemUpdate,
    CartItemResponse,
    CartResponse,
    CartSummary,
    AddToCartRequest,
    AddToCartResponse,
    RemoveFromCartResponse,
    UpdateCartItemResponse,
)
from app.models.cart import CartItem
from app.services.cart_service import CartService

router = APIRouter(prefix="/cart", tags=["Cart"])


# ============================================================================
# GET /v1/cart - Получить текущую корзину
# ============================================================================

@router.get("/", response_model=CartResponse, summary="Получить корзину")
async def get_cart(
    user_id: Optional[str] = None,
    session_id: Optional[str] = None,
    db: Session = Depends(get_db),
):
    """
    Получить текущую корзину пользователя.
    
    **Auth:** Optional (авторизован → через user_id, иначе → через session_id)
    
    **Response:** CartResponse
    
    **Status:** 200 OK
    """
    if not user_id and not session_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Требуется user_id или session_id"
        )
    
    cart_service = CartService()
    cart = cart_service.get_or_create_cart(db, user_id=user_id, session_id=session_id)
    
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


# ============================================================================
# POST /v1/cart/items - Добавить товар в корзину
# ============================================================================

@router.post("/items", response_model=AddToCartResponse, status_code=status.HTTP_201_CREATED, summary="Добавить товар в корзину")
async def add_item_to_cart(
    request: AddToCartRequest,
    user_id: Optional[str] = None,
    session_id: Optional[str] = None,
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
    if not user_id and not session_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Требуется user_id или session_id"
        )
    
    cart_service = CartService()
    
    try:
        # Создаём CartItemCreate из запроса
        item_data = CartItemCreate(
            furniture_type=request.furniture_type,
            furniture_id=request.furniture_id,
            configuration_id=None,  # TODO: получить из конфигурации
            quantity=request.quantity,
        )
        
        cart = cart_service.add_item(
            db=db,
            cart_id=None,  # Будет получена/создана внутри
            item_data=item_data,
            configuration=request.configuration,
        )
        
        # Получаем созданный/обновлённый элемент
        cart_item = None
        for item in cart.items:
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
            saved_configuration_snapshot=cart_item.saved_configuration_snapshot,
            item_total=cart_item.total_price,
            furniture_name=None,
            created_at=cart_item.created_at,
            updated_at=cart_item.updated_at,
        )

        items_count = sum(item.quantity for item in cart.items)
        subtotal = sum(item.total_price for item in cart.items)

        cart_summary = CartSummary(
            items_count=items_count,
            subtotal=subtotal,
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
    

# ============================================================================
# PATCH /v1/cart/items/{item_id} - Обновить количество товара
# ============================================================================

@router.patch("/items/{item_id}", response_model=UpdateCartItemResponse, summary="Обновить количество товара")
async def update_cart_item_quantity(
    item_id: str,
    request: CartItemUpdate,
    user_id: Optional[str] = None,
    session_id: Optional[str] = None,
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
    if not user_id and not session_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Требуется user_id или session_id"
        )
    
    cart_service = CartService()
    
    # Получаем корзину
    cart = cart_service.get_or_create_cart(db, user_id=user_id, session_id=session_id)
    
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
            # Если quantity был <= 0, товар был удалён
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
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
                status_code=status.HTTP_404_NOT_FOUND,
                detail=str(e)
            )
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


# ============================================================================
# DELETE /v1/cart/items/{item_id} - Удалить товар из корзины
# ============================================================================

@router.delete("/items/{item_id}", response_model=RemoveFromCartResponse, summary="Удалить товар из корзины")
async def remove_item_from_cart(
    item_id: str,
    user_id: Optional[str] = None,
    session_id: Optional[str] = None,
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
    if not user_id and not session_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Требуется user_id или session_id"
        )
    
    cart_service = CartService()
    
    # Получаем корзину
    cart = cart_service.get_or_create_cart(db, user_id=user_id, session_id=session_id)
    
    try:
        updated_cart = cart_service.remove_item(
            db=db,
            cart_id=str(cart.id),
            item_id=item_id,
        )
        
        items_count = sum(item.quantity for item in updated_cart.items)
        subtotal = sum(item.total_price for item in updated_cart.items)
        
        cart_summary = CartSummary(
            items_count=items_count,
            subtotal=subtotal,
        )
        
        return RemoveFromCartResponse(
            removed_item_id=item_id,
            cart_summary=cart_summary,
        )
        
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )


# ============================================================================
# DELETE /v1/cart - Очистить корзину
# ============================================================================

@router.delete("/", response_model=dict, summary="Очистить корзину")
async def clear_cart(
    user_id: Optional[str] = None,
    session_id: Optional[str] = None,
    db: Session = Depends(get_db),
):
    """
    Очистить всю корзину.
    
    **Auth:** Optional
    
    **Response:** { "message": "Cart cleared" }
    
    **Status:** 200 OK
    """
    if not user_id and not session_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Требуется user_id или session_id"
        )
    
    cart_service = CartService()
    cart = cart_service.get_or_create_cart(db, user_id=user_id, session_id=session_id)
    cart_service.clear_cart(db, str(cart.id))
    
    return {"message": "Cart cleared"}


# ============================================================================
# POST /v1/cart/merge - Объединить корзины (при логине)
# ============================================================================

@router.post("/merge", response_model=CartResponse, summary="Объединить корзины")
async def merge_carts(
    request: dict,
    user_id: str = Depends(lambda: None),  # TODO: получить из токена авторизации
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
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Требуется авторизация"
        )
    
    guest_session_id = request.get("session_id")
    if not guest_session_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
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
