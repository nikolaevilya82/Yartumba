"""
Сохранённые конфигурации товаров
"""
import uuid
from sqlalchemy import Column, String, ForeignKey, Integer, Boolean
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from app.core.db_setup import Base


class ProductConfiguration(Base):
    """
    Сохранённая конфигурация товара с выбранными опциями.
    Одна конфигурация может содержать несколько выбранных значений атрибутов.
    """
    __tablename__ = "product_configurations"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    
    product_id = Column(
        UUID(as_uuid=True),
        ForeignKey("products.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )
    
    # Название конфигурации (например, "Мой шкаф" или "Детская комната")
    name = Column(String(200), nullable=True)
    
    # Итоговая цена с учётом всех опций (в копейках)
    total_price = Column(Integer, nullable=False)
    
    # Публичная ссылка для шаринга
    share_token = Column(String(64), unique=True, nullable=True, index=True)
    
    # Связи
    product = relationship("Product", back_populates="configurations")
    items = relationship("ConfigurationItem", back_populates="configuration", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<ProductConfiguration {self.product.sku}: {self.name}>"


class ConfigurationItem(Base):
    """
    Выбранное значение атрибута в конфигурации.
    Пример: { attribute: "material", value: "oak" }
    """
    __tablename__ = "configuration_items"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    
    configuration_id = Column(
        UUID(as_uuid=True),
        ForeignKey("product_configurations.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )
    
    attribute_id = Column(
        UUID(as_uuid=True),
        ForeignKey("attributes.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )
    
    attribute_value_id = Column(
        UUID(as_uuid=True),
        ForeignKey("attribute_values.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )
    
    # Связи
    configuration = relationship("ProductConfiguration", back_populates="items")
    attribute = relationship("Attribute")
    attribute_value = relationship("AttributeValue")

    def __repr__(self):
        return f"<ConfigurationItem {self.attribute.code}={self.attribute_value.value}>"
