"""
Главный сервис конфигуратора — сборка всех компонентов
"""
from typing import Dict, Any

from sqlalchemy.orm import Session

from app.services.configurator.validators import get_validator
from app.services.configurator.calculators import get_calculator
from app.services.configurator.material_options import get_material_options


class ConfiguratorService:
    """
    Сервис для работы с конфигуратором мебели
    
    Использует паттерны:
    - Factory (для создания валидаторов и калькуляторов)
    - Dependency Injection (через db)
    - Single Responsibility (каждый компонент отвечает за свою задачу)
    """

    def __init__(self, db: Session):
        """
        Args:
            db: Сессия базы данных
        """
        self.db = db

    def get_material_options(self) -> Dict[str, Any]:
        """
        Получить все доступные материалы и фурнитуру
        
        Returns:
            Словарь с категориями материалов
        """
        return get_material_options(self.db)

    def validate(self, furniture_type: str, config: Dict[str, Any]) -> Dict[str, Any]:
        """
        Валидировать конфигурацию
        
        Args:
            furniture_type: Тип мебели (nightstand, bookshelf, dresser)
            config: Конфигурация изделия
            
        Returns:
            Результат валидации
        """
        validator = get_validator(furniture_type)
        return validator.validate(config)

    def calculate(self, furniture_type: str, config: Dict[str, Any]) -> Dict[str, Any]:
        """
        Рассчитать стоимость
        
        Args:
            furniture_type: Тип мебели (nightstand, bookshelf, dresser)
            config: Конфигурация изделия
            
        Returns:
            Детализация стоимости
        """
        calculator = get_calculator(furniture_type, self.db)
        return calculator.calculate(config)


# Экспорт экземпляра сервиса (для обратной совместимости)
def create_configurator_service(db: Session) -> ConfiguratorService:
    """
    Создать экземпляр сервиса конфигуратора
    
    Args:
        db: Сессия базы данных
        
    Returns:
        Экземпляр ConfiguratorService
    """
    return ConfiguratorService(db)
