"""
Калькулятор стоимости книжной полки
"""
from decimal import Decimal
from typing import Dict, Any
from uuid import UUID

from app.services.configurator.calculators.furniture_calculator import FurnitureCostCalculator


class BookshelfCalculator(FurnitureCostCalculator):
    """Калькулятор для книжных полок"""

    def calculate(self, config: Dict[str, Any]) -> Dict[str, Any]:
        """
        Рассчитать стоимость полки

        Материал считается по объёму изделия (габаритные размеры).
        BOM формируется отдельно при оформлении заказа.

        Args:
            config: Конфигурация полки
            
        Returns:
            Детализация стоимости
        """
        # Размеры
        width = config.get("width", 800)
        height = config.get("height", 1800)
        depth = config.get("depth", 300)
        
        # Материалы
        body_material = config.get("bodyMaterial", {})
        sheet_material_id = body_material.get("sheetMaterialId")

        # Количество полок
        shelf_count = config.get("shelf_count", 3)
        shelf_type = config.get("shelf_type", "closed")
        has_back_panel = shelf_type == "closed"
        
        # Стоимость материала по объёму изделия
        materials_cost = self.calculate_volume_material_cost(
            width=width,
            height=height,
            depth=depth,
            material_id=UUID(sheet_material_id) if sheet_material_id else None,
        )
        
        # Фурнитура (для полок пока отсутствует)
        hardware_cost = Decimal("0")

        # Стоимость работы и итог
        work_cost = self.add_work_cost(materials_cost, hardware_cost, rate=0.25)
        total_cost = self.calculate_total(materials_cost, hardware_cost, work_cost)
        
        # Формируем результат
        return self.format_result(
            materials_cost=materials_cost,
            hardware_cost=hardware_cost,
            work_cost=work_cost,
            total_cost=total_cost,
            details={
                "volume_m3": round((width * height * depth) / 1_000_000_000, 6),
                "shelf_count": shelf_count,
                "has_back_panel": has_back_panel,
            },
        )
