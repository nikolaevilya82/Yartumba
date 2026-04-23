"""
Тесты Pydantic схем для прикроватных тумб
"""
import pytest
from pydantic import ValidationError
from app.api.v1.goods.nightstand.schemas import (
    NightstandCreate,
    NightstandUpdate,
    NightstandResponse,
    NightstandPartCreate,
    NightstandPartUpdate,
    NightstandPartResponse,
)
from uuid import uuid4


class TestNightstandCreate:
    """Тесты схемы NightstandCreate"""

    def test_create_valid_nightstand(self):
        """Валидное создание тумбы"""
        data = {
            "width": 500,
            "height": 600,
            "depth": 400,
            "drawer_count": 2,
            "has_open_shelf": True,
            "leg_type": "wooden"
        }
        
        schema = NightstandCreate(**data)
        
        assert schema.width == 500
        assert schema.height == 600
        assert schema.depth == 400
        assert schema.drawer_count == 2
        assert schema.has_open_shelf is True
        assert schema.leg_type == "wooden"

    def test_create_with_default_values(self):
        """Создание с полями по умолчанию"""
        data = {
            "width": 500,
            "height": 600,
            "depth": 400
        }
        
        schema = NightstandCreate(**data)
        
        assert schema.drawer_count == 1  # default
        assert schema.has_open_shelf is False  # default
        assert schema.leg_type == "standard"  # default

    def test_create_negative_width(self):
        """Отрицательная ширина - ошибка валидации"""
        with pytest.raises(ValidationError) as exc_info:
            NightstandCreate(
                width=-100,
                height=600,
                depth=400
            )
        
        assert "width" in str(exc_info.value)

    def test_create_zero_dimensions(self):
        """Нулевые размеры - ошибка валидации"""
        with pytest.raises(ValidationError):
            NightstandCreate(
                width=0,
                height=600,
                depth=400
            )

    def test_create_invalid_drawer_count_zero(self):
        """Нулевое количество ящиков - ошибка"""
        with pytest.raises(ValidationError) as exc_info:
            NightstandCreate(
                width=500,
                height=600,
                depth=400,
                drawer_count=0
            )

        assert "drawer_count" in str(exc_info.value)

    def test_create_invalid_drawer_count_negative(self):
        """Отрицательное количество ящиков - ошибка"""
        with pytest.raises(ValidationError) as exc_info:
            NightstandCreate(
                width=500,
                height=600,
                depth=400,
                drawer_count=-1
            )

        assert "drawer_count" in str(exc_info.value)

    def test_create_max_drawer_count(self):
        """Максимальное количество ящиков (10)"""
        schema = NightstandCreate(
            width=500,
            height=600,
            depth=400,
            drawer_count=10
        )
        
        assert schema.drawer_count == 10

    def test_create_excessive_drawer_count(self):
        """Чрезмерное количество ящиков (>10) - ошибка"""
        with pytest.raises(ValidationError) as exc_info:
            NightstandCreate(
                width=500,
                height=600,
                depth=400,
                drawer_count=11
            )

        assert "drawer_count" in str(exc_info.value)

    def test_create_with_product_id(self):
        """Создание с product_id"""
        product_id = uuid4()
        schema = NightstandCreate(
            width=500,
            height=600,
            depth=400,
            product_id=product_id
        )
        
        assert schema.product_id == product_id


class TestNightstandUpdate:
    """Тесты схемы NightstandUpdate"""

    def test_update_all_fields(self):
        """Обновление всех полей"""
        data = {
            "width": 600,
            "height": 700,
            "depth": 450,
            "drawer_count": 3,
            "has_open_shelf": True,
            "leg_type": "metal"
        }
        
        schema = NightstandUpdate(**data)
        
        assert schema.width == 600
        assert schema.height == 700
        assert schema.depth == 450
        assert schema.drawer_count == 3
        assert schema.has_open_shelf is True
        assert schema.leg_type == "metal"

    def test_update_partial(self):
        """Частичное обновление (только высота)"""
        schema = NightstandUpdate(height=800)
        
        assert schema.height == 800
        assert schema.width is None
        assert schema.depth is None

    def test_update_all_optional(self):
        """Все поля опциональны - пустой объект"""
        schema = NightstandUpdate()
        
        assert schema.width is None
        assert schema.height is None
        assert schema.depth is None
        assert schema.drawer_count is None

    def test_update_invalid_dimensions(self):
        """Невалидные размеры при обновлении"""
        with pytest.raises(ValidationError):
            NightstandUpdate(width=-100)

    def test_update_invalid_drawer_count(self):
        """Невалидное количество ящиков"""
        with pytest.raises(ValidationError):
            NightstandUpdate(drawer_count=0)


class TestNightstandPartCreate:
    """Тесты схемы NightstandPartCreate"""

    def test_create_valid_part(self):
        """Валидное создание детали"""
        data = {
            "name": "боковина",
            "part_width": 400,
            "part_height": 600,
            "part_depth": 18,
            "quantity": 2
        }
        
        schema = NightstandPartCreate(**data)
        
        assert schema.name == "боковина"
        assert schema.part_width == 400
        assert schema.part_height == 600
        assert schema.part_depth == 18
        assert schema.quantity == 2

    def test_create_part_with_material(self):
        """Создание детали с material_id"""
        sheet_material_id = uuid4()
        schema = NightstandPartCreate(
            name="полка",
            part_width=468,
            part_height=300,
            part_depth=18,
            quantity=1,
            sheet_material_id=sheet_material_id
        )
        
        assert schema.sheet_material_id == sheet_material_id

    def test_create_part_without_dimensions(self):
        """Деталь без размеров (опционально)"""
        schema = NightstandPartCreate(
            name="тест",
            quantity=1
        )
        
        assert schema.name == "тест"
        assert schema.part_width is None
        assert schema.part_height is None
        assert schema.part_depth is None

    def test_create_part_zero_quantity(self):
        """Нулевое количество - ошибка"""
        with pytest.raises(ValidationError):
            NightstandPartCreate(
                name="тест",
                quantity=0
            )

    def test_create_part_negative_quantity(self):
        """Отрицательное количество - ошибка"""
        with pytest.raises(ValidationError):
            NightstandPartCreate(
                name="тест",
                quantity=-5
            )

    def test_create_part_negative_dimensions(self):
        """Отрицательные размеры - ошибка"""
        with pytest.raises(ValidationError):
            NightstandPartCreate(
                name="тест",
                part_width=-100,
                part_height=200,
                part_depth=18,
                quantity=1
            )

    def test_create_part_empty_name(self):
        """Пустое имя - проверяем, что принимается (валидация на бэкенде)"""
        # Pydantic не валидирует пустые строки по умолчанию
        schema = NightstandPartCreate(
            name="",
            quantity=1
        )
        
        assert schema.name == ""


class TestNightstandPartUpdate:
    """Тесты схемы NightstandPartUpdate"""

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
        
        schema = NightstandPartUpdate(**data)
        
        assert schema.name == "новое имя"
        assert schema.part_width == 500
        assert schema.quantity == 5

    def test_update_partial(self):
        """Частичное обновление"""
        schema = NightstandPartUpdate(quantity=10)
        
        assert schema.quantity == 10
        assert schema.name is None

    def test_update_all_optional(self):
        """Все поля опциональны"""
        schema = NightstandPartUpdate()
        
        assert schema.name is None
        assert schema.part_width is None
        assert schema.quantity is None


class TestNightstandResponse:
    """Тесты схемы NightstandResponse"""

    def test_response_structure(self):
        """Структура ответа"""
        # Имитация данных из БД
        data = {
            "id": str(uuid4()),
            "width": 500,
            "height": 600,
            "depth": 400,
            "drawer_count": 2,
            "has_open_shelf": True,
            "leg_type": "standard",
            "product_id": None,
            "created_at": "2025-01-15T10:00:00Z",
            "updated_at": "2025-01-15T10:00:00Z"
        }
        
        schema = NightstandResponse(**data)
        
        assert schema.id is not None
        assert schema.width == 500
        assert schema.drawer_count == 2
        assert schema.has_open_shelf is True
        assert schema.leg_type == "standard"

    def test_response_with_product_id(self):
        """Ответ с product_id"""
        product_id = uuid4()
        data = {
            "id": str(uuid4()),
            "width": 500,
            "height": 600,
            "depth": 400,
            "drawer_count": 1,
            "has_open_shelf": False,
            "leg_type": "wooden",
            "product_id": product_id,
            "created_at": None,
            "updated_at": None
        }
        
        schema = NightstandResponse(**data)
        
        assert schema.product_id == product_id


class TestNightstandPartResponse:
    """Тесты схемы NightstandPartResponse"""

    def test_response_structure(self):
        """Структура ответа"""
        nightstand_id = uuid4()
        sheet_material_id = uuid4()
        
        data = {
            "id": str(uuid4()),
            "name": "боковина",
            "part_width": 400,
            "part_height": 600,
            "part_depth": 18,
            "quantity": 2,
            "nightstand_id": nightstand_id,
            "sheet_material_id": sheet_material_id
        }
        
        schema = NightstandPartResponse(**data)
        
        assert schema.id is not None
        assert schema.name == "боковина"
        assert schema.part_width == 400
        assert schema.quantity == 2
        assert schema.nightstand_id == nightstand_id
        assert schema.sheet_material_id == sheet_material_id

    def test_response_without_material(self):
        """Ответ без материала"""
        data = {
            "id": str(uuid4()),
            "name": "тест",
            "part_width": 100,
            "part_height": 200,
            "part_depth": 10,
            "quantity": 1,
            "nightstand_id": str(uuid4()),
            "sheet_material_id": None
        }
        
        schema = NightstandPartResponse(**data)
        
        assert schema.sheet_material_id is None
