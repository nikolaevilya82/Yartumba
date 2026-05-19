"""
Калькулятор стоимости прикроватной тумбы
"""
from typing import Dict, Any
from decimal import Decimal

from sqlalchemy.orm import Session

from app.services.configurator.calculators.base_calculator import BaseCostCalculator
from app.services.configurator.constants import THICKNESS, GAP


class NightstandCalculator(BaseCostCalculator):
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
        height = config.get("height", 500)
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
        
        # Базовые параметры
        thickness = THICKNESS["default"]
        gap = GAP["default"]
        
        # Расчёт площади деталей (в мм², потом конвертируем в м²)
        side_area = 2 * (height * depth)
        shelf_area = (drawer_count - 1) * (width - 2 * thickness) * depth
        top_bottom_area = 2 * (width * depth)
        facade_area = drawer_count * (width - gap) * (height / drawer_count)
        
        total_sheet_area_mm2 = side_area + shelf_area + top_bottom_area + facade_area
        total_sheet_area_m2 = total_sheet_area_mm2 / 1_000_000
        
        # Расчёт длины кромки (в мм)
        edge_length = (
            2 * (height + depth) * 2 +  # боковины
            2 * (width + depth) * (drawer_count + 1) +  # полки и верх/низ
            2 * (width + height / drawer_count) * drawer_count  # фасады
        )
        
        # Стоимость материалов
        sheet_cost = self._calculate_sheet_cost(total_sheet_area_m2, sheet_material_id)
        edge_cost = self._calculate_edge_cost(edge_length, edge_material_id)
        
        materials_cost = sheet_cost + edge_cost
        
        # Стоимость фурнитуры
        hinge_cost = self._calculate_hinge_cost(drawer_count * 2, hinge_id)  # 2 петли на фасад
        slide_cost = self._calculate_slide_cost(drawer_count, slide_guide_id)
        
        hardware_cost = hinge_cost + slide_cost
        
        # Стоимость работы (30% от материалов + фурнитура)
        work_cost = self._add_work_cost(materials_cost + hardware_cost)
        
        # Итого
        total_cost = materials_cost + hardware_cost + work_cost
        
        return {
            "materials_cost": int(materials_cost),
            "hardware_cost": int(hardware_cost),
            "work_cost": int(work_cost),
            "total_price": int(total_cost),
            "details": {
                "sheet_material_area_m2": round(total_sheet_area_m2, 3),
                "edge_length_m": round(edge_length / 1000, 2) if edge_material_id else 0,
                "hinges_count": drawer_count * 2,
                "slides_count": drawer_count,
            }
        }
