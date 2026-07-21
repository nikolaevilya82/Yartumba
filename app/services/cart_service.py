"""
Сервис корзины
Отвечает за бизнес-логику работы с корзиной: добавление, удаление, обновление товаров
"""
from decimal import Decimal
from typing import Optional, Dict, Any
from sqlalchemy.orm import Session
from sqlalchemy import func

from app.models.cart import Cart, CartItem
from app.models.goods import Bookshelf, Nightstand, Dresser
from app.api.v1.goods.cart.schemas import CartItemCreate


class CartService:
    """Сервис для работы с корзиной"""

    # =========================================================================
    # Получение корзины
    # =========================================================================

    def get_or_create_cart(
        self,
        db: Session,
        user_id: Optional[str] = None,
        session_id: Optional[str] = None
    ) -> Cart:
        """
        Получить существующую корзину или создать новую
        
        Приоритет: user_id > session_id > создать новую
        
        Args:
            db: Database session
            user_id: ID пользователя (опционально)
            session_id: ID сессии для гостей (опционально)
            
        Returns:
            Cart: Корзина пользователя или гостя
        """
        # Приоритет 1: Ищем корзину пользователя
        if user_id:
            cart = db.query(Cart).filter(Cart.user_id == user_id).first()
            if cart:
                return cart
        
        # Приоритет 2: Ищем корзину по session_id
        if session_id:
            cart = db.query(Cart).filter(Cart.session_id == session_id).first()
            if cart:
                # Если есть user_id, привязываем корзину к пользователю
                if user_id:
                    cart.user_id = user_id
                    cart.session_id = None  # Убираем session_id после логина
                    db.commit()
                    db.refresh(cart)
                return cart
        
        # Приоритет 3: Создаём новую корзину
        return self._create_empty_cart(db, user_id=user_id, session_id=session_id)

    def get_cart_by_user_id(self, db: Session, user_id: str) -> Optional[Cart]:
        """
        Получить корзину пользователя по user_id
        
        Args:
            db: Database session
            user_id: ID пользователя
            
        Returns:
            Cart | None: Корзина или None
        """
        return db.query(Cart).filter(Cart.user_id == user_id).first()

    def get_cart_by_session_id(self, db: Session, session_id: str) -> Optional[Cart]:
        """
        Получить корзину по session_id
        
        Args:
            db: Database session
            session_id: ID сессии
            
        Returns:
            Cart | None: Корзина или None
        """
        return db.query(Cart).filter(Cart.session_id == session_id).first()

    def _create_empty_cart(
        self,
        db: Session,
        user_id: Optional[str] = None,
        session_id: Optional[str] = None
    ) -> Cart:
        """
        Создать пустую корзину
        
        Args:
            db: Database session
            user_id: ID пользователя (опционально)
            session_id: ID сессии (опционально)
            
        Returns:
            Cart: Новая пустая корзина
        """
        cart = Cart(user_id=user_id, session_id=session_id)
        db.add(cart)
        db.commit()
        db.refresh(cart)
        return cart

    # =========================================================================
    # Работа с товарами в корзине
    # =========================================================================

    def add_item(
        self,
        db: Session,
        cart_id: str,
        item_data: CartItemCreate,
        configuration: Optional[Dict[str, Any]] = None
    ) -> Cart:
        """
        Добавить товар в корзину
        
        1. Проверить существование товара (furniture_type + furniture_id)
        2. Получить product_id и актуальную цену товара
        3. Если товар уже в корзине → увеличить quantity
        4. Иначе → создать новый CartItem
        5. Вернуть обновленную корзину
        """
        # 1. Проверить существование корзины
        cart = db.query(Cart).filter(Cart.id == cart_id).first()
        if not cart:
            raise ValueError(f"Корзина {cart_id} не найдена")
        
        # 2. Проверить существование товара и получить product_id
        furniture = self._get_furniture(db, item_data.furniture_type, item_data.furniture_id)
        if not furniture:
            raise ValueError(
                f"Товар {item_data.furniture_type} {item_data.furniture_id} не найден"
            )
        
        if not furniture.product_id:
            raise ValueError(
                f"Товар {item_data.furniture_type} не привязан к каталогу (product_id отсутствует)"
            )
        
        product_id = str(furniture.product_id)
        
        # 3. Получить актуальную цену
        unit_price = self._get_furniture_price(db, furniture)
        
        # Определяем конфигурацию для сохранения
        item_configuration = item_data.configuration if item_data.configuration is not None else configuration
        if item_configuration is None:
            item_configuration = {}
        
        # 4. Ищем существующий товар в корзине
        existing_item = db.query(CartItem).filter(
            CartItem.cart_id == cart_id,
            CartItem.furniture_type == item_data.furniture_type,
            CartItem.furniture_id == item_data.furniture_id,
            CartItem.configuration_id == item_data.configuration_id
        ).first()
        
        if existing_item:
            # 5. Увеличиваем количество
            existing_item.quantity += item_data.quantity
            existing_item.unit_price = unit_price
            existing_item.total_price = unit_price * existing_item.quantity
            existing_item.configuration = item_configuration
            existing_item.materials_snapshot = configuration
        else:
            # 6. Создаём новый CartItem
            cart_item = CartItem(
                cart_id=cart_id,
                product_id=product_id,
                furniture_type=item_data.furniture_type,
                furniture_id=item_data.furniture_id,
                configuration_id=item_data.configuration_id,
                quantity=item_data.quantity,
                unit_price=unit_price,
                total_price=unit_price * item_data.quantity,
                configuration=item_configuration,
                materials_snapshot=configuration
            )
            db.add(cart_item)
        
        # 7. Сохраняем и обновляем корзину
        db.commit()
        db.refresh(cart)
        
        return cart

    def update_item_quantity(
        self,
        db: Session,
        cart_id: str,
        item_id: str,
        quantity: int
    ) -> Cart:
        """
        Обновить количество товара в корзине
        
        1. Проверить существование CartItem
        2. Если quantity <= 0 → удалить товар
        3. Иначе → обновить quantity
        4. Вернуть обновленную корзину
        
        Args:
            db: Database session
            cart_id: ID корзины
            item_id: ID позиции
            quantity: Новое количество
            
        Returns:
            Cart: Обновлённая корзина
            
        Raises:
            ValueError: Если позиция не найдена
        """
        # 1. Найти позицию
        cart_item = db.query(CartItem).filter(
            CartItem.id == item_id,
            CartItem.cart_id == cart_id
        ).first()
        
        if not cart_item:
            raise ValueError(f"Позиция {item_id} не найдена в корзине {cart_id}")
        
        # 2. Если quantity <= 0 → удалить
        if quantity <= 0:
            db.delete(cart_item)
        else:
            # 3. Обновить количество
            cart_item.quantity = quantity
            cart_item.total_price = cart_item.unit_price * quantity
        
        # 4. Сохранить и вернуть корзину
        db.commit()
        
        cart = db.query(Cart).filter(Cart.id == cart_id).first()
        db.refresh(cart)
        
        return cart

    def remove_item(self, db: Session, cart_id: str, item_id: str) -> Cart:
        """
        Удалить товар из корзины
        
        Args:
            db: Database session
            cart_id: ID корзины
            item_id: ID позиции
            
        Returns:
            Cart: Обновлённая корзина
            
        Raises:
            ValueError: Если позиция не найдена
        """
        # Найти и удалить позицию
        cart_item = db.query(CartItem).filter(
            CartItem.id == item_id,
            CartItem.cart_id == cart_id
        ).first()
        
        if not cart_item:
            raise ValueError(f"Позиция {item_id} не найдена в корзине {cart_id}")
        
        db.delete(cart_item)
        db.commit()
        
        cart = db.query(Cart).filter(Cart.id == cart_id).first()
        db.refresh(cart)
        
        return cart

    def clear_cart(self, db: Session, cart_id: str) -> Cart:
        """
        Очистить корзину (удалить все позиции)
        
        Args:
            db: Database session
            cart_id: ID корзины
            
        Returns:
            Cart: Пустая корзина
        """
        # Удаляем все позиции
        db.query(CartItem).filter(CartItem.cart_id == cart_id).delete()
        db.commit()
        
        cart = db.query(Cart).filter(Cart.id == cart_id).first()
        db.refresh(cart)
        
        return cart

    # =========================================================================
    # Расчёты
    # =========================================================================

    def _calculate_subtotal(self, db: Session, cart_id: str) -> Decimal:
        """
        Рассчитать подытог корзины (сумма всех item_total)
        
        Args:
            db: Database session
            cart_id: ID корзины
            
        Returns:
            Decimal: Подытог корзины
        """
        result = db.query(func.sum(CartItem.total_price)).filter(
            CartItem.cart_id == cart_id
        ).first()
        
        return result[0] or Decimal("0.00")

    def _calculate_items_count(self, db: Session, cart_id: str) -> int:
        """
        Рассчитать общее количество товаров в корзине
        
        Args:
            db: Database session
            cart_id: ID корзины
            
        Returns:
            int: Общее количество товаров
        """
        result = db.query(func.sum(CartItem.quantity)).filter(
            CartItem.cart_id == cart_id
        ).first()
        
        return result[0] or 0

    # =========================================================================
    # Объединение корзин (при логине)
    # =========================================================================

    def merge_carts(
        self,
        db: Session,
        guest_session_id: str,
        user_id: str
    ) -> Cart:
        """
        Объединить гостевую корзину с корзиной пользователя
        
        1. Получить гостевую корзину по session_id
        2. Получить/создать корзину пользователя
        3. Объединить товары (суммировать quantity для одинаковых)
        4. Удалить гостевую корзину
        5. Вернуть корзину пользователя
        
        Args:
            db: Database session
            guest_session_id: Session ID гостя
            user_id: ID пользователя
            
        Returns:
            Cart: Объединённая корзина пользователя
        """
        # 1. Получить гостевую корзину
        guest_cart = db.query(Cart).filter(
            Cart.session_id == guest_session_id
        ).first()
        
        if not guest_cart or not guest_cart.items:
            # Если гостевой корзины нет или она пуста, просто получаем корзину пользователя
            return self.get_or_create_cart(db, user_id=user_id)
        
        # 2. Получить корзину пользователя
        user_cart = self.get_or_create_cart(db, user_id=user_id)
        
        # 3. Объединить товары
        for guest_item in guest_cart.items:
            # Ищем аналогичный товар в корзине пользователя
            existing_item = db.query(CartItem).filter(
                CartItem.cart_id == user_cart.id,
                CartItem.furniture_type == guest_item.furniture_type,
                CartItem.furniture_id == guest_item.furniture_id,
                CartItem.configuration_id == guest_item.configuration_id
            ).first()
            
            if existing_item:
                # Суммируем количество
                existing_item.quantity += guest_item.quantity
                existing_item.total_price = existing_item.unit_price * existing_item.quantity
            else:
                # Переносим товар
                new_item = CartItem(
                    cart_id=user_cart.id,
                    furniture_type=guest_item.furniture_type,
                    furniture_id=guest_item.furniture_id,
                    configuration_id=guest_item.configuration_id,
                    quantity=guest_item.quantity,
                    unit_price=guest_item.unit_price,
                    total_price=guest_item.total_price,
                    materials_snapshot=guest_item.materials_snapshot,
                    configuration=guest_item.configuration,
                    product_id=guest_item.product_id,
                )
                db.add(new_item)
        
        # 4. Удалить гостевую корзину
        db.delete(guest_cart)
        db.commit()
        
        # 5. Вернуть корзину пользователя
        db.refresh(user_cart)
        return user_cart

    # =========================================================================
    # Вспомогательные методы
    # =========================================================================

    def _get_furniture(
        self,
        db: Session,
        furniture_type: str,
        furniture_id: str
    ):
        """
        Получить объект мебели по типу и ID
        
        Args:
            db: Database session
            furniture_type: Тип мебели
            furniture_id: ID мебели
            
        Returns:
            Bookshelf | Nightstand | Dresser | None
        """
        if furniture_type == "bookshelf":
            return db.query(Bookshelf).filter(Bookshelf.id == furniture_id).first()
        elif furniture_type == "nightstand":
            return db.query(Nightstand).filter(Nightstand.id == furniture_id).first()
        elif furniture_type == "dresser":
            return db.query(Dresser).filter(Dresser.id == furniture_id).first()
        return None

    def _get_furniture_price(
        self,
        db: Session,
        furniture
    ) -> Decimal:
        """
        Получить актуальную цену товара
        
        Args:
            db: Database session
            furniture: Объект мебели
            
        Returns:
            Decimal: Цена товара
        """
        if furniture and furniture.product and furniture.product.base_price:
            return Decimal(str(furniture.product.base_price))
        return Decimal("0.00")

    def _validate_furniture_exists(
        self,
        db: Session,
        furniture_type: str,
        furniture_id: str
    ) -> None:
        """
        Проверить, что товар существует в БД
        
        Args:
            db: Database session
            furniture_type: Тип мебели
            furniture_id: ID мебели
            
        Raises:
            ValueError: Если товар не найден
        """
        furniture = self._get_furniture(db, furniture_type, furniture_id)
        if not furniture:
            raise ValueError(f"Товар {furniture_type} {furniture_id} не найден")
