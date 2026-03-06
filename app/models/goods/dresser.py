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
    drawers = relationship("DresserDrawer", back_populates="dresser", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Dresser {self.width}x{self.height}x{self.depth}, {self.drawer_count} ящиков>"


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
