"""
Тесты Pydantic схем для книжных полок
"""
import pytest
from pydantic import ValidationError
from app.api.v1.goods.bookshelf.schemas import (
    BookshelfCreate,
    BookshelfUpdate,
    BookshelfPartCreate,
    BookshelfPartUpdate,
)
from uuid import uuid4


class TestBookshelfCreate:
    """Тесты схемы BookshelfCreate"""

    def test_create_valid_bookshelf(self):
        """Валидное создание полки"""
        data = {
            "width": 800,
            "height": 2000,
            "depth": 400,
            "shelf_count": 4,
            "shelf_type": "open"
        }
        
        schema = BookshelfCreate(**data)
        
        assert schema.width == 800
        assert schema.height == 2000
        assert schema.depth == 400
        assert schema.shelf_count == 4
        assert schema.shelf_type == "open"

    def test_create_with_default_values(self):
        """Создание с полями по умолчанию"""
        schema = BookshelfCreate(
            width=800,
            height=2000,
            depth=400
        )
        
        assert schema.shelf_count == 3  # default
        assert schema.shelf_type == "open"  # default

    def test_create_negative_dimensions(self):
        """Отрицательные размеры - ошибка"""
        with pytest.raises(ValidationError):
            BookshelfCreate(
                width=-100,
                height=2000,
                depth=400
            )

    def test_create_zero_shelf_count(self):
        """Нулевое количество полок - ошибка"""
        with pytest.raises(ValidationError):
            BookshelfCreate(
                width=800,
                height=2000,
                depth=400,
                shelf_count=0
            )

    def test_create_max_shelf_count(self):
        """Максимальное количество полок"""
        schema = BookshelfCreate(
            width=800,
            height=2000,
            depth=400,
            shelf_count=10
        )
        
        assert schema.shelf_count == 10


class TestBookshelfUpdate:
    """Тесты схемы BookshelfUpdate"""

    def test_update_all_fields(self):
        """Обновление всех полей"""
        data = {
            "width": 1000,
            "height": 2200,
            "depth": 450,
            "shelf_count": 5,
            "shelf_type": "closed"
        }
        
        schema = BookshelfUpdate(**data)
        
        assert schema.width == 1000
        assert schema.shelf_count == 5

    def test_update_partial(self):
        """Частичное обновление"""
        schema = BookshelfUpdate(shelf_count=6)
        
        assert schema.shelf_count == 6
        assert schema.width is None

    def test_update_all_optional(self):
        """Все поля опциональны"""
        schema = BookshelfUpdate()
        
        assert schema.width is None
        assert schema.shelf_count is None


class TestBookshelfPartCreate:
    """Тесты схемы BookshelfPartCreate"""

    def test_create_valid_part(self):
        """Валидное создание детали"""
        data = {
            "name": "боковина",
            "part_width": 400,
            "part_height": 2000,
            "part_depth": 18,
            "quantity": 2
        }
        
        schema = BookshelfPartCreate(**data)
        
        assert schema.name == "боковина"
        assert schema.part_width == 400
        assert schema.part_height == 2000
        assert schema.quantity == 2

    def test_create_shelf_part(self):
        """Создание полки"""
        schema = BookshelfPartCreate(
            name="полка",
            part_width=768,
            part_height=300,
            part_depth=18,
            quantity=4
        )
        
        assert schema.name == "полка"
        assert schema.quantity == 4

    def test_create_back_panel(self):
        """Создание задней стенки"""
        schema = BookshelfPartCreate(
            name="задняя стенка",
            part_width=800,
            part_height=1968,
            part_depth=3,
            quantity=1
        )
        
        assert schema.name == "задняя стенка"
        assert schema.part_depth == 3  # тонкий материал

    def test_create_part_zero_quantity(self):
        """Нулевое количество - ошибка"""
        with pytest.raises(ValidationError):
            BookshelfPartCreate(
                name="тест",
                quantity=0
            )

    def test_create_part_negative_dimensions(self):
        """Отрицательные размеры - ошибка"""
        with pytest.raises(ValidationError):
            BookshelfPartCreate(
                name="тест",
                part_width=-100,
                part_height=200,
                part_depth=18,
                quantity=1
            )

    def test_create_with_material(self):
        """Создание с материалом"""
        schema = BookshelfPartCreate(
            name="боковина",
            part_width=400,
            part_height=2000,
            part_depth=18,
            quantity=2,
            sheet_material_id=uuid4()
        )
        
        assert schema.sheet_material_id is not None


class TestBookshelfPartUpdate:
    """Тесты схемы BookshelfPartUpdate"""

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
        
        schema = BookshelfPartUpdate(**data)
        
        assert schema.name == "новое имя"
        assert schema.quantity == 5

    def test_update_partial(self):
        """Частичное обновление"""
        schema = BookshelfPartUpdate(quantity=10)
        
        assert schema.quantity == 10
        assert schema.name is None

    def test_update_all_optional(self):
        """Все поля опциональны"""
        schema = BookshelfPartUpdate()
        
        assert schema.name is None
        assert schema.part_width is None
        assert schema.quantity is None
