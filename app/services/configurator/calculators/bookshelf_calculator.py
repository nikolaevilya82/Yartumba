"""
Калькулятор стоимости книжной полки
"""
from typing import Dict, Any

from sqlalchemy.orm import Session

from app.services.configurator.calculators.furniture_calculator import FurnitureCostCalculator


class BookshelfCalculator(FurnitureCostCalculator):
    """Калькулятор для книжных полок"""

    def calculate(self, config: Dict[str, Any]) -> Dict[str, Any]:
        """
        Рассчитать стоимость полки
        
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
        edge_material_id = body_material.get("edgeMaterialId")
        
        # Количество полок
        shelf_count = config.get("shelf_count", 3)
        shelf_type = config.get("shelf_type", "closed")
        
        # Расчёт площади
        total_area, area_details = self.calculate_body_area(
            width=width,
            height=height,
            depth=depth,
            shelf_count=shelf_count - 1,  # внутренние полки
            facade_count=0,
            has_back_panel=(shelf_type == "closed")
        )
        
        # Расчёт длины кромки
        total_edge, edge_details = self.calculate_edge_length(
            width=width,
            height=height,
            depth=depth,
            shelf_count=shelf_count - 1,
            facade_count=0,
            has_back_panel=(shelf_type == "closed")
        )
        
        # Стоимость материалов
        sheet_cost = self.calculate_sheet_cost(total_area, sheet_material_id)
        edge_cost = self.calculate_edge_cost(total_edge, edge_material_id)
        materials_cost = sheet_cost + edge_cost
        
        # Фурнитура для полок (крепежи, уголки) - пока 0
        hardware_cost = 0
        
        # Стоимость работы (25% для полок)
        work_cost = self.add_work_cost(materials_cost, hardware_cost, rate=0.25)
        
        # Итого
        total_cost = self.calculate_total(materials_cost, hardware_cost, work_cost)
        
        # Формируем результат
        return self.format_result(
            materials_cost=materials_cost,
            hardware_cost=hardware_cost,
            work_cost=work_cost,
            total_cost=total_cost,
            details={
                "sheet_material_area_m2": round(total_area, 3),
                "edge_length_m": round(total_edge / 1000, 2) if edge_material_id else 0,
                "area_breakdown": area_details,
                "edge_breakdown": edge_details,
                "shelf_count": shelf_count,
                "has_back_panel": shelf_type == "closed",
            }
        )
