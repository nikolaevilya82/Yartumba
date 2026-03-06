"""
Экспорт моделей товаров
"""
from app.models.goods.bookshelf import Bookshelf, BookshelfPart
from app.models.goods.nightstand import Nightstand, NightstandDrawer
from app.models.goods.dresser import Dresser, DresserDrawer
from app.models.catalog.material import FurnitureMaterial
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
    "NightstandDrawer",
    # Комоды
    "Dresser",
    "DresserDrawer",
    # Универсальная связь материалов
    "FurnitureMaterial",
    # Материалы
    "SheetMaterial",
    "SlideGuide",
    "Hinge",
    "EdgeMaterial",
    "Support",
    "WallMount",
]
