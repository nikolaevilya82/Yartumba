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
    Связана с деталями (полки, боковины, задняя стенка) и материалами.
    """
    __tablename__ = "bookshelves"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    
    # Ссылка на товар из каталога
    product_id = Column(
        UUID(as_uuid=True),
        ForeignKey("products.id", ondelete="SET NULL"),
        nullable=True,
        index=True
    )
    
    # Размеры в мм
    width = Column(Integer, nullable=False)    # Ширина
    height = Column(Integer, nullable=False)   # Высота
    depth = Column(Integer, nullable=False)    # Глубина
    
    # Количество полок
    shelf_count = Column(Integer, nullable=False, default=3)
    
    # Тип: открытый / закрытый / комбинированный
    shelf_type = Column(String(50), nullable=False, default="open")  # open, closed, combined
    
    # Связи
    product = relationship("Product", backref="bookshelf")
    materials = relationship("BookshelfMaterial", back_populates="bookshelf", cascade="all, delete-orphan")
    parts = relationship("BookshelfPart", back_populates="bookshelf", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Bookshelf {self.width}x{self.height}x{self.depth}>"


class BookshelfMaterial(Base):
    """
    Материалы для книжной полки.
    Позволяет выбрать материал для корпуса и полок отдельно.
    """
    __tablename__ = "bookshelf_materials"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    bookshelf_id = Column(
        UUID(as_uuid=True),
        ForeignKey("bookshelves.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )
    
    # Тип элемента: корпус, полки, задняя стенка
    part_type = Column(String(50), nullable=False)  # body, shelf, back
    
    # Ссылка на материал (из справочника материалов)
    material_id = Column(UUID(as_uuid=True), nullable=True)
    
    # Цвет (если применимо)
    color_id = Column(UUID(as_uuid=True), nullable=True)

    bookshelf = relationship("Bookshelf", back_populates="materials")


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
    
    # Связь с компонентом (если есть)
    component_id = Column(UUID(as_uuid=True), nullable=True)

    bookshelf = relationship("Bookshelf", back_populates="parts")
