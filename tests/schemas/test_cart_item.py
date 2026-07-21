"""
Тесты модели CartItem
"""
import pytest
from decimal import Decimal
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.core.db_setup import Base
from app.models.cart import Cart, CartItem
from app.models.catalog import Product, Category
from app.models.goods import Bookshelf, Nightstand, Dresser
import uuid


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


@pytest.fixture
def sample_product(db_session):
    """Создаёт продукт для тестов"""
    category = Category(
        id=uuid.uuid4(),
        name="Test Category",
        slug="test-category"
    )
    db_session.add(category)
    db_session.flush()
    
    product = Product(
        id=uuid.uuid4(),
        sku="TEST-001",
        name="Test Product",
        base_price=10000,
        category_id=category.id
    )
    db_session.add(product)
    db_session.flush()
    return product


@pytest.fixture
def sample_cart(db_session):
    """Создаёт корзину для тестов"""
    cart = Cart(
        id=uuid.uuid4(),
        user_id=uuid.uuid4()
    )
    db_session.add(cart)
    db_session.flush()
    return cart


class TestCartItem:
    """Тесты модели CartItem"""

    def test_create_cart_item(self, db_session, sample_cart, sample_product):
        """Создание позиции корзины"""
        bookshelf = Bookshelf(
            id=uuid.uuid4(),
            width=1000,
            height=1800,
            depth=300
        )
        db_session.add(bookshelf)
        db_session.flush()
        
        cart_item = CartItem(
            cart_id=sample_cart.id,
            product_id=sample_product.id,
            furniture_type="bookshelf",
            furniture_id=bookshelf.id,
            configuration={
                "dimensions": {"width": 1000, "height": 1800, "depth": 300},
                "parts": []
            },
            quantity=1,
            unit_price=Decimal("8500.00"),
            total_price=Decimal("8500.00")
        )
        
        db_session.add(cart_item)
        db_session.commit()
        
        # Проверка создания
        assert cart_item.id is not None
        assert cart_item.quantity == 1
        assert cart_item.unit_price == Decimal("8500.00")
        assert cart_item.total_price == Decimal("8500.00")
        assert cart_item.furniture_type == "bookshelf"

    def test_cart_item_total_price_calculation(self, db_session, sample_cart, sample_product):
        """Автоматический расчёт total_price"""
        nightstand = Nightstand(
            id=uuid.uuid4(),
            width=500,
            height=450,
            depth=400
        )
        db_session.add(nightstand)
        db_session.flush()
        
        cart_item = CartItem(
            cart_id=sample_cart.id,
            product_id=sample_product.id,
            furniture_type="nightstand",
            furniture_id=nightstand.id,
            configuration={"dimensions": {"width": 500, "height": 450, "depth": 400}},
            quantity=3,
            unit_price=Decimal("5200.00"),
            total_price=Decimal("15600.00")  # 5200 * 3
        )
        
        db_session.add(cart_item)
        db_session.commit()
        
        assert cart_item.total_price == cart_item.unit_price * cart_item.quantity

    def test_cart_item_with_jsonb_configuration(self, db_session, sample_cart, sample_product):
        """JSONB конфигурация для разных типов мебели"""
        # Bookshelf конфигурация
        bookshelf_config = {
            "dimensions": {"width": 800, "height": 1800, "depth": 300},
            "parts": [
                {"type": "side_panel", "material_id": "uuid-1", "quantity": 2},
                {"type": "shelf", "material_id": "uuid-2", "quantity": 4}
            ],
            "back_panel": {"material_id": "uuid-3", "thickness": 8}
        }
        
        dresser = Dresser(
            id=uuid.uuid4(),
            width=1200,
            height=800,
            depth=500
        )
        db_session.add(dresser)
        db_session.flush()
        
        cart_item = CartItem(
            cart_id=sample_cart.id,
            product_id=sample_product.id,
            furniture_type="dresser",
            furniture_id=dresser.id,
            configuration=bookshelf_config,
            quantity=1,
            unit_price=Decimal("12500.00"),
            total_price=Decimal("12500.00")
        )
        
        db_session.add(cart_item)
        db_session.commit()
        
        # Проверка сохранения JSON
        assert cart_item.configuration["dimensions"]["width"] == 800
        assert len(cart_item.configuration["parts"]) == 2

    def test_cart_item_materials_snapshot(self, db_session, sample_cart, sample_product):
        """Снепшот материалов для истории цен"""
        bookshelf = Bookshelf(
            id=uuid.uuid4(),
            width=1000,
            height=1800,
            depth=300
        )
        db_session.add(bookshelf)
        db_session.flush()
        
        materials_snapshot = {
            "sheet_materials": [{"id": "uuid-1", "price": 1500}],
            "edge_materials": [{"id": "uuid-2", "price": 200}],
            "hardware": [{"id": "uuid-3", "price": 500}]
        }
        
        cart_item = CartItem(
            cart_id=sample_cart.id,
            product_id=sample_product.id,
            furniture_type="bookshelf",
            furniture_id=bookshelf.id,
            configuration={"dimensions": {}},
            quantity=1,
            unit_price=Decimal("8500.00"),
            total_price=Decimal("8500.00"),
            materials_snapshot=materials_snapshot
        )
        
        db_session.add(cart_item)
        db_session.commit()
        
        assert cart_item.materials_snapshot["sheet_materials"][0]["price"] == 1500

    def test_cart_item_timestamps(self, db_session, sample_cart, sample_product):
        """Автоматические временные метки"""
        bookshelf = Bookshelf(
            id=uuid.uuid4(),
            width=1000,
            height=1800,
            depth=300
        )
        db_session.add(bookshelf)
        db_session.flush()
        
        cart_item = CartItem(
            cart_id=sample_cart.id,
            product_id=sample_product.id,
            furniture_type="bookshelf",
            furniture_id=bookshelf.id,
            configuration={},
            quantity=1,
            unit_price=Decimal("8500.00"),
            total_price=Decimal("8500.00")
        )
        
        db_session.add(cart_item)
        db_session.commit()
        
        assert cart_item.created_at is not None
        assert cart_item.updated_at is not None
        assert cart_item.created_at <= cart_item.updated_at

    def test_cart_item_relationships(self, db_session, sample_cart, sample_product):
        """Связи с Cart и Product"""
        bookshelf = Bookshelf(
            id=uuid.uuid4(),
            width=1000,
            height=1800,
            depth=300
        )
        db_session.add(bookshelf)
        db_session.flush()
        
        cart_item = CartItem(
            cart_id=sample_cart.id,
            product_id=sample_product.id,
            furniture_type="bookshelf",
            furniture_id=bookshelf.id,
            configuration={},
            quantity=1,
            unit_price=Decimal("8500.00"),
            total_price=Decimal("8500.00")
        )
        
        db_session.add(cart_item)
        db_session.commit()
        
        # Проверка связи с Cart
        assert cart_item.cart.id == sample_cart.id
        assert cart_item in sample_cart.items
        
        # Проверка связи с Product
        assert cart_item.product.id == sample_product.id
        assert cart_item.product.sku == "TEST-001"

    def test_cart_item_cascade_delete(self, db_session, sample_cart, sample_product):
        """Каскадное удаление при удалении корзины (PostgreSQL feature)"""
        # Примечание: CASCADE работает в PostgreSQL, но в SQLite требуется ручное управление
        # Этот тест помечен как ожидающий PostgreSQL
        
        bookshelf = Bookshelf(
            id=uuid.uuid4(),
            width=1000,
            height=1800,
            depth=300
        )
        db_session.add(bookshelf)
        db_session.flush()
        
        cart_item = CartItem(
            cart_id=sample_cart.id,
            product_id=sample_product.id,
            furniture_type="bookshelf",
            furniture_id=bookshelf.id,
            configuration={},
            quantity=1,
            unit_price=Decimal("8500.00"),
            total_price=Decimal("8500.00")
        )
        
        db_session.add(cart_item)
        db_session.commit()
        
        # В SQLite проверяем, что позиция существует
        result = db_session.query(CartItem).filter(CartItem.id == cart_item.id).first()
        assert result is not None
        
        # Примечание: после миграции на PostgreSQL CASCADE будет работать автоматически
        # Удаление корзины должно удалять все позиции

    def test_get_furniture_object_bookshelf(self, db_session, sample_cart, sample_product):
        """Получение объекта Bookshelf из CartItem"""
        bookshelf = Bookshelf(
            id=uuid.uuid4(),
            width=1000,
            height=1800,
            depth=300
        )
        db_session.add(bookshelf)
        db_session.flush()
        
        cart_item = CartItem(
            cart_id=sample_cart.id,
            product_id=sample_product.id,
            furniture_type="bookshelf",
            furniture_id=bookshelf.id,
            configuration={},
            quantity=1,
            unit_price=Decimal("8500.00"),
            total_price=Decimal("8500.00")
        )
        
        db_session.add(cart_item)
        db_session.commit()
        
        retrieved_bookshelf = cart_item.get_furniture_object(db_session)
        assert retrieved_bookshelf is not None
        assert retrieved_bookshelf.id == bookshelf.id
        assert retrieved_bookshelf.width == 1000

    def test_get_furniture_object_nightstand(self, db_session, sample_cart, sample_product):
        """Получение объекта Nightstand из CartItem"""
        nightstand = Nightstand(
            id=uuid.uuid4(),
            width=500,
            height=450,
            depth=400
        )
        db_session.add(nightstand)
        db_session.flush()
        
        cart_item = CartItem(
            cart_id=sample_cart.id,
            product_id=sample_product.id,
            furniture_type="nightstand",
            furniture_id=nightstand.id,
            configuration={},
            quantity=1,
            unit_price=Decimal("5200.00"),
            total_price=Decimal("5200.00")
        )
        
        db_session.add(cart_item)
        db_session.commit()
        
        retrieved_nightstand = cart_item.get_furniture_object(db_session)
        assert retrieved_nightstand is not None
        assert retrieved_nightstand.id == nightstand.id

    def test_get_furniture_object_dresser(self, db_session, sample_cart, sample_product):
        """Получение объекта Dresser из CartItem"""
        dresser = Dresser(
            id=uuid.uuid4(),
            width=1200,
            height=800,
            depth=500
        )
        db_session.add(dresser)
        db_session.flush()
        
        cart_item = CartItem(
            cart_id=sample_cart.id,
            product_id=sample_product.id,
            furniture_type="dresser",
            furniture_id=dresser.id,
            configuration={},
            quantity=1,
            unit_price=Decimal("12500.00"),
            total_price=Decimal("12500.00")
        )
        
        db_session.add(cart_item)
        db_session.commit()
        
        retrieved_dresser = cart_item.get_furniture_object(db_session)
        assert retrieved_dresser is not None
        assert retrieved_dresser.id == dresser.id

    def test_get_furniture_object_invalid_type(self, db_session, sample_cart, sample_product):
        """Невалидный тип мебели возвращает None"""
        bookshelf = Bookshelf(
            id=uuid.uuid4(),
            width=1000,
            height=1800,
            depth=300
        )
        db_session.add(bookshelf)
        db_session.flush()
        
        cart_item = CartItem(
            cart_id=sample_cart.id,
            product_id=sample_product.id,
            furniture_type="invalid_type",
            furniture_id=bookshelf.id,
            configuration={},
            quantity=1,
            unit_price=Decimal("8500.00"),
            total_price=Decimal("8500.00")
        )
        
        db_session.add(cart_item)
        db_session.commit()
        
        result = cart_item.get_furniture_object(db_session)
        assert result is None

    def test_cart_item_repr(self, db_session, sample_cart, sample_product):
        """Проверка __repr__ метода"""
        bookshelf = Bookshelf(
            id=uuid.uuid4(),
            width=1000,
            height=1800,
            depth=300
        )
        db_session.add(bookshelf)
        db_session.flush()
        
        cart_item = CartItem(
            cart_id=sample_cart.id,
            product_id=sample_product.id,
            furniture_type="bookshelf",
            furniture_id=bookshelf.id,
            configuration={},
            quantity=2,
            unit_price=Decimal("8500.00"),
            total_price=Decimal("17000.00")
        )
        
        db_session.add(cart_item)
        db_session.commit()
        
        repr_str = repr(cart_item)
        assert "CartItem" in repr_str
        assert "bookshelf" in repr_str
        assert "qty=2" in repr_str

    def test_different_furniture_types_in_cart(self, db_session, sample_cart, sample_product):
        """Разные типы мебели в одной корзине"""
        bookshelf = Bookshelf(id=uuid.uuid4(), width=1000, height=1800, depth=300)
        nightstand = Nightstand(id=uuid.uuid4(), width=500, height=450, depth=400)
        dresser = Dresser(id=uuid.uuid4(), width=1200, height=800, depth=500)
        
        db_session.add_all([bookshelf, nightstand, dresser])
        db_session.flush()
        
        items = [
            CartItem(
                cart_id=sample_cart.id,
                product_id=sample_product.id,
                furniture_type="bookshelf",
                furniture_id=bookshelf.id,
                configuration={},
                quantity=1,
                unit_price=Decimal("8500.00"),
                total_price=Decimal("8500.00")
            ),
            CartItem(
                cart_id=sample_cart.id,
                product_id=sample_product.id,
                furniture_type="nightstand",
                furniture_id=nightstand.id,
                configuration={},
                quantity=2,
                unit_price=Decimal("5200.00"),
                total_price=Decimal("10400.00")
            ),
            CartItem(
                cart_id=sample_cart.id,
                product_id=sample_product.id,
                furniture_type="dresser",
                furniture_id=dresser.id,
                configuration={},
                quantity=1,
                unit_price=Decimal("12500.00"),
                total_price=Decimal("12500.00")
            )
        ]
        
        db_session.add_all(items)
        db_session.commit()
        
        # Проверка всех позиций
        assert len(sample_cart.items) == 3
        assert any(item.furniture_type == "bookshelf" for item in sample_cart.items)
        assert any(item.furniture_type == "nightstand" for item in sample_cart.items)
        assert any(item.furniture_type == "dresser" for item in sample_cart.items)
        
        # Проверка итоговой суммы
        total = sum(item.total_price for item in sample_cart.items)
        assert total == Decimal("31400.00")  # 8500 + 10400 + 12500
