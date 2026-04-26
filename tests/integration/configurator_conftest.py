"""
Фикстуры для интеграционных тестов конфигуратора
"""
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.core.db_setup import Base
from app.models.materials import SheetMaterial, EdgeMaterial, SlideGuide, Hinge, Support


@pytest.fixture(scope="function")
def db_engine():
    """Создаёт SQLite в памяти для каждого теста"""
    engine = create_engine("sqlite:///:memory:", echo=False)
    Base.metadata.create_all(engine)
    yield engine
    Base.metadata.drop_all(engine)


@pytest.fixture(scope="function")
def db_session(db_engine):
    """Сессия БД для тестов"""
    Session = sessionmaker(bind=db_engine)
    session = Session()
    yield session
    session.close()


@pytest.fixture(scope="function")
def sample_sheet_material(db_session):
    """Тестовый листовой материал"""
    material = SheetMaterial(
        name="ЛДСП Белый",
        material_type="ldsp",
        thickness=16,
        standard_width=2800,
        standard_height=2070,
        decor_name="Белый матовый",
        hex_code="#FFFFFF",
        price=1500,
        is_active="active"
    )
    db_session.add(material)
    db_session.commit()
    db_session.refresh(material)
    return material


@pytest.fixture(scope="function")
def sample_edge_material(db_session, sample_sheet_material):
    """Тестовая кромка"""
    edge = EdgeMaterial(
        sheet_material_id=sample_sheet_material.id,
        edge_type="PVC",
        thickness=0.5,
        width=22,
        decor_name="Белый",
        price_per_meter=10
    )
    db_session.add(edge)
    db_session.commit()
    db_session.refresh(edge)
    return edge


@pytest.fixture(scope="function")
def sample_slide_guide(db_session):
    """Тестовые направляющие"""
    guide = SlideGuide(
        name="Направляющие телескопические",
        guide_type="ball_bearing",
        extension_type="full",
        length=400,
        load_capacity=25,
        has_soft_close=True,
        price=350
    )
    db_session.add(guide)
    db_session.commit()
    db_session.refresh(guide)
    return guide


@pytest.fixture(scope="function")
def sample_hinge(db_session):
    """Тестовые петли"""
    hinge = Hinge(
        name="Петля с доводчиком",
        hinge_type="concealed",
        mounting_type="clip_on",
        opening_angle=110,
        has_soft_close=True,
        price=250
    )
    db_session.add(hinge)
    db_session.commit()
    db_session.refresh(hinge)
    return hinge


@pytest.fixture(scope="function")
def sample_support(db_session):
    """Тестовая ножка"""
    support = Support(
        name="Ножка пластиковая",
        support_type="plastic",
        material="plastic",
        height=100,
        diameter=40,
        is_adjustable=False,
        price=50
    )
    db_session.add(support)
    db_session.commit()
    db_session.refresh(support)
    return support
