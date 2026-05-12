"""
Зависимости для корзины
SRP: Только получение корзины из авторизации или сессии
"""
from typing import Optional, Annotated
from fastapi import Depends, HTTPException, status
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
    
    SRP: Только извлечение user_id из auth токена.
    
    TODO: Реализовать после внедрения авторизации.
    Сейчас возвращает None (гостевой режим).
    
    Returns:
        Optional[str]: user_id или None
    """
    # TODO: Добавить проверку JWT токена
    # from app.core.security import get_current_user
    # user = get_current_user(token)
    # return str(user.id) if user else None
    return None


def get_optional_session_id() -> Optional[str]:
    """
    Получить session_id из cookies или запроса (опционально).
    
    SRP: Только извлечение session_id из сессии.
    
    TODO: Реализовать получение из cookies.
    Сейчас возвращает None (требует явной передачи).
    
    Returns:
        Optional[str]: session_id или None
    """
    # TODO: Добавить получение из cookies
    # from fastapi import Request
    # request: Request = ...
    # return request.cookies.get("session_id")
    return None


# ============================================================================
# Зависимости для получения корзины
# ============================================================================


def get_cart_identifier(
    user_id: Optional[str] = Depends(get_optional_user_id),
    session_id: Optional[str] = Depends(get_optional_session_id),
) -> tuple[Optional[str], bool]:
    """
    Получить идентификатор корзины и флаг авторизации.
    
    Логика:
    1. Если есть user_id → корзина пользователя
    2. Если есть session_id → гостевая корзина
    3. Иначе → ошибка (требуется хотя бы один)
    
    SRP: Только определение идентификатора для корзины.
    
    Args:
        user_id: ID авторизованного пользователя (может быть None)
        session_id: ID сессии гостя (может быть None)
        
    Returns:
        tuple[Optional[str], bool]: (identifier, is_user_authenticated)
            - identifier: user_id или session_id (never None после проверки)
            - is_user_authenticated: True если пользователь авторизован
        
    Raises:
        HTTPException: 400 если нет ни user_id ни session_id
    """
    if not user_id and not session_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Требуется авторизация (user_id) или session_id"
        )
    
    # Приоритет: user_id > session_id
    identifier: Optional[str] = user_id if user_id else session_id
    is_authenticated = bool(user_id)
    
    return identifier, is_authenticated


def get_cart(
    identifier: Annotated[tuple[Optional[str], bool], Depends(get_cart_identifier)],
    db: Session = Depends(get_db),
) -> Cart:
    """
    Получить или создать корзину по идентификатору.
    
    SRP: Только получение/создание объекта корзины.
    
    Args:
        identifier: (user_id_or_session_id, is_authenticated)
        db: Database session
        
    Returns:
        Cart: Объект корзины
    """
    user_id, is_authenticated = identifier
    
    cart_service = CartService()
    cart = cart_service.get_or_create_cart(
        db=db,
        user_id=user_id if is_authenticated else None,
        session_id=user_id if not is_authenticated else None,
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
