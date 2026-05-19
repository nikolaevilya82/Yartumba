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

# Корзина
from app.models.cart import Cart, CartItem

__all__ = [
    # Catalog
    "Category",
    "Product",
    "FurnitureMaterial",
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
    # Cart
    "Cart",
    "CartItem",
    # Catalog (continued)
    "AttributeType",
    "SizeUnit",
    "Attribute",
    "AttributeValue",
    "ProductAttribute",
    "ProductConfiguration",
    "ConfigurationItem",
]
