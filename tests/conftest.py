"""
Фикстуры для тестов
"""
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.core.db_setup import Base


@pytest.fixture(scope="function")
def engine():
    """Создаёт SQLite в памяти для каждого теста"""
    engine = create_engine("sqlite:///:memory:", echo=False)
    Base.metadata.create_all(engine)
    yield engine
    Base.metadata.drop_all(engine)


@pytest.fixture(scope="function")
def db_session(engine):
    """Сессия БД для тестов"""
    Session = sessionmaker(bind=engine)
    session = Session()
    yield session
    session.close()
