"""
Тесты производительности конфигуратора
"""
import pytest
import time
import concurrent.futures
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


@pytest.mark.slow
class TestConfiguratorPerformance:
    """Тесты производительности"""

    def test_calculation_within_100ms(self, service):
        """Расчёт в течение 100мс"""
        config = {
            "width": 500,
            "height": 600,
            "depth": 400,
            "bodyMaterial": {},
            "hardware": {},
            "drawers": {"count": 2},
        }
        
        start = time.time()
        result = service.calculate("nightstand", config)
        elapsed = (time.time() - start) * 1000
        
        assert result["total_price"] >= 0
        assert elapsed < 100, f"Расчёт занял {elapsed:.2f}мс, должно быть < 100мс"

    def test_validation_within_50ms(self, service):
        """Валидация в течение 50мс"""
        config = {
            "width": 500,
            "height": 600,
            "depth": 400,
            "bodyMaterial": {"sheetMaterialId": "00000000-0000-0000-0000-000000000000"},
            "hardware": {},
            "drawers": {"count": 2},
        }
        
        start = time.time()
        result = service.validate("nightstand", config)
        elapsed = (time.time() - start) * 1000
        
        assert result["valid"] is True
        assert elapsed < 50, f"Валидация заняла {elapsed:.2f}мс, должно быть < 50мс"

    def test_concurrent_configurations(self, service):
        """Параллельные конфигурации"""
        config = {
            "width": 500,
            "height": 600,
            "depth": 400,
            "bodyMaterial": {},
            "hardware": {},
            "drawers": {"count": 2},
        }
        
        def make_request(_):
            return service.calculate("nightstand", config)
        
        start = time.time()
        
        with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
            results = list(executor.map(make_request, range(10)))
        
        elapsed = time.time() - start
        
        assert all(r["total_price"] >= 0 for r in results)
        assert elapsed < 10, f"Параллельные запросы заняли {elapsed:.2f}с"
