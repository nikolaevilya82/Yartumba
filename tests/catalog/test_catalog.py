"""
Тесты каталога (Product, Category, FurnitureMaterial)
"""
import uuid
import pytest
from app.models.catalog import (
    Category,
    Product,
    FurnitureMaterial,
)
from app.models.goods import Bookshelf, Nightstand, Dresser


class TestCategory:
    def test_create_category(self, db_session):
        """Создание категории"""
        category = Category(
            name="Книжные полки",
            slug="bookshelves",
            description="Стеллажи и полки для книг"
        )
        db_session.add(category)
        db_session.commit()
        
        assert category.id is not None
        assert category.slug == "bookshelves"

    def test_category_unique_slug(self, db_session):
        """Уникальность slug"""
        cat1 = Category(name="Полки", slug="shelves")
        db_session.add(cat1)
        db_session.commit()
        
        cat2 = Category(name="Полки 2", slug="shelves")
        db_session.add(cat2)
        
        with pytest.raises(Exception):
            db_session.commit()


class TestProduct:
    def test_create_product(self, db_session):
        """Создание товара"""
        product = Product(
            sku="BS-001",
            name="Книжная полка",
            description="Стандартная полка",
            base_price=5000,
            is_active=True
        )
        db_session.add(product)
        db_session.commit()
        
        assert product.id is not None
        assert product.sku == "BS-001"
        assert product.base_price == 5000

    def test_product_with_category(self, db_session):
        """Товар с категорией"""
        category = Category(name="Полки", slug="shelves")
        db_session.add(category)
        db_session.commit()
        
        product = Product(
            sku="BS-002",
            name="Полка",
            base_price=3000,
            category_id=category.id
        )
        db_session.add(product)
        db_session.commit()
        
        assert product.category is not None
        assert product.category.name == "Полки"


class TestFurnitureMaterial:
    def test_furniture_material_bookshelf(self, db_session):
        """Материалы для книжной полки"""
        # Создаём полку
        bookshelf = Bookshelf(
            width=800,
            height=2000,
            depth=400
        )
        db_session.add(bookshelf)
        db_session.flush()

        # Создаём материал
        sheet = SheetMaterial(
            name="ЛДСП 16мм Дуб сонома",
            material_type="ldsp",
            thickness=16,
            standard_width=2800,
            standard_height=2070,
            price=3500
        )
        db_session.add(sheet)
        db_session.flush()

        edge = EdgeMaterial(
            sheet_material_id=sheet.id,
            edge_type="abs",
            thickness=0.5,
            width=23,
            decor_name="Дуб сонома",
            price_per_meter=50
        )
        db_session.add(edge)
        
        db_session.flush()

        # Связываем материал с полкой
        fm = FurnitureMaterial(
            furniture_type="bookshelf",
            furniture_id=bookshelf.id,
            part_type="body",
            sheet_material_id=sheet.id,
            edge_id=edge.id
        )
        db_session.add(fm)
        db_session.commit()
        
        assert fm.furniture_type == "bookshelf"
        assert fm.part_type == "body"

    def test_furniture_material_nightstand_with_hinge(self, db_session):
        """Материалы для тумбы с петлями"""
        nightstand = Nightstand(
            width=500,
            height=600,
            depth=400
        )
        db_session.add(nightstand)
        
        sheet = SheetMaterial(
            name="МДФ 18мм Белый",
            material_type="mdf",
            thickness=18,
            standard_width=2800,
            standard_height=2070,
            price=5000
        )
        db_session.add(sheet)
        
        hinge = Hinge(
            name="Петля Blum",
            hinge_type="clip",
            mounting_type="overlay",
            price=250
        )
        db_session.add(hinge)
        
        db_session.commit()
        
        fm = FurnitureMaterial(
            furniture_type="nightstand",
            furniture_id=nightstand.id,
            part_type="facade",
            sheet_material_id=sheet.id,
            hinge_id=hinge.id
        )
        db_session.add(fm)
        db_session.commit()
        
        assert fm.part_type == "facade"
        assert fm.hinge is not None

    def test_furniture_material_dresser_with_support(self, db_session):
        """Материалы для комода с ножками"""
        dresser = Dresser(
            width=1200,
            height=900,
            depth=500
        )
        db_session.add(dresser)
        
        support = Support(
            name="Ножка деревянная",
            support_type="leg",
            material="solid_wood",
            height=100,
            price=200
        )
        db_session.add(support)
        
        db_session.commit()
        
        fm = FurnitureMaterial(
            furniture_type="dresser",
            furniture_id=dresser.id,
            part_type="legs",
            support_id=support.id,
            quantity=4
        )
        db_session.add(fm)
        db_session.commit()
        
        assert fm.quantity == 4
        assert fm.support.name == "Ножка деревянная"


# Импорт для тестов
from app.models.materials import SheetMaterial, EdgeMaterial, Hinge, Support
