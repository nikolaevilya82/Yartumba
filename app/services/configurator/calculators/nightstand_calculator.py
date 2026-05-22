"""
Калькулятор стоимости прикроватной тумбы
"""
from decimal import Decimal
from typing import Dict, Any
from uuid import UUID

from sqlalchemy.orm import Session

from app.services.configurator.calculators.furniture_calculator import FurnitureCostCalculator
from app.services.configurator.constants import GAP
from app.services.configurator.bom_schemas import BOM, HardwareItem
from app.services.configurator.bom_schemas import Part


class NightstandCalculator(FurnitureCostCalculator):
    """Калькулятор для прикроватных тумб"""

    def calculate(self, config: Dict[str, Any]) -> Dict[str, Any]:
        """
        Рассчитать стоимость тумбы + генерация BOM
        
        Args:
            config: Конфигурация тумбы
            
        Returns:
            Детализация стоимости и BOM для производства
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
        
        # Генерация списка деталей (BOM)
        parts = self.generate_parts_list(
            width=width,
            height=height,
            depth=depth,
            shelf_count=drawer_count - 1,  # полки между ящиками
            facade_count=drawer_count,
            has_back_panel=False,
            sheet_material_id=UUID(sheet_material_id) if sheet_material_id else None,
            edge_material_id=UUID(edge_material_id) if edge_material_id else None,
        )
        
        # Генерация списка кромки
        edges = self.generate_edge_list(parts)
        
        # Формирование списка фурнитуры
        hardware_items = []
        
        # Петли
        hinge_count = drawer_count * 2
        if hinge_id:
            hinge = self.get_hinge(UUID(hinge_id))
            if hinge:
                hinge_cost = int(hinge.price) * hinge_count
                hardware_items.append(HardwareItem(
                    type="hinge",
                    name=hinge.name,
                    item_id=hinge_id,
                    quantity=hinge_count,
                    price_per_unit=int(hinge.price),
                    total_price=hinge_cost,
                ))
        
        # Направляющие
        if slide_guide_id:
            slide = self.get_slide_guide(UUID(slide_guide_id))
            if slide:
                slide_cost = int(slide.price) * drawer_count
                hardware_items.append(HardwareItem(
                    type="slide_guide",
                    name=slide.name,
                    item_id=slide_guide_id,
                    quantity=drawer_count,
                    price_per_unit=int(slide.price),
                    total_price=slide_cost,
                ))
        
        # Генерация полного BOM
        bom = self.generate_bom(
            furniture_type="nightstand",
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
        work_cost = self.add_work_cost(materials_cost, hardware_cost, rate=0.3)
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
                "hinges_count": hinge_count,
                "slides_count": drawer_count,
            },
            bom=bom
        )
