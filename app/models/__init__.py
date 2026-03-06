"""
Экспорт всех моделей проекта
"""
# Каталог (товары, атрибуты, категории)
from app.models.catalog import (
    Category,
    Product,
    AttributeType,
    SizeUnit,
    Attribute,
    AttributeValue,
    ProductAttribute,
    ProductConfiguration,
    ConfigurationItem,
    FurnitureMaterial,
)

# Товары (конкретные изделия)
from app.models.goods import (
    Bookshelf,
    BookshelfPart,
    Nightstand,
    NightstandDrawer,
    Dresser,
    DresserDrawer,
)

# Материалы
from app.models.materials import (
    SheetMaterial,
    SheetMaterialDecor,
    SlideGuide,
    Hinge,
    EdgeMaterial,
    Support,
    WallMount,
)

__all__ = [
    # Catalog
    "Category",
    "Product",
    "AttributeType",
    "SizeUnit",
    "Attribute",
    "AttributeValue",
    "ProductAttribute",
    "ProductConfiguration",
    "ConfigurationItem",
    # Goods
    "Bookshelf",
    "BookshelfPart",
    "Nightstand",
    "NightstandDrawer",
    "Dresser",
    "DresserDrawer",
    # Materials
    "SheetMaterial",
    "SheetMaterialDecor",
    "SlideGuide",
    "Hinge",
    "EdgeMaterial",
    "Support",
    "WallMount",
    # Material link
    "FurnitureMaterial",
]
