"""
Калькулятор стоимости прикроватной тумбы
"""
from typing import Dict, Any

from sqlalchemy.orm import Session

from app.services.configurator.calculators.furniture_calculator import FurnitureCostCalculator
from app.services.configurator.constants import GAP


class NightstandCalculator(FurnitureCostCalculator):
    """Калькулятор для прикроватных тумб"""

    def calculate(self, config: Dict[str, Any]) -> Dict[str, Any]:
        """
        Рассчитать стоимость тумбы
        
        Args:
            config: Конфигурация тумбы
            
        Returns:
            Детализация стоимости
        """
        # Размеры
        width = config.get("width", 500)
        height = config.get("height", 600)
        depth = config.get("depth", 400)
        
        # Материалы
        body_material = config.get("bodyMaterial", {})
        sheet_material_id = body_material.get("sheetMaterialId")
        edge_material_id = body_material.get("edgeMaterialId")
        
        # Фурнитура
        hardware = config.get("hardware", {})
        hinge_id = hardware.get("hingeId")
        slide_guide_id = hardware.get("slideGuideId")
        
        # Ящики
        drawers = config.get("drawers", {})
        drawer_count = drawers.get("count", 1)
        
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
        hinge_cost = self.calculate_hinge_cost(drawer_count * 2, hinge_id)
        slide_cost = self.calculate_slide_cost(drawer_count, slide_guide_id)
        hardware_cost = hinge_cost + slide_cost
        
        # Стоимость работы (30%)
        work_cost = self.add_work_cost(materials_cost, hardware_cost, rate=0.3)
        
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
                "hinges_count": drawer_count * 2,
                "slides_count": drawer_count,
            }
        )
