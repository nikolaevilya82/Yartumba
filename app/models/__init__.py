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

# Компоненты (заготовка для будущего)
# from app.models.components import ...

# Продажи (заготовка)
# from app.models.sales import ...

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
]
