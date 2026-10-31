"""
Фикстуры для тестов
"""
import uuid

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.core.db_setup import Base
from app.core.dependencies import get_db
from app.main import app


@pytest.fixture(scope="function")
def engine():
    """
    Создаёт SQLite в памяти для каждого теста.

    StaticPool + check_same_thread=False нужны, чтобы TestClient (запросы
    выполняются в отдельном потоке) работал с той же самой in-memory БД.
    """
    engine = create_engine(
        "sqlite:///:memory:",
        echo=False,
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    Base.metadata.create_all(engine)
    yield engine
    Base.metadata.drop_all(engine)
    engine.dispose()


@pytest.fixture(scope="function")
def db_session(engine):
    """Сессия БД для тестов"""
    Session = sessionmaker(bind=engine)
    session = Session()
    yield session
    session.close()


@pytest.fixture(scope="function")
def client(db_session):
    """
    HTTP-клиент приложения с подменой `get_db` на тестовую сессию.

    Запросы идут через реальные роутеры, но данные пишутся в in-memory SQLite,
    поэтому тест может проверять результат напрямую через `db_session`.
    """
    def override_get_db():
        yield db_session

    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.pop(get_db, None)


@pytest.fixture(scope="function")
def authenticated_user(client):
    """
    Авторизованный пользователь.

    Авторизация в проекте не реализована, поэтому зависимости
    `get_current_user_id` и `get_optional_user_id` подменяются на фиксированный ID.
    """
    from app.api.v1.goods.cart.dependencies import (
        get_current_user_id,
        get_optional_user_id,
    )

    user_id = uuid.uuid4()
    app.dependency_overrides[get_current_user_id] = lambda: user_id
    app.dependency_overrides[get_optional_user_id] = lambda: user_id

    yield user_id

    app.dependency_overrides.pop(get_current_user_id, None)
    app.dependency_overrides.pop(get_optional_user_id, None)


@pytest.fixture(scope="function")
def nightstand_config():
    """Конфигурация прикроватной тумбы для тестов конфигуратора"""
    return {
        "width": 500,
        "height": 600,
        "depth": 400,
        "drawers": {"count": 1, "slide_guide_id": None},
        "bodyMaterial": {"sheet_material_id": None, "edge_id": None},
        "hardware": {"hinge_id": None, "support_id": None},
    }


@pytest.fixture(scope="function")
def promocode():
    """
    Промокод для тестов корзины.

    Отдельной таблицы промокодов в проекте нет, поэтому фикстура возвращает
    словарь с параметрами скидки.
    """
    return {
        "code": "SALE10",
        "discount_percent": 10,
        "is_active": True,
        "min_total": 0,
    }


@pytest.fixture(scope="function")
def cart_item(db_session, authenticated_user):
    """
    Готовая позиция корзины авторизованного пользователя.

    Создаёт товар каталога, прикроватную тумбу, корзину пользователя
    и одну позицию в ней. Возвращает объект CartItem.
    """
    from app.models.cart import Cart, CartItem
    from app.models.catalog import Product
    from app.models.goods import Nightstand

    product = Product(
        sku=f"NS-{uuid.uuid4().hex[:8]}",
        name="Тумба прикроватная (тест)",
        base_price=500000,
    )
    db_session.add(product)
    db_session.flush()

    nightstand = Nightstand(
        product_id=product.id,
        width=500,
        height=600,
        depth=400,
        drawer_count=1,
    )
    db_session.add(nightstand)
    db_session.flush()

    cart = Cart(user_id=authenticated_user)
    db_session.add(cart)
    db_session.flush()

    item = CartItem(
        cart_id=cart.id,
        product_id=product.id,
        furniture_type="nightstand",
        furniture_id=nightstand.id,
        quantity=1,
        unit_price=500000,
        total_price=500000,
        configuration={},
    )
    db_session.add(item)
    db_session.commit()
    db_session.refresh(item)

    return item
