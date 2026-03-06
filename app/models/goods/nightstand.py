"""
Прикроватная тумба
"""
import uuid
from sqlalchemy import Column, Integer, String, ForeignKey, Boolean
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from app.core.db_setup import Base


class Nightstand(Base):
    """
    Прикроватная тумба.
    Обычно с ящиками, может иметь открытую полку.
    """
    __tablename__ = "nightstands"

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
    
    # Количество ящиков
    drawer_count = Column(Integer, nullable=False, default=1)
    
    # Есть ли открытая полка
    has_open_shelf = Column(Boolean, default=False)
    
    # Тип ножек: стандартные, накладные, царговые
    leg_type = Column(String(50), nullable=False, default="standard")
    
    # Связи
    product = relationship("Product", backref="nightstand")
    materials = relationship("NightstandMaterial", back_populates="nightstand", cascade="all, delete-orphan")
    drawers = relationship("NightstandDrawer", back_populates="nightstand", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Nightstand {self.width}x{self.height}x{self.depth}, {self.drawer_count} ящика>"


class NightstandMaterial(Base):
    """
    Материалы для прикроватной тумбы.
    """
    __tablename__ = "nightstand_materials"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    nightstand_id = Column(
        UUID(as_uuid=True),
        ForeignKey("nightstands.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )
    
    # Тип элемента: корпус, фасад, столешница, ножки
    part_type = Column(String(50), nullable=False)  # body, facade, top, legs
    
    material_id = Column(UUID(as_uuid=True), nullable=True)
    color_id = Column(UUID(as_uuid=True), nullable=True)

    nightstand = relationship("Nightstand", back_populates="materials")


class NightstandDrawer(Base):
    """
    Ящик прикроватной тумбы.
    """
    __tablename__ = "nightstand_drawers"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    nightstand_id = Column(
        UUID(as_uuid=True),
        ForeignKey("nightstands.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )
    
    # Номер ящика (1, 2, 3...)
    drawer_number = Column(Integer, nullable=False)
    
    # Внутренние размеры ящика в мм
    inner_width = Column(Integer, nullable=True)
    inner_height = Column(Integer, nullable=True)
    inner_depth = Column(Integer, nullable=True)
    
    # Тип направляющих: роликовые, шариковые, полновыкатные
    guide_type = Column(String(50), nullable=False, default="roller")
    
    # Есть ли доводчик
    has_soft_close = Column(Boolean, default=False)

    nightstand = relationship("Nightstand", back_populates="drawers")
