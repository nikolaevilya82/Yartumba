"""
Книжная полка / стеллаж
"""
import uuid
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from app.core.db_setup import Base


class Bookshelf(Base):
    """
    Книжная полка / стеллаж.
    """
    __tablename__ = "bookshelves"

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

    shelf_count = Column(Integer, nullable=False, default=3)
    shelf_type = Column(String(50), nullable=False, default="open")

    product = relationship("Product", backref="bookshelf")
    materials = relationship(
        "FurnitureMaterial",
        primaryjoin="and_(Bookshelf.id==foreign(FurnitureMaterial.furniture_id), "
                    "FurnitureMaterial.furniture_type=='bookshelf')",
        backref="bookshelf_ref",
        cascade="all, delete-orphan",
        viewonly=True
    )
    parts = relationship("BookshelfPart", back_populates="bookshelf", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Bookshelf {self.width}x{self.height}x{self.depth}>"


class BookshelfPart(Base):
    """
    Детали книжной полки с размерами для производства.
    Связь с компонентами (панели, фурнитура).
    """
    __tablename__ = "bookshelf_parts"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    bookshelf_id = Column(
        UUID(as_uuid=True),
        ForeignKey("bookshelves.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )
    
    # Название детали: боковина, полка, верх, низ, задняя стенка
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

    bookshelf = relationship("Bookshelf", back_populates="parts")
    sheet_material = relationship("SheetMaterial")
