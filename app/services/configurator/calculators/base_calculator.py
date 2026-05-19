"""
Базовый класс для расчёта стоимости мебели
"""
from abc import ABC, abstractmethod
from typing import Dict, Any, Optional
from decimal import Decimal
from uuid import UUID

from sqlalchemy.orm import Session

from app.models.materials import (
    SheetMaterial,
    EdgeMaterial,
    SlideGuide,
    Hinge,
    Support,
    WallMount,
)


class BaseCostCalculator(ABC):
    """Базовый класс для расчёта стоимости мебели"""

    def __init__(self, db: Session):
        """
        Args:
            db: Сессия базы данных
        """
        self.db = db

    @abstractmethod
    def calculate(self, config: Dict[str, Any]) -> Dict[str, Any]:
        """
        Рассчитать стоимость
        
        Args:
            config: Конфигурация изделия
            
        Returns:
            Детализация стоимости
        """
        pass

    def _get_sheet_material(self, material_id: Optional[UUID]) -> Optional[SheetMaterial]:
        """Получить листовой материал по ID"""
        if not material_id:
            return None
        return self.db.query(SheetMaterial).get(material_id)

    def _get_edge_material(self, material_id: Optional[UUID]) -> Optional[EdgeMaterial]:
        """Получить кромку по ID"""
        if not material_id:
            return None
        return self.db.query(EdgeMaterial).get(material_id)

    def _get_hinge(self, hinge_id: Optional[UUID]) -> Optional[Hinge]:
        """Получить петлю по ID"""
        if not hinge_id:
            return None
        return self.db.query(Hinge).get(hinge_id)

    def _get_slide_guide(self, guide_id: Optional[UUID]) -> Optional[SlideGuide]:
        """Получить направляющую по ID"""
        if not guide_id:
            return None
        return self.db.query(SlideGuide).get(guide_id)

    def _calculate_sheet_cost(
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
            Стоимость
        """
        if not material_id:
            return Decimal("0")
        
        material = self._get_sheet_material(material_id)
        if not material:
            return Decimal("0")
        
        # Цена за площадь
        return Decimal(str(area_m2)) * material.price

    def _calculate_edge_cost(
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
            Стоимость
        """
        if not material_id:
            return Decimal("0")
        
        material = self._get_edge_material(material_id)
        if not material:
            return Decimal("0")
        
        # Длина в метрах
        length_m = length_mm / 1000
        return Decimal(str(length_m)) * material.price_per_meter

    def _calculate_hinge_cost(
        self,
        count: int,
        hinge_id: Optional[UUID]
    ) -> Decimal:
        """Рассчитать стоимость петель"""
        if not hinge_id or count == 0:
            return Decimal("0")
        
        hinge = self._get_hinge(hinge_id)
        if not hinge:
            return Decimal("0")
        
        return Decimal(hinge.price) * count

    def _calculate_slide_cost(
        self,
        count: int,
        guide_id: Optional[UUID]
    ) -> Decimal:
        """Рассчитать стоимость направляющих"""
        if not guide_id or count == 0:
            return Decimal("0")
        
        guide = self._get_slide_guide(guide_id)
        if not guide:
            return Decimal("0")
        
        return Decimal(guide.price) * count

    def _add_work_cost(self, materials_cost: Decimal, rate: float = 0.3) -> Decimal:
        """
        Добавить стоимость работы
        
        Args:
            materials_cost: Стоимость материалов
            rate: Процент наценки (по умолчанию 30%)
            
        Returns:
            Стоимость работы
        """
        return materials_cost * Decimal(str(rate))
