"""
Атрибуты товаров: размеры, материалы, цвета и их возможные значения
"""
import uuid
from sqlalchemy import Column, String, Text, Integer, ForeignKey, Enum as SQLEnum
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from app.core.db_setup import Base
from app.models.catalog.attribute_type import AttributeType, SizeUnit


class Attribute(Base):
    """
    Атрибут товара.
    Пример: "Материал", "Цвет", "Ширина", "Высота"
    """
    __tablename__ = "attributes"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    code = Column(String(50), unique=True, nullable=False, index=True)
    name = Column(String(100), nullable=False)
    description = Column(Text, nullable=True)
    
    # Тип атрибута (size, material, color...)
    type = Column(SQLEnum(AttributeType), nullable=False, index=True)
    
    # Для size-атрибутов — единица измерения
    unit = Column(SQLEnum(SizeUnit), nullable=True)
    
    # Для сортировки в UI
    sort_order = Column(Integer, default=0)
    
    # Может ли клиент изменять этот атрибут
    is_configurable = Column(Integer, default=True)  # 0 = только для чтения

    def __repr__(self):
        return f"<Attribute {self.code}: {self.name}>"


class AttributeValue(Base):
    """
    Возможное значение атрибута.
    Примеры: для "Материал" — "дуб", "сосна", "МДФ"
              для "Цвет" — "белый", "чёрный", "коричневый"
              для "Ширина" — 600, 800, 1000 (в единицах атрибута)
    """
    __tablename__ = "attribute_values"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    attribute_id = Column(
        UUID(as_uuid=True),
        ForeignKey("attributes.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )
    
    value = Column(String(100), nullable=False)  # "дуб", "белый", "800"
    
    # Для числовых значений (размеры)
    numeric_value = Column(Integer, nullable=True)  # 800 (в мм)
    
    # Цена доплаты за это значение (в копейках). 0 = бесплатно
    price_modifier = Column(Integer, default=0)
    
    # Сортировка в UI
    sort_order = Column(Integer, default=0)
    
    # Связь
    attribute = relationship("Attribute", backref="values")

    def __repr__(self):
        return f"<AttributeValue {self.attribute.code}={self.value}>"
