"""
Модель корзины покупок
Отвечает за хранение товаров в корзине пользователя
"""
import uuid
from datetime import datetime
from sqlalchemy import Column, String, ForeignKey, Integer, Numeric, DateTime, Text
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.dialects.postgresql import JSONB as PG_JSONB
from sqlalchemy.types import JSON
from sqlalchemy.orm import relationship
from app.core.db_setup import Base


class Cart(Base):
    """
    Корзина покупок пользователя.
    Одна корзина на одного пользователя.
    """
    __tablename__ = "carts"

    id = Column(PG_UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    
    # ID пользователя (будет заполняться после авторизации)
    user_id = Column(PG_UUID(as_uuid=True), nullable=True, index=True, unique=True)
    
    # Временная корзина для гостей (если user_id NULL)
    session_id = Column(String(255), nullable=True, index=True)
    
    # Дата создания
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Дата последнего обновления
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f"<Cart {self.id} user={self.user_id}>"


class CartItem(Base):
    """
    Товар в корзине.
    Связь между корзиной и товаром.
    """
    __tablename__ = "cart_items"

    id = Column(PG_UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    
    # Ссылка на корзину
    cart_id = Column(
        PG_UUID(as_uuid=True),
        ForeignKey("carts.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )
    
    # Полиморфная связь через Product
    product_id = Column(
        PG_UUID(as_uuid=True),
        ForeignKey("products.id", ondelete="RESTRICT"),
        nullable=False,
        index=True
    )
    
    # Тип товара для быстрого доступа (дублируем для производительности)
    product_type = Column(String(50), nullable=False, index=True)  # bookshelf, nightstand, dresser
    
    # ID конкретной мебели (bookshelf.id, nightstand.id, dresser.id)
    furniture_id = Column(PG_UUID(as_uuid=True), nullable=False, index=True)
    
    # Конфигурация товара (JSONB для PostgreSQL, JSON для SQLite)
    # Структура зависит от product_type:
    # - bookshelf: {"parts": [...], "materials": {...}, "dimensions": {...}}
    # - nightstand: {"parts": [...], "drawers": [...], "materials": {...}}
    # - dresser: {"parts": [...], "drawers": [...], "facade_options": {...}}
    configuration = Column(PG_JSONB() if hasattr(PG_JSONB, '_is_postgresql') else JSON, nullable=False)
    
    # Количество
    quantity = Column(Integer, nullable=False, default=1)
    
    # Цена за единицу (на момент добавления) - в копейках для точности
    unit_price = Column(Numeric(10, 2), nullable=False)
    
    # Итоговая цена
    total_price = Column(Numeric(10, 2), nullable=False)
    
    # Снепшот материалов (для истории цен и проверки актуальности)
    materials_snapshot = Column(PG_JSONB() if hasattr(PG_JSONB, '_is_postgresql') else JSON, nullable=True)
    
    # Дата создания
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Дата последнего обновления
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Ссылка на корзину
    cart = relationship("Cart", backref="items")

    # Ссылка на Product (каталог)
    product = relationship("Product", lazy="joined")
    
    def __repr__(self):
        return f"<CartItem {self.id} product={self.product_id} type={self.product_type} qty={self.quantity}>"
    
    def get_furniture_object(self, db):
        """
        Получить объект мебели (Bookshelf/Nightstand/Dresser)
        
        Args:
            db: Database session
            
        Returns:
            Bookshelf | Nightstand | Dresser | None
        """
        if self.product_type == "bookshelf":
            from app.models.goods import Bookshelf
            return db.query(Bookshelf).filter(Bookshelf.id == self.furniture_id).first()
        elif self.product_type == "nightstand":
            from app.models.goods import Nightstand
            return db.query(Nightstand).filter(Nightstand.id == self.furniture_id).first()
        elif self.product_type == "dresser":
            from app.models.goods import Dresser
            return db.query(Dresser).filter(Dresser.id == self.furniture_id).first()
        return None
    
    def recalculate_price(self, db):
        """
        Пересчитать цену на основе текущих материалов
        
        Args:
            db: Database session
            
        Returns:
            float: Новая цена за единицу
        """
        furniture = self.get_furniture_object(db)
        if not furniture:
            return float(self.unit_price)
        
        # Используем конфигуратор для расчёта
        from app.services.configurator_service import calculate_furniture_price
        
        price = calculate_furniture_price(
            furniture_type=self.product_type,
            configuration=self.configuration,
            db=db
        )
        
        self.unit_price = price
        self.total_price = price * self.quantity
        
        return price
