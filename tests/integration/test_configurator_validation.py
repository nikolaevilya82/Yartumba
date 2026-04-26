"""
Тесты валидации конфигураций конфигуратора
"""
import pytest
from app.services.configurator_service import ConfiguratorService


class TestNightstandValidation:
    """Тесты валидации тумбы"""

    def test_valid_nightstand_configuration(self):
        """Валидная конфигурация тумбы"""
        service = ConfiguratorService()
        config = {
            "width": 500,
            "height": 600,
            "depth": 400,
            "bodyMaterial": {"sheetMaterialId": "00000000-0000-0000-0000-000000000000"},
            "hardware": {},
            "drawers": {"count": 2},
        }
        result = service.validate_nightstand_config(config)
        
        assert result["valid"] is True
        assert result["errors"] == []

    def test_invalid_width_too_small(self):
        """Ширина слишком маленькая"""
        service = ConfiguratorService()
        result = service.validate_nightstand_config({
            "width": 200,
            "height": 600,
            "depth": 400,
            "bodyMaterial": {"sheetMaterialId": "00000000-0000-0000-0000-000000000000"},
            "drawers": {"count": 1},
        })
        
        assert result["valid"] is False
        assert any("Ширина" in error for error in result["errors"])

    def test_invalid_height_too_large(self):
        """Высота слишком большая"""
        service = ConfiguratorService()
        result = service.validate_nightstand_config({
            "width": 500,
            "height": 900,
            "depth": 400,
            "bodyMaterial": {"sheetMaterialId": "00000000-0000-0000-0000-000000000000"},
            "drawers": {"count": 1},
        })
        
        assert result["valid"] is False
        assert any("Высота" in error for error in result["errors"])

    def test_invalid_depth_too_small(self):
        """Глубина слишком маленькая"""
        service = ConfiguratorService()
        result = service.validate_nightstand_config({
            "width": 500,
            "height": 600,
            "depth": 200,
            "bodyMaterial": {"sheetMaterialId": "00000000-0000-0000-0000-000000000000"},
            "drawers": {"count": 1},
        })
        
        assert result["valid"] is False
        assert any("Глубина" in error for error in result["errors"])

    def test_exceeds_max_drawers(self):
        """Превышение максимального количества ящиков"""
        service = ConfiguratorService()
        result = service.validate_nightstand_config({
            "width": 500,
            "height": 600,
            "depth": 400,
            "bodyMaterial": {"sheetMaterialId": "00000000-0000-0000-0000-000000000000"},
            "drawers": {"count": 5},
        })
        
        assert result["valid"] is False
        assert any("ящиков" in error for error in result["errors"])

    def test_missing_material(self):
        """Отсутствие материала"""
        service = ConfiguratorService()
        result = service.validate_nightstand_config({
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

    def test_valid_bookshelf_configuration(self):
        """Валидная конфигурация полки"""
        service = ConfiguratorService()
        result = service.validate_bookshelf_config({
            "width": 800,
            "height": 1800,
            "depth": 300,
            "shelf_count": 4,
        })
        
        assert result["valid"] is True

    def test_invalid_bookshelf_width(self):
        """Невалидная ширина полки"""
        service = ConfiguratorService()
        result = service.validate_bookshelf_config({
            "width": 300,
            "height": 1800,
            "depth": 300,
            "shelf_count": 4,
        })
        
        assert result["valid"] is False

    def test_invalid_shelf_count(self):
        """Невалидное количество полок"""
        service = ConfiguratorService()
        result = service.validate_bookshelf_config({
            "width": 800,
            "height": 1800,
            "depth": 300,
            "shelf_count": 15,
        })
        
        assert result["valid"] is False


class TestDresserValidation:
    """Тесты валидации комода"""

    def test_valid_dresser_configuration(self):
        """Валидная конфигурация комода"""
        service = ConfiguratorService()
        result = service.validate_dresser_config({
            "width": 1000,
            "height": 850,
            "depth": 450,
            "drawer_count": 4,
        })
        
        assert result["valid"] is True

    def test_invalid_dresser_dimensions(self):
        """Невалидные размеры комода"""
        service = ConfiguratorService()
        result = service.validate_dresser_config({
            "width": 500,
            "height": 500,
            "depth": 300,
            "drawer_count": 4,
        })
        
        assert result["valid"] is False

    def test_invalid_drawer_count(self):
        """Невалидное количество ящиков комода"""
        service = ConfiguratorService()
        result = service.validate_dresser_config({
            "width": 1000,
            "height": 850,
            "depth": 450,
            "drawer_count": 10,
        })
        
        assert result["valid"] is False
