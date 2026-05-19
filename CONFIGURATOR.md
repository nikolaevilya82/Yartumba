# Рефакторинг конфигуратора

## 📋 Что было изменено

### Проблема
Файл `app/services/configurator_service.py` (200+ строк) нарушал принципы SOLID:
- ❌ **Single Responsibility**: один класс делал всё (валидация, расчёты, получение материалов)
- ❌ **Open/Closed**: добавление нового типа мебели требовало изменения класса
- ❌ **Dependency Inversion**: прямая зависимость от `SessionLocal()`
- ❌ **DRY**: дублирование кода для разных типов мебели

### Решение
Разбит монолитный сервис на модули по принципу разделения ответственности.

---

## 🏗️ Новая структура

```
app/services/configurator/
├── __init__.py                     # Экспорт главного сервиса
├── configurator_service.py         # Главный сервис (сборка)
├── validators.py                   # Валидация конфигураций
├── material_options.py             # Получение списка материалов
├── constants.py                    # Константы (размеры, проценты)
├── schemas.py                      # Pydantic схемы для конфигураций
└── calculators/
    ├── __init__.py                 # Фабрика калькуляторов
    ├── base_calculator.py          # Базовый класс для расчётов
    ├── nightstand_calculator.py    # Расчёт тумбы
    ├── bookshelf_calculator.py     # Расчёт полки
    └── dresser_calculator.py       # Расчёт комода
```

---

## ✅ Принципы SOLID после рефакторинга

### Single Responsibility Principle (SRP)
Каждый класс отвечает за одну задачу:
- `ConfiguratorService` — оркестрация (валидация + расчёт)
- `NightstandValidator/BookshelfValidator/DresserValidator` — валидация
- `NightstandCalculator/BookshelfCalculator/DresserCalculator` — расчёт стоимости
- `get_material_options` — получение материалов

### Open/Closed Principle (OCP)
Добавление нового типа мебели:
1. Создать `new_furniture_calculator.py` наследуя `BaseCostCalculator`
2. Создать `NewFurnitureValidator` наследуя `BaseValidator`
3. Добавить в фабрики в `calculators/__init__.py` и `validators.py`

**Не нужно менять существующий код!**

### Liskov Substitution Principle (LSP)
Все калькуляторы и валидаторы заменяемы через базовые классы.

### Interface Segregation Principle (ISP)
Минимальные интерфейсы:
- `BaseCostCalculator` — только методы расчёта
- `BaseValidator` — только метод валидации

### Dependency Inversion Principle (DIP)
- Высокоуровневые модули не зависят от низкоуровневых
- Инъекция зависимости через `db: Session`
- Фабрики создают объекты динамически

---

## 📖 Использование

### Новый API

```python
from app.services.configurator import create_configurator_service
from sqlalchemy.orm import Session

# Создание сервиса
db: Session = SessionLocal()
service = create_configurator_service(db)

# Валидация
result = service.validate("nightstand", config)
if not result["valid"]:
    print("Errors:", result["errors"])

# Расчёт стоимости
cost = service.calculate("nightstand", config)
print(f"Total: {cost['total_price']} руб.")
print(f"Materials: {cost['materials_cost']} руб.")
print(f"Hardware: {cost['hardware_cost']} руб.")
print(f"Work: {cost['work_cost']} руб.")

# Получение материалов
options = service.get_material_options()
sheet_materials = options["sheet_materials"]
```

### Фабрики

```python
# Валидатор
from app.services.configurator.validators import get_validator

validator = get_validator("nightstand")
result = validator.validate(config)

# Калькулятор
from app.services.configurator.calculators import get_calculator

calculator = get_calculator("bookshelf", db)
cost = calculator.calculate(config)
```

### Константы

```python
from app.services.configurator.constants import DIMENSION_LIMITS, WORK_COST_MULTIPLIER

limits = DIMENSION_LIMITS["nightstand"]
print(f"Width: {limits['width']['min']} - {limits['width']['max']} мм")
```

### Pydantic схемы

```python
from app.services.configurator.schemas import NightstandConfig, CostBreakdown

config = NightstandConfig(width=500, height=500, depth=400)
cost = CostBreakdown(**cost_dict)
```

---

## 🔄 Обратная совместимость

Старый API продолжает работать через обёртки:

```python
# ⚠️ ДЕПРЕЦИРОВАНО - используйте новый API
from app.services.configurator_service import (
    get_materials_options,
    calculate_nightstand_cost,
    validate_nightstand_config,
    validate_bookshelf_config,
    validate_dresser_config,
)
```

**Рекомендация:** Постепенно мигрировать на новый API `app.services.configurator`.

---

## 🧪 Тестирование

Все существующие тесты проходят:

```bash
python3 -m pytest tests/integration/test_configurator_validation.py -v
# 12 passed
```

---

## 📊 Преимущества рефакторинга

| Аспект | До | После |
|--------|----|----|
| **Строк кода** | 200+ в одном файле | ~500 по модулям |
| **Расширяемость** | Требует изменения класса | Добавление нового класса |
| **Тестируемость** | Сложно тестировать | Каждый модуль тестируется отдельно |
| **Понятность** | Монолит | Чёткое разделение ответственности |
| **Поддержка** | Трудно поддерживать | Легко находить и исправлять |

---

## 🚀 Дальнейшие шаги

1. ✅ Добавить калькуляторы для всех типов мебели
2. 🔄 Перенести API эндпоинты на новый сервис
3. 📝 Добавить unit тесты для калькуляторов
4. 📊 Добавить кэширование материалов
5. 🔧 Добавить поддержку кастомных конфигураций

---

*Рефакторинг завершён ✅*
