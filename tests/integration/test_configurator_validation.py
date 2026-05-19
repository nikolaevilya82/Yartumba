"""
Тесты валидации конфигураций конфигуратора
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


class TestNightstandValidation:
    """Тесты валидации тумбы"""

    def test_valid_nightstand_configuration(self, service):
        """Валидная конфигурация тумбы"""
        config = {
            "width": 500,
            "height": 600,
            "depth": 400,
            "bodyMaterial": {"sheetMaterialId": "00000000-0000-0000-0000-000000000000"},
            "hardware": {},
            "drawers": {"count": 2},
        }
        result = service.validate("nightstand", config)
        
        assert result["valid"] is True
        assert result["errors"] == []

    def test_invalid_width_too_small(self, service):
        """Ширина слишком маленькая"""
        result = service.validate("nightstand", {
            "width": 200,
            "height": 600,
            "depth": 400,
            "bodyMaterial": {"sheetMaterialId": "00000000-0000-0000-0000-000000000000"},
            "drawers": {"count": 1},
        })
        
        assert result["valid"] is False
        assert any("Ширина" in error for error in result["errors"])

    def test_invalid_height_too_large(self, service):
        """Высота слишком большая"""
        result = service.validate("nightstand", {
            "width": 500,
            "height": 900,
            "depth": 400,
            "bodyMaterial": {"sheetMaterialId": "00000000-0000-0000-0000-000000000000"},
            "drawers": {"count": 1},
        })
        
        assert result["valid"] is False
        assert any("Высота" in error for error in result["errors"])

    def test_invalid_depth_too_small(self, service):
        """Глубина слишком маленькая"""
        result = service.validate("nightstand", {
            "width": 500,
            "height": 600,
            "depth": 200,
            "bodyMaterial": {"sheetMaterialId": "00000000-0000-0000-0000-000000000000"},
            "drawers": {"count": 1},
        })
        
        assert result["valid"] is False
        assert any("Глубина" in error for error in result["errors"])

    def test_exceeds_max_drawers(self, service):
        """Превышение максимального количества ящиков"""
        result = service.validate("nightstand", {
            "width": 500,
            "height": 600,
            "depth": 400,
            "bodyMaterial": {"sheetMaterialId": "00000000-0000-0000-0000-000000000000"},
            "drawers": {"count": 5},
        })
        
        assert result["valid"] is False
        assert any("ящиков" in error for error in result["errors"])

    def test_missing_material(self, service):
        """Отсутствие материала"""
        result = service.validate("nightstand", {
            "width": 500,
            "height": 600,
            "depth": 400,
            "bodyMaterial": {},
            "drawers": {"count": 1},
        })
        
        assert result["valid"] is False
        assert any("материал" in error for error in result["errors"])


class TestBookshelfValidation:
    """Тесты валидации книжной полки"""

    def test_valid_bookshelf_configuration(self, service):
        """Валидная конфигурация полки"""
        result = service.validate("bookshelf", {
            "width": 800,
            "height": 1800,
            "depth": 300,
            "shelf_count": 4,
            "bodyMaterial": {
                "sheetMaterialId": "00000000-0000-0000-0000-000000000000",  # UUID-заглушка
            },
        })
        
        assert result["valid"] is True

    def test_invalid_bookshelf_width(self, service):
        """Невалидная ширина полки"""
        result = service.validate("bookshelf", {
            "width": 300,
            "height": 1800,
            "depth": 300,
            "shelf_count": 4,
        })
        
        assert result["valid"] is False

    def test_invalid_shelf_count(self, service):
        """Невалидное количество полок"""
        result = service.validate("bookshelf", {
            "width": 800,
            "height": 1800,
            "depth": 300,
            "shelf_count": 15,
        })
        
        assert result["valid"] is False


class TestDresserValidation:
    """Тесты валидации комода"""

    def test_valid_dresser_configuration(self, service):
        """Валидная конфигурация комода"""
        result = service.validate("dresser", {
            "width": 1000,
            "height": 850,
            "depth": 450,
            "drawer_count": 4,
            "bodyMaterial": {
                "sheetMaterialId": "00000000-0000-0000-0000-000000000000",  # UUID-заглушка
            },
        })
        
        assert result["valid"] is True

    def test_invalid_dresser_dimensions(self, service):
        """Невалидные размеры комода"""
        result = service.validate("dresser", {
            "width": 500,
            "height": 500,
            "depth": 300,
            "drawer_count": 4,
        })
        
        assert result["valid"] is False

    def test_invalid_drawer_count(self, service):
        """Невалидное количество ящиков комода"""
        result = service.validate("dresser", {
            "width": 1000,
            "height": 850,
            "depth": 450,
            "drawer_count": 10,
        })
        
        assert result["valid"] is False
