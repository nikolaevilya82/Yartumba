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

__all__ = [
    # Catalog
    "Category",
    # Goods
    "Bookshelf",
    "BookshelfPart",
    "Nightstand",
    "Dresser",
    # Components
    "Drawer",
    # Catalog (continued)
    "Product",
    "AttributeType",
    "SizeUnit",
    "Attribute",
    "AttributeValue",
    "ProductAttribute",
    "ProductConfiguration",
    "ConfigurationItem",
]
