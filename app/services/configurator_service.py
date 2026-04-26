"""
Сервис конфигуратора — расчёт стоимости и валидация конфигураций
"""
from typing import Dict, List, Optional, Any
from uuid import UUID
from decimal import Decimal

from app.models.materials import (
    SheetMaterial,
    EdgeMaterial,
    SlideGuide,
    Hinge,
    Support,
    WallMount,
)
from app.core.db_setup import SessionLocal


class ConfiguratorService:
    """Сервис для работы с конфигуратором мебели"""

    @staticmethod
    def get_materials_options() -> Dict[str, List[Dict[str, Any]]]:
        """
        Получить все доступные материалы и фурнитуру
        
        Returns:
            Словарь с категориями материалов
        """
        db = SessionLocal()
        try:
            options = {
                "sheet_materials": [],
                "edge_materials": [],
                "slide_guides": [],
                "hinges": [],
                "supports": [],
                "wall_mounts": [],
            }

            # Листовые материалы
            for material in db.query(SheetMaterial).filter_by(is_active="active").all():
                options["sheet_materials"].append({
                    "id": str(material.id),
                    "name": material.name,
                    "material_type": material.material_type,
                    "thickness": material.thickness,
                    "standard_width": material.standard_width,
                    "standard_height": material.standard_height,
                    "decor_name": material.decor_name,
                    "hex_code": material.hex_code,
                    "price": material.price,
                })

            # Кромка
            for edge in db.query(EdgeMaterial).all():
                options["edge_materials"].append({
                    "id": str(edge.id),
                    "sheet_material_id": str(edge.sheet_material_id),
                    "edge_type": edge.edge_type,
                    "thickness": edge.thickness,
                    "width": edge.width,
                    "decor_name": edge.decor_name,
                    "price_per_meter": edge.price_per_meter,
                })

            # Направляющие
            for guide in db.query(SlideGuide).all():
                options["slide_guides"].append({
                    "id": str(guide.id),
                    "name": guide.name,
                    "guide_type": guide.guide_type,
                    "extension_type": guide.extension_type,
                    "length": guide.length,
                    "load_capacity": guide.load_capacity,
                    "has_soft_close": guide.has_soft_close,
                    "price": guide.price,
                })

            # Петли
            for hinge in db.query(Hinge).all():
                options["hinges"].append({
                    "id": str(hinge.id),
                    "name": hinge.name,
                    "hinge_type": hinge.hinge_type,
                    "mounting_type": hinge.mounting_type,
                    "opening_angle": hinge.opening_angle,
                    "has_soft_close": hinge.has_soft_close,
                    "price": hinge.price,
                })

            # Опоры
            for support in db.query(Support).all():
                options["supports"].append({
                    "id": str(support.id),
                    "name": support.name,
                    "support_type": support.support_type,
                    "material": support.material,
                    "height": support.height,
                    "diameter": support.diameter,
                    "is_adjustable": support.is_adjustable,
                    "price": support.price,
                })

            # Настенные крепления
            for mount in db.query(WallMount).all():
                options["wall_mounts"].append({
                    "id": str(mount.id),
                    "name": mount.name,
                    "mount_type": mount.mount_type,
                    "wall_type": mount.wall_type,
                    "max_load": mount.max_load,
                    "adjustment": mount.adjustment,
                    "is_hidden": mount.is_hidden,
                    "price": mount.price,
                })

            return options
        finally:
            db.close()

    @staticmethod
    def calculate_nightstand_cost(config: Dict[str, Any]) -> Dict[str, Any]:
        """
        Расчёт стоимости прикроватной тумбы
        
        Args:
            config: Конфигурация тумбы
            
        Returns:
            Детализация стоимости
        """
        db = SessionLocal()
        try:
            # Базовые размеры
            width = config.get("width", 500)
            height = config.get("height", 500)
            depth = config.get("depth", 400)
            
            # Материалы
            sheet_material_id = config.get("bodyMaterial", {}).get("sheetMaterialId")
            edge_material_id = config.get("bodyMaterial", {}).get("edgeMaterialId")
            
            # Фурнитура
            hinge_id = config.get("hardware", {}).get("hingeId")
            slide_guide_id = config.get("hardware", {}).get("slideGuideId")
            
            # Ящики
            drawer_count = config.get("drawers", {}).get("count", 1)
            
            # Расчёт площади деталей (упрощённо)
            # Боковины: 2 шт × высота × глубина
            # Полки: (drawer_count - 1) × (width - 2×thickness) × depth
            # Верх/низ: width × depth
            # Фасады: drawer_count × (width - gap) × (height / drawer_count)
            
            thickness = 16  # мм, стандартная толщина ЛДСП
            gap = 4  # мм, зазоры между фасадами
            
            # Площадь в м²
            side_area = 2 * (height * depth) / 1_000_000
            shelf_area = (drawer_count - 1) * (width - 2 * thickness) * depth / 1_000_000
            top_bottom_area = 2 * (width * depth) / 1_000_000
            facade_area = drawer_count * (width - gap) * (height / drawer_count) / 1_000_000
            
            total_sheet_area = side_area + shelf_area + top_bottom_area + facade_area
            
            # Стоимость листового материала
            sheet_cost = 0
            if sheet_material_id:
                sheet = db.query(SheetMaterial).get(sheet_material_id)
                if sheet:
                    sheet_cost = total_sheet_area * sheet.price / sheet.standard_width * sheet.standard_height / 1_000_000
            
            # Стоимость кромки (по периметру)
            edge_cost = 0
            if edge_material_id:
                edge = db.query(EdgeMaterial).get(edge_material_id)
                if edge:
                    edge_length = (
                        2 * (height + depth) * 2 +  # боковины
                        2 * (width + depth) * (drawer_count + 1) +  # полки и верх/низ
                        2 * (width + height / drawer_count) * drawer_count  # фасады
                    )
                    edge_cost = edge_length / 1000 * edge.price_per_meter
            
            # Стоимость фурнитуры
            hinge_cost = 0
            if hinge_id:
                hinge = db.query(Hinge).get(hinge_id)
                if hinge:
                    hinge_cost = hinge.price * drawer_count * 2  # 2 петли на фасад
            
            slide_cost = 0
            if slide_guide_id:
                guide = db.query(SlideGuide).get(slide_guide_id)
                if guide:
                    slide_cost = guide.price * drawer_count
            
            # Итого
            materials_cost = sheet_cost + edge_cost
            hardware_cost = hinge_cost + slide_cost
            work_cost = (materials_cost + hardware_cost) * 0.3  # 30% на работу
            total_cost = materials_cost + hardware_cost + work_cost
            
            return {
                "materials_cost": int(materials_cost),
                "hardware_cost": int(hardware_cost),
                "work_cost": int(work_cost),
                "total_price": int(total_cost),
                "details": {
                    "sheet_material_area_m2": round(total_sheet_area, 3),
                    "edge_length_m": round(edge_length / 1000, 2) if edge_material_id else 0,
                    "hinges_count": drawer_count * 2,
                    "slides_count": drawer_count,
                }
            }
        finally:
            db.close()

    @staticmethod
    def validate_nightstand_config(config: Dict[str, Any]) -> Dict[str, Any]:
        """
        Валидация конфигурации тумбы
        
        Args:
            config: Конфигурация тумбы
            
        Returns:
            Результат валидации
        """
        errors = []
        
        # Размеры
        width = config.get("width", 0)
        height = config.get("height", 0)
        depth = config.get("depth", 0)
        
        if width < 300 or width > 800:
            errors.append("Ширина должна быть от 300 до 800 мм")
        
        if height < 300 or height > 800:
            errors.append("Высота должна быть от 300 до 800 мм")
        
        if depth < 300 or depth > 600:
            errors.append("Глубина должна быть от 300 до 600 мм")
        
        # Ящики
        drawer_count = config.get("drawers", {}).get("count", 0)
        if drawer_count < 1 or drawer_count > 3:
            errors.append("Количество ящиков должно быть от 1 до 3")
        
        # Материалы
        if not config.get("bodyMaterial", {}).get("sheetMaterialId"):
            errors.append("Выберите листовой материал")
        
        return {
            "valid": len(errors) == 0,
            "errors": errors,
        }

    @staticmethod
    def validate_bookshelf_config(config: Dict[str, Any]) -> Dict[str, Any]:
        """Валидация конфигурации книжной полки"""
        errors = []
        
        width = config.get("width", 0)
        height = config.get("height", 0)
        depth = config.get("depth", 0)
        
        if width < 400 or width > 2000:
            errors.append("Ширина должна быть от 400 до 2000 мм")
        
        if height < 400 or height > 2400:
            errors.append("Высота должна быть от 400 до 2400 мм")
        
        if depth < 200 or depth > 600:
            errors.append("Глубина должна быть от 200 до 600 мм")
        
        shelf_count = config.get("shelf_count", 0)
        if shelf_count < 1 or shelf_count > 10:
            errors.append("Количество полок должно быть от 1 до 10")
        
        return {
            "valid": len(errors) == 0,
            "errors": errors,
        }

    @staticmethod
    def validate_dresser_config(config: Dict[str, Any]) -> Dict[str, Any]:
        """Валидация конфигурации комода"""
        errors = []
        
        width = config.get("width", 0)
        height = config.get("height", 0)
        depth = config.get("depth", 0)
        
        if width < 600 or width > 1600:
            errors.append("Ширина должна быть от 600 до 1600 мм")
        
        if height < 600 or height > 1200:
            errors.append("Высота должна быть от 600 до 1200 мм")
        
        if depth < 400 or depth > 700:
            errors.append("Глубина должна быть от 400 до 700 мм")
        
        drawer_count = config.get("drawer_count", 0)
        if drawer_count < 1 or drawer_count > 6:
            errors.append("Количество ящиков должно быть от 1 до 6")
        
        return {
            "valid": len(errors) == 0,
            "errors": errors,
        }


# Экспорт экземпляра сервиса
configurator_service = ConfiguratorService()
