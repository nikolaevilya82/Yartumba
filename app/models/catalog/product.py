"""
Товары: шкафы, столы, тумбы и т.д.
"""
import uuid
from sqlalchemy import Column, String, Text, Boolean, Integer, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from app.core.db_setup import Base


class Product(Base):
    __tablename__ = "products"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    sku = Column(String(50), unique=True, nullable=False, index=True)
    name = Column(String(200), nullable=False)
    description = Column(Text, nullable=True)
    
    # Категория товара
    category_id = Column(
        UUID(as_uuid=True), 
        ForeignKey("categories.id", ondelete="SET NULL"),
        nullable=True,
        index=True
    )
    
    # Базовая цена без опций
    base_price = Column(Integer, nullable=False)  # в копейках
    
    # Для фильтрации и поиска
    is_active = Column(Boolean, default=True, index=True)
    sort_order = Column(Integer, default=0)

    # Связи
    category = relationship("Category", backref="products")
    attributes = relationship("ProductAttribute", back_populates="product", cascade="all, delete-orphan")
    configurations = relationship("ProductConfiguration", back_populates="product", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Product {self.sku}: {self.name}>"
