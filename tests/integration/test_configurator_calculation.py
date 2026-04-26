"""
Тесты расчёта стоимости конфигуратора
"""
import pytest
from app.services.configurator_service import ConfiguratorService


class TestNightstandCostCalculation:
    """Тесты расчёта стоимости тумбы"""

    def test_calculate_basic_cost(self):
        """Базовый расчёт стоимости"""
        service = ConfiguratorService()
        config = {
            "width": 500,
            "height": 600,
            "depth": 400,
            "bodyMaterial": {},
            "hardware": {},
            "drawers": {"count": 2},
        }
        result = service.calculate_nightstand_cost(config)
        
        assert "materials_cost" in result
        assert "hardware_cost" in result
        assert "work_cost" in result
        assert "total_price" in result

    def test_cost_breakdown_sum(self):
        """Сумма компонентов равна итогу"""
        service = ConfiguratorService()
        config = {
            "width": 500,
            "height": 600,
            "depth": 400,
            "bodyMaterial": {},
            "hardware": {},
            "drawers": {"count": 2},
        }
        result = service.calculate_nightstand_cost(config)
        
        calculated_sum = (
            result["materials_cost"] +
            result["hardware_cost"] +
            result["work_cost"]
        )
        assert calculated_sum == result["total_price"]

    def test_details_included(self):
        """В ответе есть детализация"""
        service = ConfiguratorService()
        config = {
            "width": 500,
            "height": 600,
            "depth": 400,
            "bodyMaterial": {},
            "hardware": {},
            "drawers": {"count": 2},
        }
        result = service.calculate_nightstand_cost(config)
        
        assert "details" in result
        assert "sheet_material_area_m2" in result["details"]
        assert "hinges_count" in result["details"]
        assert "slides_count" in result["details"]

    def test_zero_drawers_cost(self):
        """Расчёт с одним ящиком"""
        service = ConfiguratorService()
        config = {
            "width": 500,
            "height": 600,
            "depth": 400,
            "bodyMaterial": {},
            "hardware": {},
            "drawers": {"count": 1},
        }
        result = service.calculate_nightstand_cost(config)
        
        assert result["details"]["hinges_count"] == 2
        assert result["details"]["slides_count"] == 1

    def test_multiple_drawers_cost(self):
        """Расчёт с несколькими ящиками"""
        service = ConfiguratorService()
        config = {
            "width": 500,
            "height": 600,
            "depth": 400,
            "bodyMaterial": {},
            "hardware": {},
            "drawers": {"count": 3},
        }
        result = service.calculate_nightstand_cost(config)
        
        assert result["details"]["hinges_count"] == 6
        assert result["details"]["slides_count"] == 3
