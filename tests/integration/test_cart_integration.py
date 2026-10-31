"""
Интеграционные тесты корзины

Проверяют полную цепочку работы корзины через HTTP API:
1. Добавление товара в корзину
2. Обновление количества
3. Удаление товара и очистка корзины
4. Расчёт итоговой стоимости
5. Сохранение корзины между запросами
6. Объединение гостевой и пользовательской корзин
"""
import uuid

import pytest

from app.models.catalog import Product
from app.models.goods import Bookshelf, Dresser, Nightstand

CART_URL = "/v1/goods/cart"
ITEMS_URL = f"{CART_URL}/items"


def create_furniture(db_session, furniture_type: str, base_price: int = 500000):
    """
    Создать товар каталога и изделие нужного типа.

    Args:
        db_session: Сессия БД
        furniture_type: bookshelf | nightstand | dresser
        base_price: Базовая цена товара (в копейках)

    Returns:
        tuple: (product, furniture)
    """
    product = Product(
        sku=f"{furniture_type[:3].upper()}-{uuid.uuid4().hex[:8]}",
        name=f"Изделие {furniture_type} (тест)",
        base_price=base_price,
    )
    db_session.add(product)
    db_session.flush()

    if furniture_type == "bookshelf":
        furniture = Bookshelf(
            product_id=product.id, width=800, height=1200, depth=300, shelf_count=3
        )
    elif furniture_type == "dresser":
        furniture = Dresser(
            product_id=product.id, width=1000, height=800, depth=450, drawer_count=4
        )
    else:
        furniture = Nightstand(
            product_id=product.id, width=500, height=600, depth=400, drawer_count=1
        )

    db_session.add(furniture)
    db_session.commit()
    db_session.refresh(furniture)

    return product, furniture


class TestCartIntegration:
    """Интеграционные тесты корзины"""

    def test_add_item_to_cart(self, client, authenticated_user, db_session):
        """Добавление товара в корзину"""
        _, nightstand = create_furniture(db_session, "nightstand")

        response = client.post(
            ITEMS_URL,
            json={
                "furniture_type": "nightstand",
                "furniture_id": str(nightstand.id),
                "quantity": 1,
            },
        )

        assert response.status_code == 201, response.text
        data = response.json()
        assert data["cart_item"]["furniture_type"] == "nightstand"
        assert data["cart_item"]["furniture_id"] == str(nightstand.id)
        assert data["cart_item"]["quantity"] == 1
        assert float(data["cart_item"]["unit_price"]) == 500000
        assert data["cart_summary"]["total_items"] == 1

    def test_add_nonexistent_item_returns_404(self, client, authenticated_user):
        """Добавление несуществующего товара возвращает 404"""
        response = client.post(
            ITEMS_URL,
            json={
                "furniture_type": "nightstand",
                "furniture_id": str(uuid.uuid4()),
                "quantity": 1,
            },
        )

        assert response.status_code == 404

    def test_add_item_with_invalid_type_returns_422(self, client, authenticated_user):
        """Неверный тип мебели отклоняется валидацией схемы"""
        response = client.post(
            ITEMS_URL,
            json={
                "furniture_type": "chair",
                "furniture_id": str(uuid.uuid4()),
                "quantity": 1,
            },
        )

        assert response.status_code == 422

    def test_update_cart_item_quantity(
        self, client, authenticated_user, cart_item, db_session
    ):
        """Обновление количества товара"""
        response = client.patch(
            f"{ITEMS_URL}/{cart_item.id}",
            json={"quantity": 3},
        )

        assert response.status_code == 200, response.text
        data = response.json()
        assert data["cart_item"]["quantity"] == 3
        assert float(data["cart_item"]["item_total"]) == 1500000
        assert data["cart_summary"]["total_items"] == 3

        db_session.refresh(cart_item)
        assert cart_item.quantity == 3

    def test_update_missing_item_returns_404(
        self, client, authenticated_user, cart_item
    ):
        """Обновление несуществующей позиции возвращает 404"""
        response = client.patch(
            f"{ITEMS_URL}/{uuid.uuid4()}",
            json={"quantity": 2},
        )

        assert response.status_code == 404

    def test_remove_item_from_cart(
        self, client, authenticated_user, cart_item, db_session
    ):
        """Удаление товара из корзины"""
        from app.models.cart import CartItem

        response = client.delete(f"{ITEMS_URL}/{cart_item.id}")

        assert response.status_code == 200, response.text
        data = response.json()
        assert data["removed_item_id"] == str(cart_item.id)
        assert data["cart_summary"]["total_items"] == 0
        assert db_session.query(CartItem).count() == 0

    def test_clear_cart(self, client, authenticated_user, cart_item, db_session):
        """Полная очистка корзины"""
        from app.models.cart import CartItem

        response = client.delete(f"{CART_URL}/")

        assert response.status_code == 200
        assert response.json() == {"message": "Cart cleared"}
        assert db_session.query(CartItem).count() == 0

    def test_cart_total_calculation(self, client, authenticated_user, db_session):
        """Расчёт итоговой стоимости корзины"""
        _, nightstand = create_furniture(db_session, "nightstand", base_price=500000)
        _, dresser = create_furniture(db_session, "dresser", base_price=700000)

        client.post(
            ITEMS_URL,
            json={
                "furniture_type": "nightstand",
                "furniture_id": str(nightstand.id),
                "quantity": 2,
            },
        )
        client.post(
            ITEMS_URL,
            json={
                "furniture_type": "dresser",
                "furniture_id": str(dresser.id),
                "quantity": 1,
            },
        )

        response = client.get(f"{CART_URL}/")

        assert response.status_code == 200, response.text
        data = response.json()
        assert data["total_items"] == 3
        # 2 * 500000 + 1 * 700000
        assert float(data["total_price"]) == 1700000
        assert len(data["items"]) == 2

    def test_cart_persistence(self, client, authenticated_user, db_session):
        """Корзина сохраняется между запросами одного пользователя"""
        _, nightstand = create_furniture(db_session, "nightstand")

        client.post(
            ITEMS_URL,
            json={
                "furniture_type": "nightstand",
                "furniture_id": str(nightstand.id),
                "quantity": 1,
            },
        )

        first = client.get(f"{CART_URL}/").json()
        second = client.get(f"{CART_URL}/").json()

        assert first["id"] == second["id"]
        assert second["total_items"] == 1
        assert len(second["items"]) == 1

    @pytest.mark.skip(reason="Промокоды не реализованы в API корзины")
    def test_apply_promocode(self, client, authenticated_user, promocode):
        """Применение промокода"""
        response = client.post(
            f"{CART_URL}/promocode",
            json={"code": promocode["code"]},
        )

        assert response.status_code == 200


class TestCartWithProducts:
    """Тесты корзины с реальными товарами"""

    def test_add_nightstand_to_cart(
        self, client, authenticated_user, db_session, nightstand_config
    ):
        """Добавление тумбы в корзину вместе с конфигурацией"""
        _, nightstand = create_furniture(db_session, "nightstand")

        response = client.post(
            ITEMS_URL,
            json={
                "furniture_type": "nightstand",
                "furniture_id": str(nightstand.id),
                "configuration": nightstand_config,
                "quantity": 1,
            },
        )

        assert response.status_code == 201, response.text
        assert response.json()["cart_item"]["configuration"] == nightstand_config

    def test_add_multiple_items(self, client, authenticated_user, db_session):
        """Добавление нескольких товаров"""
        _, nightstand = create_furniture(db_session, "nightstand")
        _, bookshelf = create_furniture(db_session, "bookshelf", base_price=300000)

        client.post(
            ITEMS_URL,
            json={
                "furniture_type": "nightstand",
                "furniture_id": str(nightstand.id),
                "quantity": 1,
            },
        )
        client.post(
            ITEMS_URL,
            json={
                "furniture_type": "bookshelf",
                "furniture_id": str(bookshelf.id),
                "quantity": 2,
            },
        )

        data = client.get(f"{CART_URL}/").json()

        assert len(data["items"]) == 2
        assert data["total_items"] == 3
        # 1 * 500000 + 2 * 300000
        assert float(data["total_price"]) == 1100000

    def test_cart_with_different_furniture_types(
        self, client, authenticated_user, db_session
    ):
        """Корзина с разными типами мебели"""
        _, nightstand = create_furniture(db_session, "nightstand")
        _, dresser = create_furniture(db_session, "dresser")

        client.post(
            ITEMS_URL,
            json={
                "furniture_type": "nightstand",
                "furniture_id": str(nightstand.id),
                "quantity": 1,
            },
        )
        client.post(
            ITEMS_URL,
            json={
                "furniture_type": "dresser",
                "furniture_id": str(dresser.id),
                "quantity": 1,
            },
        )

        data = client.get(f"{CART_URL}/").json()
        types = {item["furniture_type"] for item in data["items"]}

        assert types == {"nightstand", "dresser"}

    def test_adding_same_item_increases_quantity(
        self, client, authenticated_user, db_session
    ):
        """Повторное добавление того же товара увеличивает количество"""
        _, nightstand = create_furniture(db_session, "nightstand")
        payload = {
            "furniture_type": "nightstand",
            "furniture_id": str(nightstand.id),
            "quantity": 1,
        }

        client.post(ITEMS_URL, json=payload)
        client.post(ITEMS_URL, json=payload)

        data = client.get(f"{CART_URL}/").json()

        assert len(data["items"]) == 1
        assert data["items"][0]["quantity"] == 2
        assert data["total_items"] == 2


class TestCartMerge:
    """Объединение гостевой и пользовательской корзин"""

    def test_merge_guest_cart_into_user_cart(
        self, client, authenticated_user, db_session
    ):
        """Гостевая корзина переносится в корзину пользователя"""
        from app.models.cart import Cart, CartItem

        _, nightstand = create_furniture(db_session, "nightstand")

        # Гостевая корзина создаётся напрямую в БД: через API все запросы
        # в этом тесте идут от авторизованного пользователя
        session_id = f"guest-{uuid.uuid4()}"
        guest_cart = Cart(session_id=session_id)
        db_session.add(guest_cart)
        db_session.flush()

        guest_item = CartItem(
            cart_id=guest_cart.id,
            product_id=nightstand.product_id,
            furniture_type="nightstand",
            furniture_id=nightstand.id,
            quantity=2,
            unit_price=500000,
            total_price=1000000,
            configuration={},
        )
        db_session.add(guest_item)
        db_session.commit()

        response = client.post(
            f"{CART_URL}/merge",
            json={"session_id": session_id},
        )

        assert response.status_code == 200, response.text
        data = response.json()
        assert data["user_id"] == str(authenticated_user)
        assert data["total_items"] == 2
        assert len(data["items"]) == 1

        # Гостевая корзина удалена
        assert db_session.query(Cart).filter(Cart.session_id == session_id).first() is None
