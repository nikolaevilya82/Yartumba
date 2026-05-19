"""
Калькулятор стоимости комода
"""
from typing import Dict, Any

from sqlalchemy.orm import Session

from app.services.configurator.calculators.furniture_calculator import FurnitureCostCalculator
from app.services.configurator.constants import GAP


class DresserCalculator(FurnitureCostCalculator):
    """Калькулятор для комодов"""

    def calculate(self, config: Dict[str, Any]) -> Dict[str, Any]:
        """
        Рассчитать стоимость комода
        
        Args:
            config: Конфигурация комода
            
        Returns:
            Детализация стоимости
        """
        # Размеры
        width = config.get("width", 1200)
        height = config.get("height", 850)
        depth = config.get("depth", 450)
        
        # Материалы
        body_material = config.get("bodyMaterial", {})
        sheet_material_id = body_material.get("sheetMaterialId")
        edge_material_id = body_material.get("edgeMaterialId")
        
        # Фурнитура
        hardware = config.get("hardware", {})
        hinge_id = hardware.get("hingeId")
        slide_guide_id = hardware.get("slideGuideId")
        
        # Ящики
        drawer_count = config.get("drawer_count", 3)
        
        # Расчёт площади (корпус + фасады)
        total_area, area_details = self.calculate_body_area(
            width=width,
            height=height,
            depth=depth,
            shelf_count=drawer_count - 1,  # полки между ящиками
            facade_count=drawer_count,
            has_back_panel=False
        )
        
        # Расчёт длины кромки
        total_edge, edge_details = self.calculate_edge_length(
            width=width,
            height=height,
            depth=depth,
            shelf_count=drawer_count - 1,
            facade_count=drawer_count,
            has_back_panel=False
        )
        
        # Стоимость материалов
        sheet_cost = self.calculate_sheet_cost(total_area, sheet_material_id)
        edge_cost = self.calculate_edge_cost(total_edge, edge_material_id)
        materials_cost = sheet_cost + edge_cost
        
        # Стоимость фурнитуры
        hinge_cost = self.calculate_hinge_cost(drawer_count, hinge_id)
        slide_cost = self.calculate_slide_cost(drawer_count, slide_guide_id)
        hardware_cost = hinge_cost + slide_cost
        
        # Стоимость работы (35% для комодов, больше фурнитуры)
        work_cost = self.add_work_cost(materials_cost, hardware_cost, rate=0.35)
        
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
                "hinges_count": drawer_count,
                "slides_count": drawer_count,
                "drawer_count": drawer_count,
            }
        )
