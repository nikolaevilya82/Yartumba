"""
Схемы Pydantic для книжных полок
"""
from uuid import UUID
from typing import Optional
from pydantic import BaseModel, Field

# Импорт общих схем
from app.api.v1.goods.schemas import (
    GoodsBase,
    GoodsCreate,
    GoodsUpdate,
    GoodsResponse,
    PartBase,
    PartCreate,
    PartUpdate,
    PartResponse,
)


# === Схемы для Bookshelf ===
class BookshelfCreate(GoodsCreate):
    """Создание книжной полки"""
    shelf_count: int = Field(default=3, ge=1, le=20, description="Количество полок")
    shelf_type: str = Field(default="open", description="Тип: open, closed, mixed")


class BookshelfUpdate(GoodsUpdate):
    """Обновление книжной полки"""
    shelf_count: Optional[int] = Field(None, ge=1, le=20)
    shelf_type: Optional[str] = None


class BookshelfResponse(GoodsResponse):
    """Ответ с книжной полкой"""
    shelf_count: int
    shelf_type: str

    class Config:
        from_attributes = True


# === Схемы для деталей BookshelfPart ===
class BookshelfPartBase(PartBase):
    """Базовая схема детали"""
    name: str = Field(..., description="Название детали: боковина, полка, верх, низ, задняя стенка")


class BookshelfPartCreate(PartCreate):
    """Создание детали"""
    pass


class BookshelfPartUpdate(PartUpdate):
    """Обновление детали"""
    pass


class BookshelfPartResponse(PartResponse):
    """Ответ с деталью"""
    bookshelf_id: UUID

    class Config:
        from_attributes = True


# === Схема для списка деталей ===
class BookshelfWithParts(BookshelfResponse):
    """Книжная полка с деталями"""
    parts: list[BookshelfPartResponse] = []

    class Config:
        from_attributes = True

