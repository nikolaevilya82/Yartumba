"""
Универсальная связь материалов с изделиями
"""
import uuid
from sqlalchemy import Column, String, ForeignKey, Integer
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from app.core.db_setup import Base


class FurnitureMaterial(Base):
    """
    Универсальная связь материала с изделием мебели.
    """
    __tablename__ = "furniture_materials"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    
    # Тип изделия: bookshelf, nightstand, dresser
    furniture_type = Column(String(50), nullable=False, index=True)
    
    # ID конкретного изделия
    furniture_id = Column(UUID(as_uuid=True), nullable=False, index=True)
    
    # Тип элемента: body, shelf, facade, top, legs, back, drawer
    part_type = Column(String(50), nullable=False)
    
    # Листовой материал (для корпуса, полок, фасадов)
    sheet_material_id = Column(
        UUID(as_uuid=True),
        ForeignKey("sheet_materials.id", ondelete="SET NULL"),
        nullable=True,
        index=True
    )
    
    # Кромка
    edge_id = Column(
        UUID(as_uuid=True),
        ForeignKey("edge_materials.id", ondelete="SET NULL"),
        nullable=True,
        index=True
    )
    
    # Направляющие (для ящиков)
    slide_guide_id = Column(
        UUID(as_uuid=True),
        ForeignKey("slide_guides.id", ondelete="SET NULL"),
        nullable=True,
        index=True
    )
    
    # Петли (для фасадов)
    hinge_id = Column(
        UUID(as_uuid=True),
        ForeignKey("hinges.id", ondelete="SET NULL"),
        nullable=True,
        index=True
    )
    
    # Опоры/ножки
    support_id = Column(
        UUID(as_uuid=True),
        ForeignKey("supports.id", ondelete="SET NULL"),
        nullable=True,
        index=True
    )
    
    # Крепление для подвесных
    wall_mount_id = Column(
        UUID(as_uuid=True),
        ForeignKey("wall_mounts.id", ondelete="SET NULL"),
        nullable=True,
        index=True
    )
    
    # Количество (например, 4 ножки, 2 петли)
    quantity = Column(Integer, default=1)
    
    # Связи
    sheet_material = relationship("SheetMaterial", foreign_keys=[sheet_material_id])
    edge = relationship("EdgeMaterial", foreign_keys=[edge_id])
    slide_guide = relationship("SlideGuide", foreign_keys=[slide_guide_id])
    hinge = relationship("Hinge", foreign_keys=[hinge_id])
    support = relationship("Support", foreign_keys=[support_id])
    wall_mount = relationship("WallMount", foreign_keys=[wall_mount_id])

    def __repr__(self):
        return f"<FurnitureMaterial {self.furniture_type}/{self.part_type}>"
