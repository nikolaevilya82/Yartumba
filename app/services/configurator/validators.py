"""
Валидация конфигураций мебели
"""
from typing import Dict, Any, List
from abc import ABC, abstractmethod

from app.services.configurator.constants import (
    DIMENSION_LIMITS,
    DRAWER_LIMITS,
    SHELF_LIMITS,
)


class BaseValidator(ABC):
    """Базовый класс для валидаторов"""

    @abstractmethod
    def validate(self, config: Dict[str, Any]) -> Dict[str, Any]:
        """
        Валидировать конфигурацию
        
        Args:
            config: Конфигурация изделия
            
        Returns:
            Результат валидации
        """
        pass


class NightstandValidator(BaseValidator):
    """Валидатор для прикроватных тумб"""

    def validate(self, config: Dict[str, Any]) -> Dict[str, Any]:
        """Валидация конфигурации тумбы"""
        errors = []
        
        # Размеры
        limits = DIMENSION_LIMITS["nightstand"]
        width = config.get("width", 0)
        height = config.get("height", 0)
        depth = config.get("depth", 0)
        
        if width < limits["width"]["min"] or width > limits["width"]["max"]:
            errors.append(
                f"Ширина должна быть от {limits['width']['min']} до {limits['width']['max']} мм"
            )
        
        if height < limits["height"]["min"] or height > limits["height"]["max"]:
            errors.append(
                f"Высота должна быть от {limits['height']['min']} до {limits['height']['max']} мм"
            )
        
        if depth < limits["depth"]["min"] or depth > limits["depth"]["max"]:
            errors.append(
                f"Глубина должна быть от {limits['depth']['min']} до {limits['depth']['max']} мм"
            )
        
        # Ящики
        drawer_limits = DRAWER_LIMITS["nightstand"]
        drawer_count = config.get("drawers", {}).get("count", 0)
        
        if drawer_count < drawer_limits["min"] or drawer_count > drawer_limits["max"]:
            errors.append(
                f"Количество ящиков должно быть от {drawer_limits['min']} до {drawer_limits['max']}"
            )
        
        # Материалы
        if not config.get("bodyMaterial", {}).get("sheetMaterialId"):
            errors.append("Выберите листовой материал")
        
        return {
            "valid": len(errors) == 0,
            "errors": errors,
        }


class BookshelfValidator(BaseValidator):
    """Валидатор для книжных полок"""

    def validate(self, config: Dict[str, Any]) -> Dict[str, Any]:
        """Валидация конфигурации полки"""
        errors = []
        
        # Размеры
        limits = DIMENSION_LIMITS["bookshelf"]
        width = config.get("width", 0)
        height = config.get("height", 0)
        depth = config.get("depth", 0)
        
        if width < limits["width"]["min"] or width > limits["width"]["max"]:
            errors.append(
                f"Ширина должна быть от {limits['width']['min']} до {limits['width']['max']} мм"
            )
        
        if height < limits["height"]["min"] or height > limits["height"]["max"]:
            errors.append(
                f"Высота должна быть от {limits['height']['min']} до {limits['height']['max']} мм"
            )
        
        if depth < limits["depth"]["min"] or depth > limits["depth"]["max"]:
            errors.append(
                f"Глубина должна быть от {limits['depth']['min']} до {limits['depth']['max']} мм"
            )
        
        # Полки
        shelf_count = config.get("shelf_count", 0)
        
        if shelf_count < SHELF_LIMITS["min"] or shelf_count > SHELF_LIMITS["max"]:
            errors.append(
                f"Количество полок должно быть от {SHELF_LIMITS['min']} до {SHELF_LIMITS['max']}"
            )
        
        # Материалы
        if not config.get("bodyMaterial", {}).get("sheetMaterialId"):
            errors.append("Выберите листовой материал")
        
        return {
            "valid": len(errors) == 0,
            "errors": errors,
        }


class DresserValidator(BaseValidator):
    """Валидатор для комодов"""

    def validate(self, config: Dict[str, Any]) -> Dict[str, Any]:
        """Валидация конфигурации комода"""
        errors = []
        
        # Размеры
        limits = DIMENSION_LIMITS["dresser"]
        width = config.get("width", 0)
        height = config.get("height", 0)
        depth = config.get("depth", 0)
        
        if width < limits["width"]["min"] or width > limits["width"]["max"]:
            errors.append(
                f"Ширина должна быть от {limits['width']['min']} до {limits['width']['max']} мм"
            )
        
        if height < limits["height"]["min"] or height > limits["height"]["max"]:
            errors.append(
                f"Высота должна быть от {limits['height']['min']} до {limits['height']['max']} мм"
            )
        
        if depth < limits["depth"]["min"] or depth > limits["depth"]["max"]:
            errors.append(
                f"Глубина должна быть от {limits['depth']['min']} до {limits['depth']['max']} мм"
            )
        
        # Ящики
        drawer_limits = DRAWER_LIMITS["dresser"]
        drawer_count = config.get("drawer_count", 0)
        
        if drawer_count < drawer_limits["min"] or drawer_count > drawer_limits["max"]:
            errors.append(
                f"Количество ящиков должно быть от {drawer_limits['min']} до {drawer_limits['max']}"
            )
        
        # Материалы
        if not config.get("bodyMaterial", {}).get("sheetMaterialId"):
            errors.append("Выберите листовой материал")
        
        return {
            "valid": len(errors) == 0,
            "errors": errors,
        }


# Фабрика валидаторов
VALIDATORS = {
    "nightstand": NightstandValidator(),
    "bookshelf": BookshelfValidator(),
    "dresser": DresserValidator(),
}


def get_validator(furniture_type: str) -> BaseValidator:
    """
    Получить валидатор для типа мебели
    
    Args:
        furniture_type: Тип мебели (nightstand, bookshelf, dresser)
        
    Returns:
        Валидатор
        
    Raises:
        ValueError: Если тип мебели не поддерживается
    """
    validator = VALIDATORS.get(furniture_type)
    if not validator:
        raise ValueError(f"Unsupported furniture type: {furniture_type}")
    return validator
