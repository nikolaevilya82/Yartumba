"""
Фурнитура: направляющие, петли
"""
import uuid
from sqlalchemy import Column, String, Integer, Boolean, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from app.core.db_setup import Base


class SlideGuide(Base):
    """
    Направляющие для ящиков.
    """
    __tablename__ = "slide_guides"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    
    # Название
    name = Column(String(100), nullable=False)
    
    # Тип направляющих
    guide_type = Column(String(50), nullable=False)  # roller, ball, push_to_open, tandem, metabox
    
    # Тип выдвижения: роликовые, шариковые, полновыкатные
    extension_type = Column(String(50), nullable=False)  # partial, full, overtravel
    
    # Длина в мм
    length = Column(Integer, nullable=False)
    
    # Нагрузка на пару в кг
    load_capacity = Column(Integer, default=30)
    
    # Есть ли доводчик
    has_soft_close = Column(Boolean, default=False)
    
    # Производитель
    manufacturer = Column(String(100), nullable=True)
    
    # Артикул
    vendor_code = Column(String(50), nullable=True)
    
    # Цена в копейках
    price = Column(Integer, default=0)
    
    is_active = Column(String(10), default="active")

    def __repr__(self):
        return f"<SlideGuide {self.name} {self.length}мм>"


class Hinge(Base):
    """
    Петли для фасадов.
    """
    __tablename__ = "hinges"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    
    # Название
    name = Column(String(100), nullable=False)
    
    # Тип петли
    hinge_type = Column(String(50), nullable=False)  # clip, slide_on, press, decorative
    
    # Тип крепления: вкладная, накладная, полунакладная, угловая
    mounting_type = Column(String(50), nullable=False)  # inset, overlay, half_overlay, corner
    
    # Угол открывания
    opening_angle = Column(Integer, default=110)  # 90, 110, 170, 180
    
    # Диаметр чашки в мм
    cup_diameter = Column(Integer, default=35)
    
    # Есть ли доводчик
    has_soft_close = Column(Boolean, default=False)
    
    # Есть ли интегрированный доводчик
    has_integrated_soft_close = Column(Boolean, default=False)
    
    # Производитель
    manufacturer = Column(String(100), nullable=True)
    
    # Артикул
    vendor_code = Column(String(50), nullable=True)
    
    # Цена в копейках
    price = Column(Integer, default=0)
    
    is_active = Column(String(10), default="active")

    def __repr__(self):
        return f"<Hinge {self.name} {self.opening_angle}°>"
