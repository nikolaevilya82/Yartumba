# Универсальный калькулятор стоимости мебели

**Файл:** `app/services/configurator/calculators/furniture_calculator.py`

## Назначение

Содержит общую логику расчёта стоимости для всех типов изделий (тумбы, полки, комоды). Устраняет дублирование кода между калькуляторами.

## Принцип расчёта

**Материал** считается по объёму изделия (габаритные размеры):
```
объём_м³ = (ширина × высота × глубина) / 1_000_000_000
цена_за_м³ = price_листа / (площадь_листа_м² × толщина_м)
materials_cost = объём_м³ × цена_за_м³
```

**BOM** (спецификация деталей) формируется отдельно при оформлении заказа.

## Класс `FurnitureCostCalculator`

### Методы расчёта стоимости

```python
# Материал по объёму изделия (новый подход)
materials_cost = calculator.calculate_volume_material_cost(
    width=500,
    height=600,
    depth=400,
    material_id=uuid
)

# Петли (цена за штуку)
hinge_cost = calculator.calculate_hinge_cost(count=4, hinge_id=uuid)

# Направляющие (цена за пару)
slide_cost = calculator.calculate_slide_cost(count=2, guide_id=uuid)
```

### Итоговые методы

```python
# Стоимость работы (% от материалов + фурнитура)
work_cost = calculator.add_work_cost(
    materials_cost=5000,
    hardware_cost=2000,
    rate=0.3  # 30%
)

# Итоговая сумма
total = calculator.calculate_total(
    materials_cost=5000,
    hardware_cost=2000,
    work_cost=2100
)

# Форматирование результата
result = calculator.format_result(
    materials_cost=5000,
    hardware_cost=2000,
    work_cost=2100,
    total_cost=9100,
    details={"volume_m3": 0.12}
)
```

## Использование в калькуляторах

Все специфичные калькуляторы наследуются от `FurnitureCostCalculator`:

```python
from app.services.configurator.calculators.furniture_calculator import FurnitureCostCalculator

class NightstandCalculator(FurnitureCostCalculator):
    def calculate(self, config: Dict[str, Any]) -> Dict[str, Any]:
        # Используем универсальные методы
        total_area, _ = self.calculate_body_area(...)
        total_edge, _ = self.calculate_edge_length(...)
        
        sheet_cost = self.calculate_sheet_cost(total_area, material_id)
        edge_cost = self.calculate_edge_cost(total_edge, edge_id)
        
        # ... специфичная логика ...
        
        return self.format_result(...)
```

## Преимущества

| До | После |
|----|----|
| Дублирование расчётов в 3 калькуляторах | Один универсальный модуль |
| Изменение формулы в 3 местах | Изменение в одном месте |
| Сложность поддержки | Чёткая структура |
| ~300 строк дублирования | ~180 строк универсального кода |

## Примеры

```python
from app.core.db_setup import SessionLocal
from app.services.configurator.calculators import get_calculator

db = SessionLocal()
try:
    calculator = get_calculator("nightstand", db)
    
    config = {
        "width": 500,
        "height": 600,
        "depth": 400,
        "bodyMaterial": {"sheetMaterialId": uuid, "edgeMaterialId": uuid},
        "hardware": {"hingeId": uuid, "slideGuideId": uuid},
        "drawers": {"count": 2}
    }
    
    result = calculator.calculate(config)
    # {
    #     "materials_cost": 3500,
    #     "hardware_cost": 1200,
    #     "work_cost": 1410,
    #     "total_price": 6110,
    #     "details": {...}
    # }
finally:
    db.close()
```