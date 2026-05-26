"""
Тесты Pydantic схем корзины
"""
import pytest
from decimal import Decimal
from datetime import datetime
from app.api.v1.goods.cart.schemas import (
    CartBase,
    CartCreate,
    CartUpdate,
    CartResponse,
    CartItemBase,
    CartItemCreate,
    CartItemUpdate,
    CartItemResponse,
    CartSummary,
    AddToCartRequest,
    AddToCartResponse,
    RemoveFromCartResponse,
    UpdateCartItemResponse,
)


class TestCartBase:
    """Тесты базовой схемы корзины"""

    def test_cart_base_with_user_id(self):
        """CartBase с user_id"""
        cart = CartBase(user_id="user-123")
        assert cart.user_id == "user-123"
        assert cart.session_id is None

    def test_cart_base_with_session_id(self):
        """CartBase с session_id"""
        cart = CartBase(session_id="session-456")
        assert cart.session_id == "session-456"
        assert cart.user_id is None

    def test_cart_base_both_none(self):
        """CartBase с обоими None"""
        cart = CartBase()
        assert cart.user_id is None
        assert cart.session_id is None


class TestCartCreate:
    """Тесты схемы создания корзины"""

    def test_cart_create_empty(self):
        """Создание корзины без полей"""
        cart = CartCreate()
        assert cart.user_id is None
        assert cart.session_id is None

    def test_cart_create_with_user(self):
        """Создание корзины пользователя"""
        cart = CartCreate(user_id="user-123")
        assert cart.user_id == "user-123"


class TestCartUpdate:
    """Тесты схемы обновления корзины"""

    def test_cart_update_session_id(self):
        """Обновление session_id"""
        update = CartUpdate(session_id="new-session")
        assert update.session_id == "new-session"

    def test_cart_update_partial(self):
        """Частичное обновление"""
        update = CartUpdate()
        assert update.session_id is None


class TestCartItemBase:
    """Тесты базовой схемы позиции корзины"""

    def test_cart_item_base_valid(self):
        """Валидная позиция"""
        item = CartItemBase(
            furniture_type="bookshelf",
            furniture_id="furn-123",
            configuration_id="config-456",
            quantity=2,
            unit_price=Decimal("8500.00"),
            configuration={"dimensions": {"width": 1000}}
        )
        assert item.furniture_type == "bookshelf"
        assert item.quantity == 2
        assert item.unit_price == Decimal("8500.00")

    def test_cart_item_base_without_snapshot(self):
        """Позиция без конфигурации"""
        item = CartItemBase(
            furniture_type="nightstand",
            furniture_id="furn-789",
            quantity=1,
            unit_price=Decimal("5200.00")
        )
        assert item.configuration is None


class TestCartItemCreate:
    """Тесты схемы создания позиции корзины"""

    def test_cart_item_create_valid(self):
        """Валидное создание позиции"""
        item = CartItemCreate(
            furniture_type="dresser",
            furniture_id="furn-123",
            quantity=1
        )
        assert item.furniture_type == "dresser"
        assert item.quantity == 1
        assert item.configuration_id is None

    def test_cart_item_create_default_quantity(self):
        """Стандартное количество по умолчанию"""
        item = CartItemCreate(
            furniture_type="bookshelf",
            furniture_id="furn-123"
        )
        assert item.quantity == 1

    def test_cart_item_create_with_configuration_id(self):
        """Создание с configuration_id"""
        item = CartItemCreate(
            furniture_type="nightstand",
            furniture_id="furn-123",
            configuration_id="config-456",
            quantity=2
        )
        assert item.configuration_id == "config-456"

    def test_cart_item_create_invalid_furniture_type(self):
        """Неверный тип мебели"""
        with pytest.raises(ValueError) as exc_info:
            CartItemCreate(
                furniture_type="invalid",
                furniture_id="furn-123"
            )
        assert "Неверный тип мебели" in str(exc_info.value)

    def test_cart_item_create_zero_quantity(self):
        """Нулевое количество"""
        with pytest.raises(ValueError):
            CartItemCreate(
                furniture_type="bookshelf",
                furniture_id="furn-123",
                quantity=0
            )

    def test_cart_item_create_negative_quantity(self):
        """Отрицательное количество"""
        with pytest.raises(ValueError):
            CartItemCreate(
                furniture_type="bookshelf",
                furniture_id="furn-123",
                quantity=-1
            )

    def test_cart_item_create_max_quantity(self):
        """Максимальное количество"""
        item = CartItemCreate(
            furniture_type="bookshelf",
            furniture_id="furn-123",
            quantity=99
        )
        assert item.quantity == 99

    def test_cart_item_create_excessive_quantity(self):
        """Чрезмерное количество"""
        with pytest.raises(ValueError):
            CartItemCreate(
                furniture_type="bookshelf",
                furniture_id="furn-123",
                quantity=100
            )


class TestCartItemUpdate:
    """Тесты схемы обновления позиции корзины"""

    def test_cart_item_update_quantity(self):
        """Обновление количества"""
        update = CartItemUpdate(quantity=5)
        assert update.quantity == 5

    def test_cart_item_update_partial(self):
        """Частичное обновление"""
        update = CartItemUpdate()
        assert update.quantity is None

    def test_cart_item_update_zero_quantity(self):
        """Нулевое количество"""
        with pytest.raises(ValueError):
            CartItemUpdate(quantity=0)

    def test_cart_item_update_negative_quantity(self):
        """Отрицательное количество"""
        with pytest.raises(ValueError):
            CartItemUpdate(quantity=-1)


class TestCartSummary:
    """Тесты схемы резюме корзины"""

    def test_cart_summary_valid(self):
        """Валидное резюме"""
        summary = CartSummary(
            total_items=3,
            total_price=Decimal("25200.00")
        )
        assert summary.total_items == 3
        assert summary.total_price == Decimal("25200.00")

    def test_cart_summary_empty(self):
        """Пустая корзина"""
        summary = CartSummary(
            total_items=0,
            total_price=Decimal("0.00")
        )
        assert summary.total_items == 0
        assert summary.total_price == Decimal("0.00")


class TestAddToCartRequest:
    """Тесты запроса добавления в корзину"""

    def test_add_to_cart_valid(self):
        """Валидный запрос"""
        request = AddToCartRequest(
            furniture_type="bookshelf",
            furniture_id="furn-123",
            quantity=2
        )
        assert request.furniture_type == "bookshelf"
        assert request.quantity == 2

    def test_add_to_cart_with_configuration(self):
        """Запрос с конфигурацией"""
        request = AddToCartRequest(
            furniture_type="nightstand",
            furniture_id="furn-123",
            configuration={"dimensions": {"width": 500}},
            quantity=1
        )
        assert request.configuration["dimensions"]["width"] == 500


class TestAddToCartResponse:
    """Тесты ответа добавления в корзину"""

    def test_add_to_cart_response_structure(self):
        """Структура ответа"""
        item = CartItemResponse(
            id="item-123",
            cart_id="cart-456",
            furniture_type="bookshelf",
            furniture_id="furn-123",
            quantity=1,
            unit_price=Decimal("8500.00"),
            item_total=Decimal("8500.00"),
            created_at=datetime.now(),
            updated_at=datetime.now()
        )
        summary = CartSummary(total_items=1, total_price=Decimal("8500.00"))
        
        response = AddToCartResponse(
            cart_item=item,
            cart_summary=summary
        )
        
        assert response.success is True
        assert response.message == "Товар добавлен в корзину"
        assert response.cart_item.id == "item-123"


class TestRemoveFromCartResponse:
    """Тесты ответа удаления из корзины"""

    def test_remove_from_cart_response(self):
        """Структура ответа"""
        summary = CartSummary(total_items=0, total_price=Decimal("0.00"))
        
        response = RemoveFromCartResponse(
            removed_item_id="item-123",
            cart_summary=summary
        )
        
        assert response.success is True
        assert response.message == "Товар удалён из корзины"
        assert response.removed_item_id == "item-123"


class TestUpdateCartItemResponse:
    """Тесты ответа обновления позиции"""

    def test_update_cart_item_response(self):
        """Структура ответа"""
        item = CartItemResponse(
            id="item-123",
            cart_id="cart-456",
            furniture_type="bookshelf",
            furniture_id="furn-123",
            quantity=5,
            unit_price=Decimal("8500.00"),
            item_total=Decimal("42500.00"),
            created_at=datetime.now(),
            updated_at=datetime.now()
        )
        summary = CartSummary(total_items=1, total_price=Decimal("42500.00"))
        
        response = UpdateCartItemResponse(
            cart_item=item,
            cart_summary=summary
        )
        
        assert response.success is True
        assert response.cart_item.quantity == 5


class TestCartItemResponseComputedFields:
    """Тесты вычисляемых полей CartItemResponse"""

    def test_item_total_calculation(self):
        """Расчёт итоговой суммы позиции"""
        item = CartItemResponse(
            id="item-123",
            cart_id="cart-456",
            furniture_type="bookshelf",
            furniture_id="furn-123",
            quantity=3,
            unit_price=Decimal("8500.00"),
            item_total=Decimal("25500.00"),  # 8500 * 3
            created_at=datetime.now(),
            updated_at=datetime.now()
        )
        assert item.item_total == item.unit_price * item.quantity

    def test_furniture_name_optional(self):
        """Название мебели опционально"""
        item = CartItemResponse(
            id="item-123",
            cart_id="cart-456",
            furniture_type="bookshelf",
            furniture_id="furn-123",
            quantity=1,
            unit_price=Decimal("8500.00"),
            item_total=Decimal("8500.00"),
            furniture_name="Книжная полка стандарт",
            created_at=datetime.now(),
            updated_at=datetime.now()
        )
        assert item.furniture_name == "Книжная полка стандарт"

    def test_furniture_name_none(self):
        """Название мебели отсутствует"""
        item = CartItemResponse(
            id="item-123",
            cart_id="cart-456",
            furniture_type="bookshelf",
            furniture_id="furn-123",
            quantity=1,
            unit_price=Decimal("8500.00"),
            item_total=Decimal("8500.00"),
            created_at=datetime.now(),
            updated_at=datetime.now()
        )
        assert item.furniture_name is None


class TestCartResponseComputedFields:
    """Тесты вычисляемых полей CartResponse"""

    def test_total_items_computed(self):
        """Подсчёт количества товаров"""
        item1 = CartItemResponse(
            id="item-1",
            cart_id="cart-123",
            furniture_type="bookshelf",
            furniture_id="furn-1",
            quantity=2,
            unit_price=Decimal("8500.00"),
            item_total=Decimal("17000.00"),
            created_at=datetime.now(),
            updated_at=datetime.now()
        )
        item2 = CartItemResponse(
            id="item-2",
            cart_id="cart-123",
            furniture_type="nightstand",
            furniture_id="furn-2",
            quantity=1,
            unit_price=Decimal("5200.00"),
            item_total=Decimal("5200.00"),
            created_at=datetime.now(),
            updated_at=datetime.now()
        )
        
        cart = CartResponse(
            id="cart-123",
            user_id="user-456",
            items=[item1, item2],
            total_items=3,  # 2 + 1
            total_price=Decimal("22200.00"),
            created_at=datetime.now(),
            updated_at=datetime.now()
        )
        
        assert cart.total_items == 3

    def test_total_price_computed(self):
        """Подсчёт итоговой суммы"""
        item = CartItemResponse(
            id="item-1",
            cart_id="cart-123",
            furniture_type="bookshelf",
            furniture_id="furn-1",
            quantity=1,
            unit_price=Decimal("8500.00"),
            item_total=Decimal("8500.00"),
            created_at=datetime.now(),
            updated_at=datetime.now()
        )
        
        cart = CartResponse(
            id="cart-123",
            items=[item],
            total_items=1,
            total_price=Decimal("8500.00"),
            created_at=datetime.now(),
            updated_at=datetime.now()
        )
        
        assert cart.total_price == Decimal("8500.00")
