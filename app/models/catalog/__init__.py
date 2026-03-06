"""
Экспорт всех моделей каталога
"""
from app.models.catalog.category import Category
from app.models.catalog.product import Product
from app.models.catalog.attribute_type import AttributeType, SizeUnit
from app.models.catalog.attribute import Attribute, AttributeValue
from app.models.catalog.product_attribute import ProductAttribute
from app.models.catalog.product_configuration import ProductConfiguration, ConfigurationItem
from app.models.catalog.material import FurnitureMaterial

__all__ = [
    # Category
    "Category",
    # Product
    "Product",
    # Attributes
    "AttributeType",
    "SizeUnit",
    "Attribute",
    "AttributeValue",
    "ProductAttribute",
    # Configuration
    "ProductConfiguration",
    "ConfigurationItem",
    # Materials link
    "FurnitureMaterial",
]
