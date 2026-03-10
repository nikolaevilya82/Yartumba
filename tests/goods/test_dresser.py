"""
Тесты Dresser (комоды)
"""
import uuid
import pytest
from app.models.goods import Dresser, DresserPart


class TestDresser:
    def test_create_dresser(self, db_session):
        """Создание комода"""
        dresser = Dresser(
            width=1200,
            height=900,
            depth=500,
            drawer_count=4,
            drawer_rows=2,
            dresser_type="standard",
            has_legs=True
        )
        db_session.add(dresser)
        db_session.commit()
        
        assert dresser.id is not None
        assert dresser.width == 1200
        assert dresser.height == 900
        assert dresser.drawer_count == 4
        assert dresser.drawer_rows == 2

    def test_dresser_with_parts(self, db_session):
        """Комод с деталями"""
        dresser = Dresser(
            width=1200,
            height=900,
            depth=500
        )
        db_session.add(dresser)
        db_session.commit()
        
        part = DresserPart(
            dresser_id=dresser.id,
            name="боковина",
            part_width=500,
            part_height=900,
            part_depth=18,
            quantity=2
        )
        db_session.add(part)
        db_session.commit()
        
        assert len(dresser.parts) == 1

    def test_dresser_product_relation(self, db_session):
        """Связь с Product"""
        from app.models.catalog import Product
        
        product = Product(
            sku="DR-001",
            name="Комод",
            base_price=15000
        )
        db_session.add(product)
        db_session.flush()
        
        dresser = Dresser(
            product_id=product.id,
            width=1200,
            height=900,
            depth=500
        )
        db_session.add(dresser)
        db_session.commit()
        
        # Проверяем через отдельный запрос
        dresser_check = db_session.query(Dresser).filter_by(product_id=product.id).first()
        assert dresser_check is not None
        assert dresser_check.product_id == product.id
