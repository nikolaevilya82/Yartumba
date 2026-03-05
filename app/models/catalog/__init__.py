"""
Экспорт всех моделей каталога
"""
from app.models.catalog.category import Category
from app.models.catalog.product import Product
from app.models.catalog.attribute_type import AttributeType, SizeUnit
from app.models.catalog.attribute import Attribute, AttributeValue
from app.models.catalog.product_attribute import ProductAttribute
from app.models.catalog.product_configuration import ProductConfiguration, ConfigurationItem

__all__ = [
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
