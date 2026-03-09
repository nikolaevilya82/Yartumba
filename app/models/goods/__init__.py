"""
Экспорт моделей товаров
"""
from app.models.goods.bookshelf import Bookshelf, BookshelfPart
from app.models.goods.nightstand import Nightstand
from app.models.goods.dresser import Dresser
from app.models.catalog.material import FurnitureMaterial
from app.models.components.drawer import Drawer
from app.models.materials import (
    SheetMaterial,
    SlideGuide, Hinge,
    EdgeMaterial,
    Support, WallMount
)

__all__ = [
    # Книжные полки
    "Bookshelf",
    "BookshelfPart",
    # Прикроватные тумбы
    "Nightstand",
    # Комоды
    "Dresser",
    # Универсальная связь материалов
    "FurnitureMaterial",
    # Выдвижные ящики
    "Drawer",
    # Материалы
    "SheetMaterial",
    "SlideGuide",
    "Hinge",
    "EdgeMaterial",
    "Support",
    "WallMount",
]
