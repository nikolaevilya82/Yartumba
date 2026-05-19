"""
Сервис конфигуратора — расчёт стоимости и валидация конфигураций

⚠️ ДЕПРЕЦИРОВАНО: Используйте новый пакет app.services.configurator

Новая структура:
- app/services/configurator/configurator_service.py — главный сервис
- app/services/configurator/validators.py — валидация
- app/services/configurator/calculators/ — расчёты по типам мебели
- app/services/configurator/material_options.py — материалы
- app/services/configurator/constants.py — константы
- app/services/configurator/schemas.py — Pydantic схемы

Пример использования:
    from app.services.configurator import create_configurator_service
    
    db = SessionLocal()
    service = create_configurator_service(db)
    
    # Валидация
    result = service.validate("nightstand", config)
    
    # Расчёт
    cost = service.calculate("nightstand", config)
    
    # Материалы
    options = service.get_material_options()
"""
from typing import Dict, Any
from app.core.db_setup import SessionLocal
from app.services.configurator import create_configurator_service as _create_service


# Обёртки для обратной совместимости
def get_materials_options() -> Dict[str, Any]:
    """⚠️ ДЕПРЕЦИРОВАНО: Используйте app.services.configurator.get_material_options"""
    db = SessionLocal()
    try:
        service = _create_service(db)
        return service.get_material_options()
    finally:
        db.close()


def calculate_nightstand_cost(config: Dict[str, Any]) -> Dict[str, Any]:
    """⚠️ ДЕПРЕЦИРОВАНО: Используйте app.services.configurator.ConfiguratorService.calculate"""
    db = SessionLocal()
    try:
        service = _create_service(db)
        return service.calculate("nightstand", config)
    finally:
        db.close()


def validate_nightstand_config(config: Dict[str, Any]) -> Dict[str, Any]:
    """⚠️ ДЕПРЕЦИРОВАНО: Используйте app.services.configurator.ConfiguratorService.validate"""
    db = SessionLocal()
    try:
        service = _create_service(db)
        return service.validate("nightstand", config)
    finally:
        db.close()


def validate_bookshelf_config(config: Dict[str, Any]) -> Dict[str, Any]:
    """⚠️ ДЕПРЕЦИРОВАНО: Используйте app.services.configurator.ConfiguratorService.validate"""
    db = SessionLocal()
    try:
        service = _create_service(db)
        return service.validate("bookshelf", config)
    finally:
        db.close()


def validate_dresser_config(config: Dict[str, Any]) -> Dict[str, Any]:
    """⚠️ ДЕПРЕЦИРОВАНО: Используйте app.services.configurator.ConfiguratorService.validate"""
    db = SessionLocal()
    try:
        service = _create_service(db)
        return service.validate("dresser", config)
    finally:
        db.close()


# Обёрнутый экземпляр (не рекомендуется использовать)
class ConfiguratorService:
    """⚠️ ДЕПРЕЦИРОВАНО: Используйте app.services.configurator.ConfiguratorService"""
    
    def __init__(self):
        self.db = SessionLocal()
        self._service = _create_service(self.db)
    
    def __del__(self):
        if hasattr(self, 'db'):
            self.db.close()
    
    def get_materials_options(self):
        return self._service.get_material_options()
    
    def calculate_nightstand_cost(self, config: Dict[str, Any]):
        return self._service.calculate("nightstand", config)
    
    def validate_nightstand_config(self, config: Dict[str, Any]):
        return self._service.validate("nightstand", config)
    
    def validate_bookshelf_config(self, config: Dict[str, Any]):
        return self._service.validate("bookshelf", config)
    
    def validate_dresser_config(self, config: Dict[str, Any]):
        return self._service.validate("dresser", config)


configurator_service = ConfiguratorService()
