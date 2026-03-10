"""
Листовые материалы (ДСП, МДФ, фанера, массив и т.д.)
Каждая запись - конкретная позиция на складе с конкретным декором и ценой.
"""
import uuid
from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from app.core.db_setup import Base


class SheetMaterial(Base):
    """
    Листовые материалы - конкретные позиции на складе.
    ДСП 16мм Дуб сонома, МДФ 18мм Белый и т.д.
    """
    __tablename__ = "sheet_materials"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    
    # Название с декором (ДСП 16мм Дуб сонома, МДФ 18мм Белый матовый)
    name = Column(String(200), nullable=False)
    
    # Тип материала: chipboard, mdf, ldsp, plywood, solid_wood, hdf
    material_type = Column(String(50), nullable=False, index=True)
    
    # Толщина в мм
    thickness = Column(Integer, nullable=False)
    
    # Стандартные размеры листа в мм
    standard_width = Column(Integer, nullable=False)
    standard_height = Column(Integer, nullable=False)
    
    # Декор
    decor_name = Column(String(100), nullable=True)  # Дуб сонома, Белый, Венге
    hex_code = Column(String(7), nullable=True)      # для визуализации
    texture_url = Column(String(500), nullable=True) # текстура
    
    # Единица измерения (лист, кв.м, пог.м)
    unit = Column(String(20), nullable=False, default="sheet")
    
    # Цена за единицу в копейках (уже с учётом декора)
    price = Column(Integer, default=0)
    
    # Описание
    description = Column(String(500), nullable=True)
    
    # Активен / архив
    is_active = Column(String(10), default="active")
    
    # Связи
    edges = relationship("EdgeMaterial", back_populates="sheet_material", cascade="all, delete-orphan")
    bookshelf_parts = relationship("BookshelfPart", back_populates="sheet_material")
    dresser_parts = relationship("DresserPart", back_populates="sheet_material")
    nightstand_parts = relationship("NightstandPart", back_populates="sheet_material")
    drawer_parts = relationship("DrawerPart", back_populates="sheet_material")

    def __repr__(self):
        return f"<SheetMaterial {self.name}>"


