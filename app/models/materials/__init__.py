"""
Экспорт всех материалов
"""
from app.models.materials.sheet_materials import SheetMaterial, SheetMaterialDecor
from app.models.materials.hardware import SlideGuide, Hinge
from app.models.materials.edge import EdgeMaterial
from app.models.materials.supports import Support, WallMount

__all__ = [
    # Листовые материалы
    "SheetMaterial",
    "SheetMaterialDecor",
    # Фурнитура
    "SlideGuide",
    "Hinge",
    # Кромка
    "EdgeMaterial",
    # Опоры и крепления
    "Support",
    "WallMount",
]
