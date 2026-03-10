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
    """
    __tablename__ = "dressers"

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
    
    drawer_count = Column(Integer, nullable=False, default=4)
    drawer_rows = Column(Integer, nullable=False, default=2)
    dresser_type = Column(String(50), nullable=False, default="standard")
    has_legs = Column(Boolean, default=True)
    
    product = relationship("Product", backref="dresser")
    materials = relationship(
        "FurnitureMaterial",
        primaryjoin="and_(Dresser.id==foreign(FurnitureMaterial.furniture_id), "
                    "FurnitureMaterial.furniture_type=='dresser')",
        backref="dresser_ref",
        cascade="all, delete-orphan",
        viewonly=True
    )
    parts = relationship("DresserPart", back_populates="dresser", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Dresser {self.width}x{self.height}x{self.depth}, {self.drawer_count} ящиков>"


class DresserPart(Base):
    """
    Детали комода с размерами для производства.
    Связь с компонентами (панели, фурнитура).
    """
    __tablename__ = "dresser_parts"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    dresser_id = Column(
        UUID(as_uuid=True),
        ForeignKey("dressers.id", ondelete="CASCADE"),
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

    dresser = relationship("Dresser", back_populates="parts")
    sheet_material = relationship("SheetMaterial")


