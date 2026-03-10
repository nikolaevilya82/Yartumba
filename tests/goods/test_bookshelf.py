"""
Тесты Bookshelf (книжные полки)
"""
import uuid
import pytest
from app.models.goods import Bookshelf, BookshelfPart


class TestBookshelf:
    def test_create_bookshelf(self, db_session):
        """Создание книжной полки"""
        bookshelf = Bookshelf(
            width=800,
            height=2000,
            depth=400,
            shelf_count=4,
            shelf_type="open"
        )
        db_session.add(bookshelf)
        db_session.commit()
        
        assert bookshelf.id is not None
        assert bookshelf.width == 800
        assert bookshelf.height == 2000
        assert bookshelf.shelf_count == 4

    def test_bookshelf_with_parts(self, db_session):
        """Полка с деталями"""
        bookshelf = Bookshelf(
            width=800,
            height=2000,
            depth=400,
            shelf_count=4
        )
        db_session.add(bookshelf)
        db_session.commit()
        
        # Добавляем детали
        part = BookshelfPart(
            bookshelf_id=bookshelf.id,
            name="боковина",
            part_width=400,
            part_height=2000,
            part_depth=18,
            quantity=2
        )
        db_session.add(part)
        db_session.commit()
        
        assert len(bookshelf.parts) == 1
        assert part.name == "боковина"

    def test_bookshelf_product_relation(self, db_session):
        """Связь с Product"""
        from app.models.catalog import Product
        
        product = Product(
            sku="SH-001",
            name="Книжная полка",
            base_price=5000
        )
        db_session.add(product)
        db_session.flush()

        bookshelf = Bookshelf(
            product_id=product.id,
            width=800,
            height=2000,
            depth=400
        )
        db_session.add(bookshelf)
        db_session.commit()
        
        # Проверяем через отдельный запрос
        product_check = db_session.query(Product).filter_by(sku="SH-001").first()
        assert product_check is not None

        bookshelf_check = db_session.query(Bookshelf).filter_by(product_id=product.id).first()
        assert bookshelf_check is not None
        assert bookshelf_check.product_id == product.id
