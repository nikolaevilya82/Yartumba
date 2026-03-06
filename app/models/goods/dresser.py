"""
Комод
"""
import uuid
from sqlalchemy import Column, Integer, String, ForeignKey, Boolean
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from app.core.db_setup import Base


class Dresser(Base):
    """
    Комод.
    Широкий комод с множеством ящиков, часто в спальню.
    """
    __tablename__ = "dressers"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    
    # Ссылка на товар из каталога
    product_id = Column(
        UUID(as_uuid=True),
        ForeignKey("products.id", ondelete="SET NULL"),
        nullable=True,
        index=True
    )
    
    # Размеры в мм
    width = Column(Integer, nullable=False)
    height = Column(Integer, nullable=False)
    depth = Column(Integer, nullable=False)
    
    # Количество ящиков (обычно 4-6)
    drawer_count = Column(Integer, nullable=False, default=4)
    
    # Количество рядов ящиков
    drawer_rows = Column(Integer, nullable=False, default=2)
    
    # Тип комода: стандартный, с зеркалом, угловой
    dresser_type = Column(String(50), nullable=False, default="standard")  # standard, with_mirror, corner
    
    # Есть ли ножки или стоит на полу
    has_legs = Column(Boolean, default=True)
    
    # Связи
    product = relationship("Product", backref="dresser")
    materials = relationship("DresserMaterial", back_populates="dresser", cascade="all, delete-orphan")
    drawers = relationship("DresserDrawer", back_populates="dresser", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Dresser {self.width}x{self.height}x{self.depth}, {self.drawer_count} ящиков>"


class DresserMaterial(Base):
    """
    Материалы для комода.
    """
    __tablename__ = "dresser_materials"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    dresser_id = Column(
        UUID(as_uuid=True),
        ForeignKey("dressers.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )
    
    part_type = Column(String(50), nullable=False)  # body, facade, top, legs
    material_id = Column(UUID(as_uuid=True), nullable=True)
    color_id = Column(UUID(as_uuid=True), nullable=True)

    dresser = relationship("Dresser", back_populates="materials")


class DresserDrawer(Base):
    """
    Ящик комода.
    Может быть разного размера (верхние узкие, нижние широкие).
    """
    __tablename__ = "dresser_drawers"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    dresser_id = Column(
        UUID(as_uuid=True),
        ForeignKey("dressers.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )
    
    drawer_number = Column(Integer, nullable=False)
    
    # Позиция: left, right, center, full
    position = Column(String(20), nullable=False, default="full")
    
    # Размеры в мм
    inner_width = Column(Integer, nullable=True)
    inner_height = Column(Integer, nullable=True)
    inner_depth = Column(Integer, nullable=True)
    
    guide_type = Column(String(50), nullable=False, default="roller")
    has_soft_close = Column(Boolean, default=False)

    dresser = relationship("Dresser", back_populates="drawers")
