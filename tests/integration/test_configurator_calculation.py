"""
Тесты расчёта стоимости конфигуратора
"""
import pytest
from app.core.db_setup import SessionLocal
from app.services.configurator import create_configurator_service


@pytest.fixture
def service():
    """Фикстура сервиса конфигуратора"""
    db = SessionLocal()
    try:
        yield create_configurator_service(db)
    finally:
        db.close()


class TestNightstandCostCalculation:
    """Тесты расчёта стоимости тумбы"""

    def test_calculate_basic_cost(self, service):
        """Базовый расчёт стоимости"""
        config = {
            "width": 500,
            "height": 600,
            "depth": 400,
            "bodyMaterial": {},
            "hardware": {},
            "drawers": {"count": 2},
        }
        result = service.calculate("nightstand", config)
        
        assert "materials_cost" in result
        assert "hardware_cost" in result
        assert "work_cost" in result
        assert "total_price" in result

    def test_cost_breakdown_sum(self, service):
        """Сумма компонентов равна итогу"""
        config = {
            "width": 500,
            "height": 600,
            "depth": 400,
            "bodyMaterial": {},
            "hardware": {},
            "drawers": {"count": 2},
        }
        result = service.calculate("nightstand", config)
        
        calculated_sum = (
            result["materials_cost"] +
            result["hardware_cost"] +
            result["work_cost"]
        )
        assert calculated_sum == result["total_price"]

    def test_details_included(self, service):
        """В ответе есть детализация"""
        config = {
            "width": 500,
            "height": 600,
            "depth": 400,
            "bodyMaterial": {},
            "hardware": {},
            "drawers": {"count": 2},
        }
        result = service.calculate("nightstand", config)
        
        assert "details" in result
        assert "volume_m3" in result["details"]
        assert "hinges_count" in result["details"]
        assert "slides_count" in result["details"]

    def test_zero_drawers_cost(self, service):
        """Расчёт с одним ящиком"""
        config = {
            "width": 500,
            "height": 600,
            "depth": 400,
            "bodyMaterial": {},
            "hardware": {},
            "drawers": {"count": 1},
        }
        result = service.calculate("nightstand", config)
        
        assert result["details"]["hinges_count"] == 2
        assert result["details"]["slides_count"] == 1

    def test_multiple_drawers_cost(self, service):
        """Расчёт с несколькими ящиками"""
        config = {
            "width": 500,
            "height": 600,
            "depth": 400,
            "bodyMaterial": {},
            "hardware": {},
            "drawers": {"count": 3},
        }
        result = service.calculate("nightstand", config)
        
        assert result["details"]["hinges_count"] == 6
        assert result["details"]["slides_count"] == 3
