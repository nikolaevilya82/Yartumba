"""
Связь товаров с доступными атрибутами
"""
import uuid
from sqlalchemy import Column, ForeignKey, Boolean, Integer, String, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from app.core.db_setup import Base


class ProductAttribute(Base):
    """
    Какие атрибуты доступны для конкретного товара.
    Позволяет настроить конфигурацию для каждого товара отдельно.
    """
    __tablename__ = "product_attributes"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    
    product_id = Column(
        UUID(as_uuid=True),
        ForeignKey("products.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )
    
    attribute_id = Column(
        UUID(as_uuid=True),
        ForeignKey("attributes.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )
    
    # Обязательный ли этот атрибут для выбора
    is_required = Column(Boolean, default=False)
    
    # Значение по умолчанию (id значения из attribute_values)
    default_value_id = Column(UUID(as_uuid=True), nullable=True)
    
    # Минимальное значение (для size-атрибутов) в мм
    min_value = Column(Integer, nullable=True)
    
    # Максимальное значение (для size-атрибутов) в мм
    max_value = Column(Integer, nullable=True)
    
    # Шаг изменения (для size-атрибутов) в мм
    step_value = Column(Integer, nullable=True)
    
    # Позволять ли клиенту изменять этот атрибут
    is_configurable = Column(Boolean, default=True)
    
    # Сортировка в UI
    sort_order = Column(Integer, default=0)
    
    # Подсказка для клиента
    help_text = Column(Text, nullable=True)

    # Связи
    product = relationship("Product", back_populates="attributes")
    attribute = relationship("Attribute")
    default_value = relationship("AttributeValue", foreign_keys=[default_value_id])

    def __repr__(self):
        return f"<ProductAttribute {self.product.sku} -> {self.attribute.code}>"
