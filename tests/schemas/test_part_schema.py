"""
Общие тесты для схем деталей (Part)
"""
import pytest
from pydantic import ValidationError
from app.api.v1.goods.schemas import (
    PartBase,
    PartCreate,
    PartUpdate,
    PartResponse,
)
from uuid import uuid4
from datetime import datetime


class TestPartBase:
    """Тесты базовой схемы детали"""

    def test_base_valid_part(self):
        """Валидная базовая деталь"""
        data = {
            "name": "тестовая деталь",
            "part_width": 400,
            "part_height": 600,
            "part_depth": 18,
            "quantity": 2
        }
        
        schema = PartBase(**data)
        
        assert schema.name == "тестовая деталь"
        assert schema.part_width == 400
        assert schema.quantity == 2

    def test_base_name_required(self):
        """Имя обязательно"""
        with pytest.raises(ValidationError):
            PartBase(
                part_width=400,
                part_height=600,
                part_depth=18,
                quantity=1
            )

    def test_base_default_quantity(self):
        """Количество по умолчанию = 1"""
        schema = PartBase(
            name="тест",
            part_width=100,
            part_height=200,
            part_depth=10
        )
        
        assert schema.quantity == 1


class TestPartCreate:
    """Тесты схемы создания детали"""

    def test_create_valid(self):
        """Валидное создание"""
        data = {
            "name": "боковина",
            "part_width": 400,
            "part_height": 600,
            "part_depth": 18,
            "quantity": 2,
            "sheet_material_id": uuid4()
        }
        
        schema = PartCreate(**data)
        
        assert schema.name == "боковина"
        assert schema.sheet_material_id is not None

    def test_create_without_material(self):
        """Создание без материала"""
        schema = PartCreate(
            name="тест",
            quantity=1
        )
        
        assert schema.sheet_material_id is None

    def test_create_dimensions_optional(self):
        """Размеры опциональны при создании"""
        schema = PartCreate(
            name="тест",
            quantity=1
        )
        
        assert schema.part_width is None
        assert schema.part_height is None
        assert schema.part_depth is None


class TestPartUpdate:
    """Тесты схемы обновления детали"""

    def test_update_all_fields(self):
        """Обновление всех полей"""
        data = {
            "name": "новое имя",
            "part_width": 500,
            "part_height": 700,
            "part_depth": 20,
            "quantity": 5,
            "sheet_material_id": uuid4()
        }
        
        schema = PartUpdate(**data)
        
        assert schema.name == "новое имя"
        assert schema.quantity == 5

    def test_update_partial(self):
        """Частичное обновление"""
        schema = PartUpdate(quantity=10)
        
        assert schema.quantity == 10
        assert schema.name is None
        assert schema.part_width is None

    def test_update_all_optional(self):
        """Все поля опциональны"""
        schema = PartUpdate()
        
        assert schema.name is None
        assert schema.part_width is None
        assert schema.part_height is None
        assert schema.part_depth is None
        assert schema.quantity is None
        assert schema.sheet_material_id is None

    def test_update_invalid_quantity(self):
        """Невалидное количество"""
        with pytest.raises(ValidationError):
            PartUpdate(quantity=0)

    def test_update_negative_dimensions(self):
        """Отрицательные размеры"""
        with pytest.raises(ValidationError):
            PartUpdate(part_width=-100)


class TestPartResponse:
    """Тесты схемы ответа детали"""

    def test_response_structure(self):
        """Структура ответа"""
        data = {
            "id": str(uuid4()),
            "name": "боковина",
            "part_width": 400,
            "part_height": 600,
            "part_depth": 18,
            "quantity": 2,
            "sheet_material_id": str(uuid4())
        }
        
        schema = PartResponse(**data)
        
        assert schema.id is not None
        assert schema.name == "боковина"
        assert schema.part_width == 400
        assert schema.quantity == 2
        assert schema.sheet_material_id is not None

    def test_response_without_material(self):
        """Ответ без материала"""
        data = {
            "id": str(uuid4()),
            "name": "тест",
            "part_width": 100,
            "part_height": 200,
            "part_depth": 10,
            "quantity": 1,
            "sheet_material_id": None
        }
        
        schema = PartResponse(**data)
        
        assert schema.sheet_material_id is None

    def test_response_with_dimensions(self):
        """Ответ с размерами"""
        data = {
            "id": str(uuid4()),
            "name": "полка",
            "part_width": 768,
            "part_height": 300,
            "part_depth": 18,
            "quantity": 4,
            "sheet_material_id": None
        }
        
        schema = PartResponse(**data)
        
        assert schema.part_width == 768
        assert schema.part_height == 300
        assert schema.part_depth == 18

    def test_response_without_dimensions(self):
        """Ответ без размеров"""
        data = {
            "id": str(uuid4()),
            "name": "тест",
            "part_width": None,
            "part_height": None,
            "part_depth": None,
            "quantity": 1,
            "sheet_material_id": None
        }
        
        schema = PartResponse(**data)
        
        assert schema.part_width is None
        assert schema.part_height is None
        assert schema.part_depth is None


class TestPartValidation:
    """Общие тесты валидации деталей"""

    def test_part_name_types(self):
        """Разные типы имён деталей"""
        valid_names = [
            "боковина",
            "полка",
            "верх",
            "низ",
            "задняя стенка",
            "фасад",
            "царга",
            "столешница",
            "ящик",
            "фронт ящика"
        ]
        
        for name in valid_names:
            schema = PartCreate(
                name=name,
                quantity=1
            )
            assert schema.name == name

    def test_part_quantity_range(self):
        """Диапазон количества"""
        # Минимум 1
        schema_min = PartCreate(name="тест", quantity=1)
        assert schema_min.quantity == 1
        
        # Максимум (большое число)
        schema_max = PartCreate(name="тест", quantity=1000)
        assert schema_max.quantity == 1000

    def test_part_dimensions_range(self):
        """Диапазон размеров"""
        # Минимальный размер
        schema_min = PartCreate(
            name="тест",
            part_width=1,
            part_height=1,
            part_depth=1,
            quantity=1
        )
        assert schema_min.part_width == 1
        
        # Максимальный размер
        schema_max = PartCreate(
            name="тест",
            part_width=5000,
            part_height=5000,
            part_depth=100,
            quantity=1
        )
        assert schema_max.part_width == 5000

    def test_part_zero_dimensions(self):
        """Нулевые размеры - ошибка"""
        with pytest.raises(ValidationError):
            PartCreate(
                name="тест",
                part_width=0,
                part_height=200,
                part_depth=18,
                quantity=1
            )

    def test_part_very_small_dimensions(self):
        """Очень маленькие размеры (но > 0)"""
        schema = PartCreate(
            name="тест",
            part_width=1,
            part_height=1,
            part_depth=1,
            quantity=1
        )
        
        assert schema.part_width == 1
