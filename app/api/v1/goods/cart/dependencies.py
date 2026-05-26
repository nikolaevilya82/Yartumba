"""
Зависимости для корзины
SRP: Только получение корзины из авторизации или сессии
"""
import uuid
from typing import Optional, Annotated
from fastapi import Depends, HTTPException, status, Request
from pydantic import UUID4
from sqlalchemy.orm import Session

from app.api.v1.goods.dependencies import get_db
from app.models.cart import Cart, CartItem
from app.services.cart_service import CartService

# ============================================================================
# Зависимости для получения user_id и session_id
# ============================================================================


def get_optional_user_id() -> Optional[str]:
    """
    Получить user_id из токена авторизации (опционально).
    
    TODO: Реализовать после внедрения авторизации.
    Сейчас возвращает None (гостевой режим).
    """
    # TODO: Добавить проверку JWT токена
    return None


def get_optional_session_id(request: Request) -> Optional[str]:
    """
    Получить session_id из query-параметра, заголовка или cookies.
    
    Приоритет:
    1. Query-параметр ?session_id=...
    2. Заголовок X-Session-ID
    3. Cookie session_id
    
    Returns:
        Optional[str]: session_id или None
    """
    # 1. Query param
    session_id = request.query_params.get("session_id")
    if session_id:
        return session_id
    
    # 2. Header
    session_id = request.headers.get("X-Session-ID")
    if session_id:
        return session_id
    
    # 3. Cookie
    session_id = request.cookies.get("session_id")
    if session_id:
        return session_id
    
    return None


# ============================================================================
# Зависимости для получения корзины
# ============================================================================


def get_cart_identifier(
    user_id: Optional[str] = Depends(get_optional_user_id),
    session_id: Optional[str] = Depends(get_optional_session_id),
) -> tuple[Optional[str], Optional[str], bool]:
    """
    Получить идентификатор корзины, session_id и флаг авторизации.
    
    Логика:
    1. Если есть user_id → корзина пользователя
    2. Если есть session_id → гостевая корзина
    3. Иначе → генерируем новый session_id (первый визит)
    
    Returns:
        tuple[Optional[str], Optional[str], bool]:
            - identifier: user_id или session_id (never None)
            - session_id: текущий или сгенерированный session_id
            - is_user_authenticated: True если пользователь авторизован
    """
    if user_id:
        return user_id, None, True
    
    if not session_id:
        # Генерируем новый session_id для первого визита
        session_id = str(uuid.uuid4())
    
    return session_id, session_id, False


def get_cart(
    identifier: Annotated[tuple[Optional[str], Optional[str], bool], Depends(get_cart_identifier)],
    db: Session = Depends(get_db),
) -> Cart:
    """
    Получить или создать корзину по идентификатору.
    
    Args:
        identifier: (identifier, session_id, is_authenticated)
        db: Database session
        
    Returns:
        Cart: Объект корзины
    """
    user_id_or_session, session_id, is_authenticated = identifier
    
    cart_service = CartService()
    cart = cart_service.get_or_create_cart(
        db=db,
        user_id=user_id_or_session if is_authenticated else None,
        session_id=session_id if not is_authenticated else None,
    )
    
    return cart


def get_cart_id(
    cart: Cart = Depends(get_cart),
) -> str:
    """
    Получить ID корзины.
    
    SRP: Только получение ID корзины (строка).
    Использует get_cart для DRY принципа.
    
    Args:
        cart: Объект корзины (через dependency)
        
    Returns:
        str: ID корзины
    """
    return str(cart.id)


def get_cart_item_by_id(
    cart_id: str,
    item_id: str,
    db: Session = Depends(get_db),
) -> CartItem:
    """
    Получить конкретный товар из корзины.
    
    SRP: Только поиск и валидация товара в корзине.
    
    Args:
        cart_id: ID корзины
        item_id: ID товара
        db: Database session
        
    Returns:
        CartItem: Товар в корзине
        
    Raises:
        HTTPException: 404 если товар не найден
    """
    cart_item = db.query(CartItem).filter(
        CartItem.id == item_id,
        CartItem.cart_id == cart_id,
    ).first()
    
    if not cart_item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Товар не найден в корзине",
        )
    
    return cart_item
