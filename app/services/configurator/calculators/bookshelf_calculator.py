"""
Калькулятор стоимости книжной полки
"""
from decimal import Decimal
from typing import Dict, Any
from uuid import UUID

from sqlalchemy.orm import Session

from app.services.configurator.calculators.furniture_calculator import FurnitureCostCalculator
from app.services.configurator.bom_schemas import BOM, HardwareItem
from app.services.configurator.bom_schemas import Part


class BookshelfCalculator(FurnitureCostCalculator):
    """Калькулятор для книжных полок"""

    def calculate(self, config: Dict[str, Any]) -> Dict[str, Any]:
        """
        Рассчитать стоимость полки + генерация BOM
        
        Args:
            config: Конфигурация полки
            
        Returns:
            Детализация стоимости и BOM для производства
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
        has_back_panel = shelf_type == "closed"
        
        # Генерация списка деталей (BOM)
        parts = self.generate_parts_list(
            width=width,
            height=height,
            depth=depth,
            shelf_count=shelf_count - 1,  # внутренние полки
            facade_count=0,
            has_back_panel=has_back_panel,
            sheet_material_id=UUID(sheet_material_id) if sheet_material_id else None,
            edge_material_id=UUID(edge_material_id) if edge_material_id else None,
        )
        
        # Генерация списка кромки
        edges = self.generate_edge_list(parts)
        
        # Формирование списка фурнитуры (для полок пока пустой)
        hardware_items = []
        
        # Генерация полного BOM
        bom = self.generate_bom(
            furniture_type="bookshelf",
            parts=parts,
            edges=edges,
            hardware_items=hardware_items,
            sheet_material_id=UUID(sheet_material_id) if sheet_material_id else None,
        )
        
        # Расчёт стоимости по BOM
        total_materials = Decimal("0")
        for group in bom.sheet_materials:
            if group.material_id:
                material = self.get_sheet_material(UUID(group.material_id))
                if material:
                    total_materials += Decimal(str(group.total_area_m2)) * material.price
        
        total_edge = Decimal("0")
        for group in bom.edge_materials:
            if group.material_id:
                material = self.get_edge_material(UUID(group.material_id))
                if material:
                    total_edge += Decimal(str(group.total_length_m)) * material.price_per_meter
        
        total_hardware = sum((item.total_price for item in hardware_items), Decimal("0"))
        
        materials_cost = total_materials + total_edge
        hardware_cost = total_hardware
        work_cost = self.add_work_cost(materials_cost, hardware_cost, rate=0.25)
        total_cost = self.calculate_total(materials_cost, hardware_cost, work_cost)
        
        # Формируем результат
        return self.format_result(
            materials_cost=materials_cost,
            hardware_cost=hardware_cost,
            work_cost=work_cost,
            total_cost=total_cost,
            details={
                "sheet_material_area_m2": round(bom.total_sheet_area_m2, 3),
                "edge_length_m": round(bom.total_edge_length_m, 2),
                "shelf_count": shelf_count,
                "has_back_panel": has_back_panel,
            },
            bom=bom
        )
