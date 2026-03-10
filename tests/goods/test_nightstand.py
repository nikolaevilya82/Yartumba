"""
Тесты Nightstand (прикроватные тумбы)
"""
import uuid
import pytest
from app.models.goods import Nightstand, NightstandPart


class TestNightstand:
    def test_create_nightstand(self, db_session):
        """Создание прикроватной тумбы"""
        nightstand = Nightstand(
            width=500,
            height=600,
            depth=400,
            drawer_count=1,
            has_open_shelf=True,
            leg_type="standard"
        )
        db_session.add(nightstand)
        db_session.commit()
        
        assert nightstand.id is not None
        assert nightstand.width == 500
        assert nightstand.height == 600
        assert nightstand.drawer_count == 1

    def test_nightstand_with_parts(self, db_session):
        """Тумба с деталями"""
        nightstand = Nightstand(
            width=500,
            height=600,
            depth=400
        )
        db_session.add(nightstand)
        db_session.commit()
        
        part = NightstandPart(
            nightstand_id=nightstand.id,
            name="боковина",
            part_width=400,
            part_height=600,
            part_depth=18,
            quantity=2
        )
        db_session.add(part)
        db_session.commit()
        
        assert len(nightstand.parts) == 1
        assert part.quantity == 2

    def test_nightstand_product_relation(self, db_session):
        """Связь с Product"""
        from app.models.catalog import Product
        
        product = Product(
            sku="NS-001",
            name="Прикроватная тумба",
            base_price=3000
        )
        db_session.add(product)
        db_session.flush()
        
        nightstand = Nightstand(
            product_id=product.id,
            width=500,
            height=600,
            depth=400
        )
        db_session.add(nightstand)
        db_session.commit()
        
        # Проверяем через отдельный запрос
        nightstand_check = db_session.query(Nightstand).filter_by(product_id=product.id).first()
        assert nightstand_check is not None
        assert nightstand_check.product_id == product.id
