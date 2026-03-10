"""
Выдвижные ящики (универсальные для всех типов мебели)
"""
import uuid
from sqlalchemy import Column, String, Integer, Boolean, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from app.core.db_setup import Base


class Drawer(Base):
    """
    Универсальный выдвижной ящик.
    Может использоваться в Nightstand, Dresser и других изделиях с ящиками.
    """
    __tablename__ = "drawers"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    
    # Тип изделия-владельца: nightstand, dresser
    furniture_type = Column(String(50), nullable=False, index=True)
    
    # ID изделия-владельца (связь через furniture_type + furniture_id)
    furniture_id = Column(UUID(as_uuid=True), nullable=False, index=True)

    # Номер ящика (1, 2, 3...)
    drawer_number = Column(Integer, nullable=False)
    
    # Позиция (для комодов): left, right, center, full
    position = Column(String(20), nullable=True)
    
    # Внутренние размеры в мм
    inner_width = Column(Integer, nullable=True)
    inner_height = Column(Integer, nullable=True)
    inner_depth = Column(Integer, nullable=True)
    
    # Тип направляющих: роликовые, шариковые, полновыкатные
    guide_type = Column(String(50), nullable=False, default="roller")
    
    # Есть ли доводчик
    has_soft_close = Column(Boolean, default=False)
    
    # Связь с направляющими (через FurnitureMaterial)
    slide_guide_id = Column(
        UUID(as_uuid=True),
        ForeignKey("slide_guides.id", ondelete="SET NULL"),
        nullable=True,
        index=True
    )
    
    slide_guide = relationship("SlideGuide", foreign_keys=[slide_guide_id])
    parts = relationship("DrawerPart", back_populates="drawer", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Drawer {self.furniture_type} #{self.drawer_number}>"


class DrawerPart(Base):
    """
    Детали выдвижного ящика с размерами для производства.
    Боковины, дно, фасад ящика.
    """
    __tablename__ = "drawer_parts"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    drawer_id = Column(
        UUID(as_uuid=True),
        ForeignKey("drawers.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )

    # Название детали: боковина_левая, боковина_правая, дно, фасад, направляющая
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

    drawer = relationship("Drawer", back_populates="parts")
    sheet_material = relationship("SheetMaterial")

