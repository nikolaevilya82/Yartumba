"""
Экспорт моделей товаров
"""
from app.models.goods.bookshelf import Bookshelf, BookshelfPart
from app.models.goods.nightstand import Nightstand, NightstandPart
from app.models.goods.dresser import Dresser, DresserPart
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
    "NightstandPart",
    # Комоды
    "Dresser",
    "DresserPart",
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
