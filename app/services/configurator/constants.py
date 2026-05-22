"""
Константы для конфигуратора
"""

# Размеры материалов
THICKNESS = {
    "default": 16,  # мм, стандартная толщина ЛДСП
    "hdf": 3,
    "mdf": 16,
}

GAP = {
    "default": 4,  # мм, зазоры между фасадами
    "drawer": 2,
}

# Коэффициенты
WORK_COST_MULTIPLIER = 0.3  # 30% на работу
MATERIAL_WASTE_FACTOR = 1.1  # 10% на обрезки

# Валидация размеров по типам мебели
DIMENSION_LIMITS = {
    "nightstand": {
        "width": {"min": 300, "max": 800},
        "height": {"min": 300, "max": 800},
        "depth": {"min": 300, "max": 600},
    },
    "bookshelf": {
        "width": {"min": 400, "max": 2000},
        "height": {"min": 400, "max": 2400},
        "depth": {"min": 200, "max": 600},
    },
    "dresser": {
        "width": {"min": 600, "max": 1600},
        "height": {"min": 600, "max": 1200},
        "depth": {"min": 400, "max": 700},
    },
}

# Количество ящиков
DRAWER_LIMITS = {
    "nightstand": {"min": 1, "max": 3},
    "dresser": {"min": 1, "max": 6},
}

# Количество полок
SHELF_LIMITS = {
    "min": 1,
    "max": 10,
}
