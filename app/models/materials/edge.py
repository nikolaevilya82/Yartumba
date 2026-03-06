"""
Кромочные материалы (связь с листовыми 1:1)
"""
import uuid
from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from app.core.db_setup import Base


class EdgeMaterial(Base):
    """
    Кромка для листовых материалов.
    Связь 1:1 с листовым материалом (какой кромкой кромят этот материал).
    """
    __tablename__ = "edge_materials"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    
    # Ссылка на листовой материал (какой материал кромят этой кромкой)
    sheet_material_id = Column(
        UUID(as_uuid=True),
        ForeignKey("sheet_materials.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
        unique=True  # 1:1
    )
    
    # Тип кромки: ABS, ПВХ, меламин, натуральный шпон, алюминий
    edge_type = Column(String(50), nullable=False)  # abs, pvc, melamine, veneer, aluminum
    
    # Толщина кромки в мм
    thickness = Column(Integer, nullable=False)  # 0.4, 0.5, 1.0, 2.0
    
    # Ширина кромки в мм (обычно на 2-3мм больше толщины материала)
    width = Column(Integer, nullable=False)
    
    # Название декора (должен совпадать с декором листового материала)
    decor_name = Column(String(100), nullable=False)
    
    # Артикул
    vendor_code = Column(String(50), nullable=True)
    
    # Цена за погонный метр в копейках
    price_per_meter = Column(Integer, default=0)
    
    is_active = Column(String(10), default="active")

    sheet_material = relationship("SheetMaterial", back_populates="edges")

    def __repr__(self):
        return f"<EdgeMaterial {self.edge_type} {self.thickness}мм {self.decor_name}>"
