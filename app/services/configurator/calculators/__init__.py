"""
Калькуляторы стоимости мебели
"""
from app.services.configurator.calculators.furniture_calculator import FurnitureCostCalculator
from app.services.configurator.calculators.nightstand_calculator import NightstandCalculator
from app.services.configurator.calculators.bookshelf_calculator import BookshelfCalculator
from app.services.configurator.calculators.dresser_calculator import DresserCalculator

# Фабрика калькуляторов
CALCULATORS = {
    "nightstand": NightstandCalculator,
    "bookshelf": BookshelfCalculator,
    "dresser": DresserCalculator,
}


def get_calculator(furniture_type: str, db):
    """
    Получить калькулятор для типа мебели
    
    Args:
        furniture_type: Тип мебели (nightstand, bookshelf, dresser)
        db: Сессия базы данных
        
    Returns:
        Экземпляр калькулятора
        
    Raises:
        ValueError: Если тип мебели не поддерживается
    """
    calculator_class = CALCULATORS.get(furniture_type)
    if not calculator_class:
        raise ValueError(f"Unsupported furniture type: {furniture_type}")
    return calculator_class(db)


__all__ = [
    "FurnitureCostCalculator",
    "NightstandCalculator",
    "BookshelfCalculator",
    "DresserCalculator",
    "get_calculator",
]
