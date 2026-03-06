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
    drawers = relationship("NightstandDrawer", back_populates="nightstand", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Nightstand {self.width}x{self.height}x{self.depth}, {self.drawer_count} ящика>"


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
