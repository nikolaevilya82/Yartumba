"""
Pydantic схемы для BOM (Bill of Materials)
"""
from typing import Dict, Any, List, Optional
from pydantic import BaseModel, Field


class Part(BaseModel):
    """Деталь из листового материала"""
    name: str = Field(..., description="Название детали")
    width: int = Field(..., ge=0, description="Ширина, мм")
    depth: int = Field(..., ge=0, description="Глубина/длина, мм")
    thickness: int = Field(default=16, ge=0, description="Толщина, мм")
    quantity: int = Field(..., ge=1, description="Количество")
    material_id: Optional[str] = Field(None, description="ID листового материала")
    edge_materials: List[Dict[str, Any]] = Field(
        default_factory=list,
        description="Список кромки: [{'edge': 'front|back|left|right', 'material_id': str}]"
    )


class SheetMaterialGroup(BaseModel):
    """Группа деталей по листовому материалу"""
    material_id: str = Field(..., description="ID материала")
    material_name: str = Field(..., description="Название материала")
    parts: List[Part] = Field(..., description="Список деталей")
    total_area_m2: float = Field(..., description="Общая площадь, м²")
    estimated_sheets: int = Field(..., description="Примерное количество листов")


class EdgeMaterialGroup(BaseModel):
    """Группа кромки по материалу"""
    material_id: str = Field(..., description="ID материала")
    material_name: str = Field(..., description="Название материала")
    edges: List[Dict[str, Any]] = Field(
        default_factory=list,
        description="Список кромки: [{'part': str, 'edge': str, 'length_mm': int}]"
    )
    total_length_m: float = Field(..., description="Общая длина, м")


class HardwareItem(BaseModel):
    """Элемент фурнитуры"""
    type: str = Field(..., description="Тип: hinge, slide_guide, support, wall_mount")
    name: str = Field(..., description="Название")
    item_id: Optional[str] = Field(None, description="ID из БД")
    quantity: int = Field(..., ge=1, description="Количество")
    price_per_unit: int = Field(..., ge=0, description="Цена за единицу, копейки")
    total_price: int = Field(..., ge=0, description="Общая цена, копейки")


class BOM(BaseModel):
    """Список материалов для производства"""
    furniture_type: str = Field(..., description="Тип мебели: nightstand, bookshelf, dresser")
    furniture_id: Optional[str] = Field(None, description="ID изделия (если уже создано)")
    
    # Материалы
    sheet_materials: List[SheetMaterialGroup] = Field(
        default_factory=list,
        description="Листовые материалы с деталями"
    )
    edge_materials: List[EdgeMaterialGroup] = Field(
        default_factory=list,
        description="Кромка с длинами"
    )
    
    # Фурнитура
    hardware: List[HardwareItem] = Field(
        default_factory=list,
        description="Фурнитура"
    )
    
    # Итоговые метрики
    total_sheet_area_m2: float = Field(..., description="Общая площадь листовых материалов, м²")
    total_edge_length_m: float = Field(..., description="Общая длина кромки, м")
    
    # Для производства
    estimated_sheets: int = Field(
        default=0,
        description="Примерное количество листов ДСП (стандарт 2800x2070мм)"
    )
    waste_percentage: float = Field(
        default=10.0,
        description="Процент отходов при раскрое"
    )
    
    # Метаданные
    notes: List[str] = Field(
        default_factory=list,
        description="Примечания для производства"
    )

    def to_dict(self) -> Dict[str, Any]:
        """Преобразование в словарь для JSON"""
        return self.model_dump(mode='json')
    
    def to_production_json(self) -> str:
        """Экспорт в JSON для производства"""
        import json
        return json.dumps(self.to_dict(), ensure_ascii=False, indent=2)
