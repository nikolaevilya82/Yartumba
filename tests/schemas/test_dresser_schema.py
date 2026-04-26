"""
Тесты Pydantic схем для комодов
"""
import pytest
from pydantic import ValidationError
from app.api.v1.goods.dresser.schemas import (
    DresserCreate,
    DresserUpdate,
    DresserPartCreate,
    DresserPartUpdate,
)
from uuid import uuid4


class TestDresserCreate:
    """Тесты схемы DresserCreate"""

    def test_create_valid_dresser(self):
        """Валидное создание комода"""
        data = {
            "width": 1200,
            "height": 900,
            "depth": 500,
            "drawer_count": 4,
            "drawer_rows": 2,
            "dresser_type": "standard",
            "has_legs": True
        }
        
        schema = DresserCreate(**data)
        
        assert schema.width == 1200
        assert schema.height == 900
        assert schema.depth == 500
        assert schema.drawer_count == 4
        assert schema.drawer_rows == 2
        assert schema.dresser_type == "standard"
        assert schema.has_legs is True

    def test_create_with_default_values(self):
        """Создание с полями по умолчанию"""
        schema = DresserCreate(
            width=1000,
            height=850,
            depth=450
        )
        
        # Проверка, что поля есть (значения по умолчанию из схемы)
        assert schema.width == 1000
        assert schema.height == 850
        assert schema.depth == 450
        assert schema.drawer_count == 4  # из схемы
        assert schema.drawer_rows == 2    # из схемы
        assert schema.dresser_type == "standard"
        assert schema.has_legs is True    # из схемы

    def test_create_negative_dimensions(self):
        """Отрицательные размеры - ошибка"""
        with pytest.raises(ValidationError):
            DresserCreate(
                width=-500,
                height=900,
                depth=500
            )

    def test_create_zero_drawer_count(self):
        """Нулевое количество ящиков - ошибка"""
        with pytest.raises(ValidationError):
            DresserCreate(
                width=1200,
                height=900,
                depth=500,
                drawer_count=0
            )

    def test_create_max_drawer_count(self):
        """Максимальное количество ящиков"""
        schema = DresserCreate(
            width=1200,
            height=900,
            depth=500,
            drawer_count=10
        )
        
        assert schema.drawer_count == 10

    def test_create_invalid_drawer_rows(self):
        """Невалидное количество рядов"""
        with pytest.raises(ValidationError):
            DresserCreate(
                width=1200,
                height=900,
                depth=500,
                drawer_count=4,
                drawer_rows=0
            )


class TestDresserUpdate:
    """Тесты схемы DresserUpdate"""

    def test_update_all_fields(self):
        """Обновление всех полей"""
        data = {
            "width": 1400,
            "height": 1000,
            "depth": 550,
            "drawer_count": 6,
            "drawer_rows": 3,
            "dresser_type": "low",
            "has_legs": True
        }
        
        schema = DresserUpdate(**data)
        
        assert schema.width == 1400
        assert schema.drawer_count == 6
        assert schema.drawer_rows == 3

    def test_update_partial(self):
        """Частичное обновление"""
        schema = DresserUpdate(drawer_count=5)
        
        assert schema.drawer_count == 5
        assert schema.width is None

    def test_update_all_optional(self):
        """Все поля опциональны"""
        schema = DresserUpdate()
        
        assert schema.width is None
        assert schema.drawer_count is None


class TestDresserPartCreate:
    """Тесты схемы DresserPartCreate"""

    def test_create_valid_part(self):
        """Валидное создание детали"""
        data = {
            "name": "боковина",
            "part_width": 500,
            "part_height": 900,
            "part_depth": 18,
            "quantity": 2
        }
        
        schema = DresserPartCreate(**data)
        
        assert schema.name == "боковина"
        assert schema.part_width == 500
        assert schema.part_height == 900
        assert schema.quantity == 2

    def test_create_facade_part(self):
        """Создание фасада"""
        schema = DresserPartCreate(
            name="фасад",
            part_width=596,
            part_height=200,
            part_depth=18,
            quantity=4
        )
        
        assert schema.name == "фасад"
        assert schema.quantity == 4

    def test_create_drawer_part(self):
        """Создание ящика"""
        schema = DresserPartCreate(
            name="ящик",
            part_width=568,
            part_height=150,
            part_depth=450,
            quantity=1
        )
        
        assert schema.name == "ящик"

    def test_create_part_zero_quantity(self):
        """Нулевое количество - ошибка"""
        with pytest.raises(ValidationError):
            DresserPartCreate(
                name="тест",
                quantity=0
            )

    def test_create_part_negative_dimensions(self):
        """Отрицательные размеры - ошибка"""
        with pytest.raises(ValidationError):
            DresserPartCreate(
                name="тест",
                part_width=-100,
                part_height=200,
                part_depth=18,
                quantity=1
            )

    def test_create_with_material(self):
        """Создание с материалом"""
        schema = DresserPartCreate(
            name="боковина",
            part_width=500,
            part_height=900,
            part_depth=18,
            quantity=2,
            sheet_material_id=uuid4()
        )
        
        assert schema.sheet_material_id is not None


class TestDresserPartUpdate:
    """Тесты схемы DresserPartUpdate"""

    def test_update_all_fields(self):
        """Обновление всех полей"""
        data = {
            "name": "новое имя",
            "part_width": 600,
            "part_height": 800,
            "part_depth": 20,
            "quantity": 6,
            "sheet_material_id": uuid4()
        }
        
        schema = DresserPartUpdate(**data)
        
        assert schema.name == "новое имя"
        assert schema.quantity == 6

    def test_update_partial(self):
        """Частичное обновление"""
        schema = DresserPartUpdate(quantity=8)
        
        assert schema.quantity == 8
        assert schema.name is None

    def test_update_all_optional(self):
        """Все поля опциональны"""
        schema = DresserPartUpdate()
        
        assert schema.name is None
        assert schema.part_width is None
        assert schema.quantity is None
