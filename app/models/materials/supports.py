"""
Опоры и крепления для навесной мебели
"""
import uuid
from sqlalchemy import Column, String, Integer, Boolean, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from app.core.db_setup import Base


class Support(Base):
    """
    Опоры: ножки, цоколи, подпятники.
    """
    __tablename__ = "supports"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    
    # Название
    name = Column(String(100), nullable=False)
    
    # Тип опоры: ножка, цоколь, подпятник, регулируемая опора
    support_type = Column(String(50), nullable=False)  # leg, plinth, foot, adjustable
    
    # Материал: пластик, металл, массив
    material = Column(String(50), nullable=True)  # plastic, metal, solid_wood
    
    # Высота в мм
    height = Column(Integer, nullable=True)
    
    # Диаметр или ширина в мм
    diameter = Column(Integer, nullable=True)
    width = Column(Integer, nullable=True)
    
    # Регулируется по высоте
    is_adjustable = Column(Boolean, default=False)
    
    # Цвет
    color = Column(String(50), nullable=True)
    
    # Производитель
    manufacturer = Column(String(100), nullable=True)
    
    # Артикул
    vendor_code = Column(String(50), nullable=True)
    
    # Цена за штуку в копейках
    price = Column(Integer, default=0)
    
    is_active = Column(String(10), default="active")

    def __repr__(self):
        return f"<Support {self.name} {self.support_type}>"


class WallMount(Base):
    """
    Крепления для подвесных тумб и шкафов.
    """
    __tablename__ = "wall_mounts"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    
    # Название
    name = Column(String(100), nullable=False)
    
    # Тип крепления: навеска, уголок, направляющая, рейка
    mount_type = Column(String(50), nullable=False)  # hanger, bracket, rail, strip
    
    # Тип стены: гипсокартон, бетон, кирпич
    wall_type = Column(String(50), nullable=True)  # drywall, concrete, brick
    
    # Максимальная нагрузка на крепление в кг
    max_load = Column(Integer, default=50)
    
    # Регулировка: по высоте, глубине, горизонтали
    adjustment = Column(String(100), nullable=True)  # height, depth, horizontal, 3d
    
    # Скрытый/видимый
    is_hidden = Column(Boolean, default=True)
    
    # Производитель
    manufacturer = Column(String(100), nullable=True)
    
    # Артикул
    vendor_code = Column(String(50), nullable=True)
    
    # Цена за штуку в копейках
    price = Column(Integer, default=0)
    
    is_active = Column(String(10), default="active")

    def __repr__(self):
        return f"<WallMount {self.name} {self.mount_type}>"
