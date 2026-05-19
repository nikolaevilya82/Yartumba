"""
Калькулятор стоимости книжной полки
"""
from typing import Dict, Any
from decimal import Decimal

from sqlalchemy.orm import Session

from app.services.configurator.calculators.base_calculator import BaseCostCalculator
from app.services.configurator.constants import THICKNESS, SHELF_LIMITS


class BookshelfCalculator(BaseCostCalculator):
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
        
        # Базовые параметры
        thickness = THICKNESS["default"]
        
        # Расчёт площади деталей (в мм²)
        side_area = 2 * (height * depth)  # боковины
        
        # Полки: (shelf_count - 1) внутренних полок
        shelf_area = (shelf_count - 1) * (width - 2 * thickness) * depth
        
        # Верх и низ
        top_bottom_area = 2 * (width * depth)
        
        # Задняя стенка (если закрытая)
        back_area = 0
        if shelf_type == "closed":
            back_area = width * height
        
        total_sheet_area_mm2 = side_area + shelf_area + top_bottom_area + back_area
        total_sheet_area_m2 = total_sheet_area_mm2 / 1_000_000
        
        # Расчёт длины кромки (в мм)
        edge_length = (
            2 * (height + depth) * 2 +  # боковины
            2 * (width + depth) * (shelf_count + 1)  # полки и верх/низ
        )
        
        # Задняя стенка кромка (если есть)
        if shelf_type == "closed":
            edge_length += 2 * (width + height)
        
        # Стоимость материалов
        sheet_cost = self._calculate_sheet_cost(total_sheet_area_m2, sheet_material_id)
        edge_cost = self._calculate_edge_cost(edge_length, edge_material_id)
        
        materials_cost = sheet_cost + edge_cost
        
        # Фурнитура для полок (крепежи, уголки)
        # Можно добавить позже
        hardware_cost = Decimal("0")
        
        # Стоимость работы (25% для полок)
        work_cost = self._add_work_cost(materials_cost + hardware_cost, rate=0.25)
        
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
                "shelf_count": shelf_count,
                "has_back_panel": shelf_type == "closed",
            }
        }
