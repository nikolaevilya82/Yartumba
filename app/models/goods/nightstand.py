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
    """
    __tablename__ = "nightstands"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    
    product_id = Column(
        UUID(as_uuid=True),
        ForeignKey("products.id", ondelete="SET NULL"),
        nullable=True,
        index=True
    )
    
    width = Column(Integer, nullable=False)
    height = Column(Integer, nullable=False)
    depth = Column(Integer, nullable=False)
    
    drawer_count = Column(Integer, nullable=False, default=1)
    has_open_shelf = Column(Boolean, default=False)
    leg_type = Column(String(50), nullable=False, default="standard")
    
    product = relationship("Product", backref="nightstand")
    materials = relationship(
        "FurnitureMaterial",
        primaryjoin="and_(Nightstand.id==foreign(FurnitureMaterial.furniture_id), "
                    "FurnitureMaterial.furniture_type=='nightstand')",
        backref="nightstand_ref",
        cascade="all, delete-orphan",
        viewonly=True
    )
    parts = relationship("NightstandPart", back_populates="nightstand", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Nightstand {self.width}x{self.height}x{self.depth}, {self.drawer_count} ящика>"


class NightstandPart(Base):
    """
    Детали прикроватной тумбы с размерами для производства.
    """
    __tablename__ = "nightstand_parts"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    nightstand_id = Column(
        UUID(as_uuid=True),
        ForeignKey("nightstands.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )

    # Название детали: боковина, полка, верх, низ, задняя стенка, фасад
    name = Column(String(100), nullable=False)

    # Размеры детали в мм
    part_width = Column(Integer, nullable=True)
    part_height = Column(Integer, nullable=True)
    part_depth = Column(Integer, nullable=True)

    # Количество таких деталей
    quantity = Column(Integer, nullable=False, default=1)

    # Связь с листовым материалом (для разных цветов деталей)
    sheet_material_id = Column(
        UUID(as_uuid=True),
        ForeignKey("sheet_materials.id", ondelete="SET NULL"),
        nullable=True,
        index=True
    )

    nightstand = relationship("Nightstand", back_populates="parts")
    sheet_material = relationship("SheetMaterial")


