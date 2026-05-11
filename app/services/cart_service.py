"""
Сервис корзины
Отвечает за бизнес-логику работы с корзиной
"""
import json
from typing import Optional, Dict, Any, List
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.models.cart import Cart, CartItem
from app.models.goods import Bookshelf, Nightstand, Dresser
from app.services.configuratorservice import configurator_service


class CartService:
    """Сервис для работы с корзиной"""

    def __init__(self, db: Session):
        self.db = db

    def get_or_create_cart(self, user_id: Optional[str] = None, session_id: Optional[str] = None) -> Cart:
        """
        Получить или создать корзину
        SRP: Только создание/получение корзины
        """
        if user_id:
            cart = self.db.query(Cart).filter(Cart.user_id == user_id).first()
            if cart:
                return cart
        
        if session_id:
            cart = self.db.query(Cart).filter(Cart.session_id == session_id).first()
            if cart:
                return cart
        
        # Создаем новую корзину
        cart = Cart(user_id=user_id, session_id=session_id)
        self.db.add(cart)
        self.db.commit()
        self.db.refresh(cart)
        return cart

    def add_item(
        self,
        cart: Cart,
        product_type: str,
        product_id: str,
        configuration: Dict[str, Any],
        quantity: int = 1
    ) -> CartItem:
        """
        Добавить товар в корзину
        SRP: Только добавление товара
        """
        # Проверяем существует ли товар
        product = self._get_product(product_type, product_id)
        if not product:
            raise ValueError(f"Товар {product_type}/{product_id} не найден")
        
        # Рассчитываем цену в зависимости от типа товара
        if product_type == "nightstand":
            price_result = configurator_service.calculate_nightstand_cost(configuration)
            unit_price = price_result["total_price"]
        elif product_type == "bookshelf":
            # Упрощённый расчёт для полки
            unit_price = self._calculate_bookshelf_price(configuration)
        elif product_type == "dresser":
            # Упрощённый расчёт для комода
            unit_price = self._calculate_dresser_price(configuration)
        else:
            raise ValueError(f"Неподдерживаемый тип товара: {product_type}")
        
        # Проверяем есть ли такой товар в корзине
        existing_item = self.db.query(CartItem).filter(
            CartItem.cart_id == cart.id,
            CartItem.product_type == product_type,
            CartItem.product_id == product_id,
            CartItem.configuration == json.dumps(configuration)
        ).first()
        
        if existing_item:
            # Обновляем количество
            existing_item.quantity += quantity
            existing_item.total_price = existing_item.unit_price * existing_item.quantity
            self.db.commit()
            self.db.refresh(existing_item)
            return existing_item
        
        # Создаем новый товар
        cart_item = CartItem(
            cart_id=cart.id,
            product_type=product_type,
            product_id=product_id,
            configuration=json.dumps(configuration),
            quantity=quantity,
            unit_price=unit_price,
            total_price=unit_price * quantity
        )
        
        self.db.add(cart_item)
        self.db.commit()
        self.db.refresh(cart_item)
        return cart_item

    def get_cart_items(self, cart: Cart) -> List[CartItem]:
        """
        Получить все товары в корзине
        SRP: Только чтение товаров
        """
        return self.db.query(CartItem).filter(CartItem.cart_id == cart.id).all()

    def update_item_quantity(self, cart_item: CartItem, quantity: int) -> CartItem:
        """
        Обновить количество товара
        SRP: Только обновление количества
        """
        cart_item.quantity = quantity
        cart_item.total_price = cart_item.unit_price * quantity
        self.db.commit()
        self.db.refresh(cart_item)
        return cart_item

    def remove_item(self, cart_item: CartItem) -> None:
        """
        Удалить товар из корзины
        SRP: Только удаление
        """
        self.db.delete(cart_item)
        self.db.commit()

    def clear_cart(self, cart: Cart) -> None:
        """
        Очистить корзину
        SRP: Только очистка
        """
        items = self.db.query(CartItem).filter(CartItem.cart_id == cart.id).all()
        for item in items:
            self.db.delete(item)
        self.db.commit()

    def get_cart_summary(self, cart: Cart) -> Dict[str, Any]:
        """
        Получить резюме корзины
        SRP: Только подсчёт итогов
        """
        items = self.get_cart_items(cart)
        total_items = sum(item.quantity for item in items)
        total_price = sum(item.total_price for item in items)
        
        return {
            "total_items": total_items,
            "total_price": total_price,
            "item_count": len(items)
        }

    def _get_product(self, product_type: str, product_id: str):
        """
        Получить товар по типу и ID
        SRP: Только получение товара
        """
        if product_type == "bookshelf":
            return self.db.query(Bookshelf).filter(Bookshelf.id == product_id).first()
        elif product_type == "nightstand":
            return self.db.query(Nightstand).filter(Nightstand.id == product_id).first()
        elif product_type == "dresser":
            return self.db.query(Dresser).filter(Dresser.id == product_id).first()
        return None

    def _calculate_bookshelf_price(self, config: Dict[str, Any]) -> float:
        """Упрощённый расчёт цены полки"""
        base_price = 5000
        width = config.get("width", 800)
        height = config.get("height", 2000)
        depth = config.get("depth", 350)
        shelf_count = config.get("shelves", 5)
        
        # Коэффициенты
        width_factor = width / 800
        height_factor = height / 2000
        depth_factor = depth / 350
        shelves_factor = 1 + (shelf_count - 5) * 0.1
        
        return int(base_price * width_factor * height_factor * depth_factor * shelves_factor)

    def _calculate_dresser_price(self, config: Dict[str, Any]) -> float:
        """Упрощённый расчёт цены комода"""
        base_price = 10000
        width = config.get("width", 1000)
        height = config.get("height", 800)
        depth = config.get("depth", 500)
        drawer_count = config.get("drawers", 4)
        
        # Коэффициенты
        width_factor = width / 1000
        height_factor = height / 800
        depth_factor = depth / 500
        drawers_factor = 1 + (drawer_count - 4) * 0.15
        
        return int(base_price * width_factor * height_factor * depth_factor * drawers_factor)
