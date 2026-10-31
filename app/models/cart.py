"""
Модель корзины покупок
Отвечает за хранение товаров в корзине пользователя
"""
import uuid
from datetime import datetime, timezone
from sqlalchemy import Column, String, ForeignKey, Integer, Numeric, DateTime, Text
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.types import JSON
from sqlalchemy.orm import relationship, backref
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
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    
    # Дата последнего обновления
    updated_at = Column(
        DateTime,
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
    )
    
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
    furniture_type = Column(String(50), nullable=False, index=True)  # bookshelf, nightstand, dresser
    
    # ID конкретной мебели (bookshelf.id, nightstand.id, dresser.id)
    furniture_id = Column(PG_UUID(as_uuid=True), nullable=False, index=True)

    # ID конфигурации из каталога (опционально)
    configuration_id = Column(PG_UUID(as_uuid=True), nullable=True, index=True)
    
    # Конфигурация товара (JSON для совместимости с SQLite и PostgreSQL)
    # Структура зависит от furniture_type:
    # - bookshelf: {"parts": [...], "materials": {...}, "dimensions": {...}}
    # - nightstand: {"parts": [...], "drawers": [...], "materials": {...}}
    # - dresser: {"parts": [...], "drawers": [...], "facade_options": {...}}
    configuration = Column(JSON, nullable=False)
    
    # Количество
    quantity = Column(Integer, nullable=False, default=1)
    
    # Цена за единицу (на момент добавления) - в копейках для точности
    unit_price = Column(Numeric(10, 2), nullable=False)
    
    # Итоговая цена
    total_price = Column(Numeric(10, 2), nullable=False)
    
    # Снепшот материалов (для истории цен и проверки актуальности)
    materials_snapshot = Column(JSON, nullable=True)
    
    # Дата создания
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    
    # Дата последнего обновления
    updated_at = Column(
        DateTime,
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
    )
    
    # Ссылка на корзину.
    # delete-orphan: при удалении корзины её позиции удаляются ORM-ом,
    # иначе SQLAlchemy пытается обнулить cart_id (NOT NULL) и падает.
    cart = relationship(
        "Cart",
        backref=backref("items", cascade="all, delete-orphan"),
    )

    # Ссылка на Product (каталог)
    product = relationship("Product", lazy="joined")
    
    def __repr__(self):
        return f"<CartItem {self.id} product={self.product_id} type={self.furniture_type} qty={self.quantity}>"
    
    def get_furniture_object(self, db):
        """
        Получить объект мебели (Bookshelf/Nightstand/Dresser)
        
        Args:
            db: Database session
            
        Returns:
            Bookshelf | Nightstand | Dresser | None
        """
        from app.core.furniture_registry import get_furniture

        return get_furniture(db, self.furniture_type, self.furniture_id)
    
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
        from app.services.configurator import create_configurator_service
        
        service = create_configurator_service(db)
        
        # Определяем тип мебели для конфигуратора
        furniture_type = self.furniture_type  # bookshelf, nightstand, dresser
        
        # Расчёт стоимости через конфигуратор
        result = service.calculate(furniture_type, self.configuration)
        
        # Получаем итоговую цену из результата (в копейках)
        price = result.get("total_price", float(self.unit_price))
        
        self.unit_price = price
        self.total_price = price * self.quantity
        
        return price
