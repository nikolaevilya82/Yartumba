"""
Экспорт моделей товаров
"""
from app.models.goods.bookshelf import Bookshelf, BookshelfMaterial, BookshelfPart
from app.models.goods.nightstand import Nightstand, NightstandMaterial, NightstandDrawer
from app.models.goods.dresser import Dresser, DresserMaterial, DresserDrawer

__all__ = [
    # Книжные полки
    "Bookshelf",
    "BookshelfMaterial", 
    "BookshelfPart",
    # Прикроватные тумбы
    "Nightstand",
    "NightstandMaterial",
    "NightstandDrawer",
    # Комоды
    "Dresser",
    "DresserMaterial",
    "DresserDrawer",
]
