"""
Базовые компоненты для моделей
"""
from app.core.db_setup import Base
from app.models.components.drawer import Drawer

__all__ = [
    "Base",
    "Drawer",
]
