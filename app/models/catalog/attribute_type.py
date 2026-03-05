"""
Типы атрибутов для конфигурации товаров
"""
from enum import Enum


class AttributeType(str, Enum):
    """Тип атрибута определяет как он обрабатывается"""
    SIZE = "size"           # размеры (ширина, высота, глубина)
    MATERIAL = "material"   # материалы (дуб, сосна, МДФ...)
    COLOR = "color"         # цвета (белый, чёрный...)
    HANDLE = "handle"       # тип ручек
    LEGS = "legs"           # тип ножек
    OPTION = "option"       # дополнительные опции


class SizeUnit(str, Enum):
    """Единицы измерения размеров"""
    MM = "mm"   # миллиметры
    CM = "cm"   # сантиметры
