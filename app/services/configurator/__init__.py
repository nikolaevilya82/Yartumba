"""
Сервис конфигуратора — расчёт стоимости и валидация конфигураций

Структура:
- configurator_service.py — главный сервис (сборка)
- validators.py — валидация конфигураций
- calculators/ — расчёт стоимости по типам мебели
- material_options.py — получение списка материалов
- constants.py — константы (размеры, проценты)
- schemas.py — Pydantic схемы для конфигураций
"""

from app.services.configurator.configurator_service import (
    ConfiguratorService,
    create_configurator_service,
)
from app.services.configurator.validators import (
    get_validator,
    BaseValidator,
    NightstandValidator,
    BookshelfValidator,
    DresserValidator,
)
from app.services.configurator.material_options import get_material_options
from app.services.configurator.constants import (
    THICKNESS,
    GAP,
    WORK_COST_MULTIPLIER,
    DIMENSION_LIMITS,
    DRAWER_LIMITS,
    SHELF_LIMITS,
)

__all__ = [
    # Главный сервис
    "ConfiguratorService",
    "create_configurator_service",
    # Валидаторы
    "get_validator",
    "BaseValidator",
    "NightstandValidator",
    "BookshelfValidator",
    "DresserValidator",
    # Материалы
    "get_material_options",
    # Константы
    "THICKNESS",
    "GAP",
    "WORK_COST_MULTIPLIER",
    "DIMENSION_LIMITS",
    "DRAWER_LIMITS",
    "SHELF_LIMITS",
]
