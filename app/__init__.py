"""
Экспорт всех моделей приложения
"""
# Каталог
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
)

# Товары (мебель)
from app.models.goods import (
    Bookshelf,
    BookshelfPart,
    Nightstand,
    Dresser,
)

# Компоненты
from app.models.components import Drawer

# Материалы
from app.models.materials import (
    SheetMaterial,
    SlideGuide,
    Hinge,
    EdgeMaterial,
    Support,
    WallMount,
)

# Связь материалов с изделиями
from app.models.catalog.material import FurnitureMaterial

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
    "Dresser",
    # Components
    "Drawer",
    # Materials
    "SheetMaterial",
    "SlideGuide",
    "Hinge",
    "EdgeMaterial",
    "Support",
    "WallMount",
    # Material link
    "FurnitureMaterial",
]
