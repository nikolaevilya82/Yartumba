"""
Универсальные методы расчёта стоимости мебели

Содержит общую логику для всех типов изделий:
- Расчёт площади листовых материалов
- Расчёт длины кромки
- Расчёт стоимости материалов и фурнитуры
- Генерация списка деталей (BOM)
"""
from decimal import Decimal
from typing import Dict, Any, Optional, Tuple, List
from uuid import UUID

from sqlalchemy.orm import Session

from app.models.materials import (
    SheetMaterial,
    EdgeMaterial,
    SlideGuide,
    Hinge,
)
from app.services.configurator.constants import THICKNESS, GAP
from app.services.configurator.bom_schemas import (
    Part,
    SheetMaterialGroup,
    EdgeMaterialGroup,
    HardwareItem,
    BOM,
)


class FurnitureCostCalculator:
    """
    Универсальный калькулятор стоимости изделий
    
    Содержит общие методы для расчёта:
    - площади листовых материалов
    - длины кромки
    - стоимости материалов и фурнитуры
    """

    def __init__(self, db: Session):
        """
        Args:
            db: Сессия базы данных
        """
        self.db = db

    # =========================================================================
    # Получение материалов
    # =========================================================================

    def get_sheet_material(self, material_id: Optional[UUID]) -> Optional[SheetMaterial]:
        """Получить листовой материал по ID"""
        if not material_id:
            return None
        return self.db.query(SheetMaterial).get(material_id)

    def get_edge_material(self, material_id: Optional[UUID]) -> Optional[EdgeMaterial]:
        """Получить кромку по ID"""
        if not material_id:
            return None
        return self.db.query(EdgeMaterial).get(material_id)

    def get_hinge(self, hinge_id: Optional[UUID]) -> Optional[Hinge]:
        """Получить петлю по ID"""
        if not hinge_id:
            return None
        return self.db.query(Hinge).get(hinge_id)

    def get_slide_guide(self, guide_id: Optional[UUID]) -> Optional[SlideGuide]:
        """Получить направляющую по ID"""
        if not guide_id:
            return None
        return self.db.query(SlideGuide).get(guide_id)

    # =========================================================================
    # Расчёт площади листовых материалов
    # =========================================================================

    def calculate_body_area(
        self,
        width: int,
        height: int,
        depth: int,
        shelf_count: int = 0,
        facade_count: int = 0,
        has_back_panel: bool = False,
        thickness: int = None
    ) -> Tuple[float, Dict[str, float]]:
        """
        Рассчитать площадь листового материала для корпуса
        
        Args:
            width: Ширина изделия (мм)
            height: Высота изделия (мм)
            depth: Глубина изделия (мм)
            shelf_count: Количество внутренних полок
            facade_count: Количество фасадов
            has_back_panel: Есть ли задняя стенка
            thickness: Толщина материала (мм), по умолчанию 16
            
        Returns:
            (total_area_m2, details) - площадь в м² и детализация по деталям
        """
        if thickness is None:
            thickness = THICKNESS["default"]
        
        # Боковины (левая и правая)
        side_area = 2 * (height * depth)
        
        # Верх и низ
        top_bottom_area = 2 * (width * depth)
        
        # Внутренние полки
        shelf_area = 0
        if shelf_count > 0:
            shelf_area = shelf_count * (width - 2 * thickness) * depth
        
        # Фасады
        facade_area = 0
        if facade_count > 0:
            facade_height = int((height - GAP["default"] * (facade_count + 1)) / facade_count)
            facade_area = facade_count * (width - GAP["default"]) * facade_height
        
        # Задняя стенка
        back_area = 0
        if has_back_panel:
            back_area = width * height
        
        # Общая площадь в мм²
        total_area_mm2 = side_area + top_bottom_area + shelf_area + facade_area + back_area
        
        # Конвертируем в м²
        total_area_m2 = total_area_mm2 / 1_000_000
        
        details = {
            "side_area_m2": round(side_area / 1_000_000, 3),
            "top_bottom_area_m2": round(top_bottom_area / 1_000_000, 3),
            "shelf_area_m2": round(shelf_area / 1_000_000, 3),
            "facade_area_m2": round(facade_area / 1_000_000, 3),
            "back_area_m2": round(back_area / 1_000_000, 3),
        }
        
        return total_area_m2, details

    # =========================================================================
    # Расчёт длины кромки
    # =========================================================================

    def calculate_edge_length(
        self,
        width: int,
        height: int,
        depth: int,
        shelf_count: int = 0,
        facade_count: int = 0,
        has_back_panel: bool = False
    ) -> Tuple[float, Dict[str, float]]:
        """
        Рассчитать общую длину кромки (мм)
        
        Args:
            width: Ширина изделия (мм)
            height: Высота изделия (мм)
            depth: Глубина изделия (мм)
            shelf_count: Количество внутренних полок
            facade_count: Количество фасадов
            has_back_panel: Есть ли задняя стенка
            
        Returns:
            (total_length_mm, details) - длина в мм и детализация
        """
        # Боковины (периметр * 2 стороны)
        side_edge = 2 * (height + depth) * 2
        
        # Верх и низ (периметр)
        top_bottom_edge = 2 * (width + depth) * 2
        
        # Внутренние полки
        shelf_edge = 0
        if shelf_count > 0:
            shelf_edge = 2 * (width + depth) * shelf_count
        
        # Фасады
        facade_edge = 0
        if facade_count > 0:
            facade_height = int((height - GAP["default"] * (facade_count + 1)) / facade_count)
            facade_edge = 2 * (width + facade_height) * facade_count
        
        # Задняя стенка (периметр)
        back_edge = 0
        if has_back_panel:
            back_edge = 2 * (width + height)
        
        total_edge = side_edge + top_bottom_edge + shelf_edge + facade_edge + back_edge
        
        details = {
            "side_edge_mm": side_edge,
            "top_bottom_edge_mm": top_bottom_edge,
            "shelf_edge_mm": shelf_edge,
            "facade_edge_mm": facade_edge,
            "back_edge_mm": back_edge,
        }
        
        return total_edge, details

    # =========================================================================
    # Расчёт стоимости материалов
    # =========================================================================

    def calculate_sheet_cost(
        self,
        area_m2: float,
        material_id: Optional[UUID]
    ) -> Decimal:
        """
        Рассчитать стоимость листового материала
        
        Args:
            area_m2: Площадь в м²
            material_id: ID материала
            
        Returns:
            Стоимость в копейках
        """
        if not material_id:
            return Decimal("0")
        
        material = self.get_sheet_material(material_id)
        if not material:
            return Decimal("0")
        
        return Decimal(str(area_m2)) * material.price

    def calculate_edge_cost(
        self,
        length_mm: float,
        material_id: Optional[UUID]
    ) -> Decimal:
        """
        Рассчитать стоимость кромки
        
        Args:
            length_mm: Длина в мм
            material_id: ID материала
            
        Returns:
            Стоимость в копейках
        """
        if not material_id:
            return Decimal("0")
        
        material = self.get_edge_material(material_id)
        if not material:
            return Decimal("0")
        
        length_m = length_mm / 1000
        return Decimal(str(length_m)) * material.price_per_meter

    # =========================================================================
    # Расчёт стоимости фурнитуры
    # =========================================================================

    def calculate_hinge_cost(
        self,
        count: int,
        hinge_id: Optional[UUID]
    ) -> Decimal:
        """
        Рассчитать стоимость петель
        
        Args:
            count: Количество петель
            hinge_id: ID петли
            
        Returns:
            Стоимость в копейках
        """
        if not hinge_id or count == 0:
            return Decimal("0")
        
        hinge = self.get_hinge(hinge_id)
        if not hinge:
            return Decimal("0")
        
        return Decimal(hinge.price) * count

    def calculate_slide_cost(
        self,
        count: int,
        guide_id: Optional[UUID]
    ) -> Decimal:
        """
        Рассчитать стоимость направляющих
        
        Args:
            count: Количество пар направляющих
            guide_id: ID направляющей
            
        Returns:
            Стоимость в копейках
        """
        if not guide_id or count == 0:
            return Decimal("0")
        
        guide = self.get_slide_guide(guide_id)
        if not guide:
            return Decimal("0")
        
        return Decimal(guide.price) * count

    # =========================================================================
    # Итоговый расчёт
    # =========================================================================

    def add_work_cost(
        self,
        materials_cost: Decimal,
        hardware_cost: Decimal,
        rate: float = 0.3
    ) -> Decimal:
        """
        Добавить стоимость работы
        
        Args:
            materials_cost: Стоимость материалов
            hardware_cost: Стоимость фурнитуры
            rate: Процент наценки (по умолчанию 30%)
            
        Returns:
            Стоимость работы в копейках
        """
        subtotal = materials_cost + hardware_cost
        return subtotal * Decimal(str(rate))

    def calculate_total(
        self,
        materials_cost: Decimal,
        hardware_cost: Decimal,
        work_cost: Decimal
    ) -> Decimal:
        """
        Рассчитать итоговую стоимость
        
        Args:
            materials_cost: Стоимость материалов
            hardware_cost: Стоимость фурнитуры
            work_cost: Стоимость работы
            
        Returns:
            Итоговая стоимость в копейках
        """
        return materials_cost + hardware_cost + work_cost

    def format_result(
        self,
        materials_cost: Decimal,
        hardware_cost: Decimal,
        work_cost: Decimal,
        total_cost: Decimal,
        details: Dict[str, Any],
        bom: Optional[BOM] = None,
    ) -> Dict[str, Any]:
        """
        Сформировать результат расчёта
        
        Args:
            materials_cost: Стоимость материалов
            hardware_cost: Стоимость фурнитуры
            work_cost: Стоимость работы
            total_cost: Итоговая стоимость
            details: Детализация расчёта
            bom: Список материалов для производства (опционально)
            
        Returns:
            Словарь с результатами
        """
        result = {
            "materials_cost": int(materials_cost),
            "hardware_cost": int(hardware_cost),
            "work_cost": int(work_cost),
            "total_price": int(total_cost),
            "details": details,
        }

        if bom:
            result["bom"] = bom.to_dict()
        
        return result

    # =========================================================================
    # Генерация списка деталей (BOM)
    # =========================================================================

    def generate_parts_list(
        self,
        width: int,
        height: int,
        depth: int,
        shelf_count: int = 0,
        facade_count: int = 0,
        has_back_panel: bool = False,
        thickness: int = None,
        sheet_material_id: Optional[UUID] = None,
        edge_material_id: Optional[UUID] = None,
    ) -> List[Part]:
        """
        Генерировать список деталей для производства
        
        Args:
            width: Ширина изделия (мм)
            height: Высота изделия (мм)
            depth: Глубина изделия (мм)
            shelf_count: Количество внутренних полок
            facade_count: Количество фасадов
            has_back_panel: Есть ли задняя стенка
            thickness: Толщина материала (мм)
            sheet_material_id: ID листового материала
            edge_material_id: ID кромки
            
        Returns:
            Список деталей
        """
        if thickness is None:
            thickness = THICKNESS["default"]
        
        parts = []
        
        # Боковины (левая и правая)
        parts.append(Part(
            name="side_left",
            width=height,
            depth=depth,
            thickness=thickness,
            quantity=1,
            material_id=str(sheet_material_id) if sheet_material_id else None,
            edge_materials=[
                {"edge": "front", "material_id": str(edge_material_id) if edge_material_id else None},
                {"edge": "back", "material_id": str(edge_material_id) if edge_material_id else None},
                {"edge": "bottom", "material_id": str(edge_material_id) if edge_material_id else None},
            ]
        ))
        parts.append(Part(
            name="side_right",
            width=height,
            depth=depth,
            thickness=thickness,
            quantity=1,
            material_id=str(sheet_material_id) if sheet_material_id else None,
            edge_materials=[
                {"edge": "front", "material_id": str(edge_material_id) if edge_material_id else None},
                {"edge": "back", "material_id": str(edge_material_id) if edge_material_id else None},
                {"edge": "bottom", "material_id": str(edge_material_id) if edge_material_id else None},
            ]
        ))
        
        # Верх и низ
        parts.append(Part(
            name="top",
            width=width - 2 * thickness,
            depth=depth,
            thickness=thickness,
            quantity=1,
            material_id=str(sheet_material_id) if sheet_material_id else None,
            edge_materials=[
                {"edge": "front", "material_id": str(edge_material_id) if edge_material_id else None},
            ]
        ))
        parts.append(Part(
            name="bottom",
            width=width - 2 * thickness,
            depth=depth,
            thickness=thickness,
            quantity=1,
            material_id=str(sheet_material_id) if sheet_material_id else None,
            edge_materials=[
                {"edge": "front", "material_id": str(edge_material_id) if edge_material_id else None},
            ]
        ))
        
        # Внутренние полки
        if shelf_count > 0:
            for i in range(shelf_count):
                parts.append(Part(
                    name=f"shelf_{i + 1}",
                    width=width - 2 * thickness,
                    depth=depth,
                    thickness=thickness,
                    quantity=1,
                    material_id=str(sheet_material_id) if sheet_material_id else None,
                    edge_materials=[
                        {"edge": "front", "material_id": str(edge_material_id) if edge_material_id else None},
                    ]
                ))
        
        # Фасады
        if facade_count > 0:
            facade_height = int((height - GAP["default"] * (facade_count + 1)) / facade_count)
            for i in range(facade_count):
                parts.append(Part(
                    name=f"facade_{i + 1}",
                    width=width - GAP["default"],
                    depth=facade_height,
                    thickness=thickness,
                    quantity=1,
                    material_id=str(sheet_material_id) if sheet_material_id else None,
                    edge_materials=[
                        {"edge": "all", "material_id": str(edge_material_id) if edge_material_id else None},
                    ]
                ))
        
        # Задняя стенка
        if has_back_panel:
            parts.append(Part(
                name="back_panel",
                width=width,
                depth=height,
                thickness=THICKNESS["hdf"],  # Обычно ХДФ 3мм
                quantity=1,
                material_id=None,  # Отдельный материал
                edge_materials=[]
            ))
        
        return parts

    def generate_edge_list(
        self,
        parts: List[Part],
    ) -> List[Dict[str, Any]]:
        """
        Генерировать список кромки по деталям
        
        Args:
            parts: Список деталей
            
        Returns:
            Список кромки с длинами
        """
        edges = []
        
        for part in parts:
            # front/back - длина = width
            # left/right - длина = depth (высота для вертикальных деталей)
            if "side" in part.name:
                # Боковины: front, back, bottom
                for edge_info in part.edge_materials:
                    if edge_info["edge"] in ["front", "back"]:
                        edges.append({
                            "part": part.name,
                            "edge": edge_info["edge"],
                            "length_mm": part.width,
                            "material_id": edge_info.get("material_id"),
                        })
                    elif edge_info["edge"] == "bottom":
                        edges.append({
                            "part": part.name,
                            "edge": edge_info["edge"],
                            "length_mm": part.depth,
                            "material_id": edge_info.get("material_id"),
                        })
            elif "facade" in part.name:
                # Фасады: все 4 стороны
                for edge_info in part.edge_materials:
                    if edge_info["edge"] == "all":
                        edges.append({
                            "part": part.name,
                            "edge": "front",
                            "length_mm": part.width,
                            "material_id": edge_info.get("material_id"),
                        })
                        edges.append({
                            "part": part.name,
                            "edge": "back",
                            "length_mm": part.depth,
                            "material_id": edge_info.get("material_id"),
                        })
                        edges.append({
                            "part": part.name,
                            "edge": "left",
                            "length_mm": part.depth,
                            "material_id": edge_info.get("material_id"),
                        })
                        edges.append({
                            "part": part.name,
                            "edge": "right",
                            "length_mm": part.depth,
                            "material_id": edge_info.get("material_id"),
                        })
            else:
                # Полки, верх, низ
                for edge_info in part.edge_materials:
                    if edge_info["edge"] == "front":
                        edges.append({
                            "part": part.name,
                            "edge": edge_info["edge"],
                            "length_mm": part.width,
                            "material_id": edge_info.get("material_id"),
                        })
        
        return edges

    def generate_bom(
        self,
        furniture_type: str,
        parts: List[Part],
        edges: List[Dict[str, Any]],
        hardware_items: List[HardwareItem],
        sheet_material_id: Optional[UUID] = None,
    ) -> BOM:
        """
        Сформировать полный BOM
        
        Args:
            furniture_type: Тип мебели
            parts: Список деталей
            edges: Список кромки
            hardware_items: Список фурнитуры
            sheet_material_id: ID листового материала
            
        Returns:
            Полный BOM
        """
        # Агрегируем детали по материалу
        sheet_groups: Dict[str, SheetMaterialGroup] = {}
        total_area = 0.0
        
        for part in parts:
            if not part.material_id:
                continue
            
            if part.material_id not in sheet_groups:
                material = self.get_sheet_material(UUID(part.material_id))
                sheet_groups[part.material_id] = SheetMaterialGroup(
                    material_id=part.material_id,
                    material_name=material.name if material else "Unknown",
                    parts=[],
                    total_area_m2=0.0,
                    estimated_sheets=0
                )
            
            part_area = (part.width * part.depth * part.quantity) / 1_000_000
            total_area += part_area
            
            sheet_groups[part.material_id].parts.append(part)
            sheet_groups[part.material_id].total_area_m2 += part_area
        
        # Агрегируем кромку по материалу
        edge_groups: Dict[str, EdgeMaterialGroup] = {}
        total_edge_length = 0.0
        
        for edge in edges:
            material_id = edge.get("material_id")
            if not material_id:
                continue
            
            if material_id not in edge_groups:
                material = self.get_edge_material(UUID(material_id))
                edge_groups[material_id] = EdgeMaterialGroup(
                    material_id=material_id,
                    material_name=material.name if material else "Unknown",
                    edges=[],
                    total_length_m=0.0
                )
            
            edge_groups[material_id].edges.append({
                "part": edge["part"],
                "edge": edge["edge"],
                "length_mm": edge["length_mm"],
            })
            total_edge_length += edge["length_mm"]
        
        # Заполняем группы
        for group in sheet_groups.values():
            group.total_area_m2 = round(group.total_area_m2, 3)
            # Стандартный лист 2800x2070 = 5.796 м²
            group.estimated_sheets = max(1, int(group.total_area_m2 / 5.796 + 0.5))
        
        for group in edge_groups.values():
            group.total_length_m = round(total_edge_length / 1000, 2)
        
        # Считаем итоговую площадь и длину
        total_sheet_area = sum(g.total_area_m2 for g in sheet_groups.values())
        total_edge_length_m = sum(g.total_length_m for g in edge_groups.values())
        
        # Общее количество листов
        total_sheets = sum(g.estimated_sheets for g in sheet_groups.values())
        
        return BOM(
            furniture_type=furniture_type,
            sheet_materials=list(sheet_groups.values()),
            edge_materials=list(edge_groups.values()),
            hardware=hardware_items,
            total_sheet_area_m2=round(total_sheet_area, 3),
            total_edge_length_m=round(total_edge_length_m, 2),
            estimated_sheets=total_sheets,
            waste_percentage=10.0,
            notes=[
                "Проверить размеры перед раскроем",
                "Кромка 0.4мм на видимых гранях",
            ]
        )