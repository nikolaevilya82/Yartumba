"""
Тесты Drawer (выдвижные ящики)
"""
import uuid
import pytest
from app.models.components import Drawer


class TestDrawer:
    def test_create_drawer(self, db_session):
        """Создание ящика"""
        drawer = Drawer(
            furniture_type="nightstand",
            furniture_id=uuid.uuid4(),
            drawer_number=1,
            position="full",
            inner_width=400,
            inner_height=150,
            inner_depth=450,
            guide_type="ball",
            has_soft_close=True
        )
        db_session.add(drawer)
        db_session.commit()
        
        assert drawer.id is not None
        assert drawer.furniture_type == "nightstand"
        assert drawer.drawer_number == 1
        assert drawer.guide_type == "ball"

    def test_drawer_positions(self, db_session):
        """Позиции ящиков для комода"""
        dresser_id = uuid.uuid4()
        
        drawer1 = Drawer(
            furniture_type="dresser",
            furniture_id=dresser_id,
            drawer_number=1,
            position="left"
        )
        drawer2 = Drawer(
            furniture_type="dresser",
            furniture_id=dresser_id,
            drawer_number=2,
            position="right"
        )
        drawer3 = Drawer(
            furniture_type="dresser",
            furniture_id=dresser_id,
            drawer_number=3,
            position="center"
        )
        
        db_session.add_all([drawer1, drawer2, drawer3])
        db_session.commit()
        
        assert drawer1.position == "left"
        assert drawer2.position == "right"
        assert drawer3.position == "center"

    def test_drawer_with_slide_guide(self, db_session):
        """Ящик с направляющими"""
        from app.models.materials import SlideGuide
        
        # Создаём направляющие
        slide_guide = SlideGuide(
            name="Направляющие шариковые",
            guide_type="ball",
            extension_type="full",
            length=450,
            load_capacity=30,
            has_soft_close=True,
            price=1500
        )
        db_session.add(slide_guide)
        db_session.commit()
        
        # Создаём ящик с направляющими
        drawer = Drawer(
            furniture_type="nightstand",
            furniture_id=uuid.uuid4(),
            drawer_number=1,
            slide_guide_id=slide_guide.id
        )
        db_session.add(drawer)
        db_session.commit()
        
        assert drawer.slide_guide is not None
        assert drawer.slide_guide.name == "Направляющие шариковые"
