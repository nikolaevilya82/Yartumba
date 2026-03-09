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
    
    # ID изделия-владельца
    furniture_id = Column(
        UUID(as_uuid=True),
        ForeignKey("nightstands.id", ondelete="CASCADE"),
        nullable=True,
        index=True
    )
    
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

    def __repr__(self):
        return f"<Drawer {self.furniture_type} #{self.drawer_number}>"
