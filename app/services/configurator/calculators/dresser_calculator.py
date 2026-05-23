"""
Калькулятор стоимости комода
"""
from decimal import Decimal
from typing import Dict, Any
from uuid import UUID

from app.services.configurator.calculators.furniture_calculator import FurnitureCostCalculator
from app.services.configurator.bom_schemas import HardwareItem


class DresserCalculator(FurnitureCostCalculator):
    """Калькулятор для комодов"""

    def calculate(self, config: Dict[str, Any]) -> Dict[str, Any]:
        """
        Рассчитать стоимость комода

        Материал считается по объёму изделия (габаритные размеры).
        BOM формируется отдельно при оформлении заказа.

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

        # Фурнитура
        hardware = config.get("hardware", {})
        hinge_id = hardware.get("hingeId")
        slide_guide_id = hardware.get("slideGuideId")
        
        # Ящики
        drawer_count = config.get("drawer_count", 3)
        
        # Стоимость материала по объёму изделия
        materials_cost = self.calculate_volume_material_cost(
            width=width,
            height=height,
            depth=depth,
            material_id=UUID(sheet_material_id) if sheet_material_id else None,
        )
        
        # Формирование списка фурнитуры
        hardware_items = []
        hardware_cost = Decimal("0")
        
        # Петли (для комодов обычно 1 петля на ящик или не используются)
        if hinge_id:
            hinge = self.get_hinge(UUID(hinge_id))
            if hinge:
                hinge_cost = int(hinge.price) * drawer_count
                hardware_items.append(HardwareItem(
                    type="hinge",
                    name=hinge.name,
                    item_id=hinge_id,
                    quantity=drawer_count,
                    price_per_unit=int(hinge.price),
                    total_price=hinge_cost,
                ))
                hardware_cost += Decimal(hinge_cost)
        
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
                hardware_cost += Decimal(slide_cost)
        
        # Стоимость работы и итог
        work_cost = self.add_work_cost(materials_cost, hardware_cost, rate=0.35)
        total_cost = self.calculate_total(materials_cost, hardware_cost, work_cost)
        
        # Формируем результат
        return self.format_result(
            materials_cost=materials_cost,
            hardware_cost=hardware_cost,
            work_cost=work_cost,
            total_cost=total_cost,
            details={
                "volume_m3": round((width * height * depth) / 1_000_000_000, 6),
                "hinges_count": drawer_count if hinge_id else 0,
                "slides_count": drawer_count,
                "drawer_count": drawer_count,
            },
        )
