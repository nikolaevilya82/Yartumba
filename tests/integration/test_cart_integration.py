"""
Интеграционные тесты корзины

Эти тесты будут тестировать полную цепочку работы корзины:
1. Добавление товара в корзину
2. Обновление количества
3. Применение промокода
4. Расчёт итоговой стоимости
5. Переход к оформлению заказа

Требует реализации:
- app/services/cart_service.py
- app/api/v1/goods_cart.py
"""
import pytest


@pytest.mark.skip(reason="Корзина ещё не реализована")
class TestCartIntegration:
    """Интеграционные тесты корзины"""

    def test_add_item_to_cart(self, client, authenticated_user):
        """Добавление товара в корзину"""
        # TODO: Реализовать после создания корзины
        pass

    def test_update_cart_item_quantity(self, client, authenticated_user, cart_item):
        """Обновление количества товара"""
        # TODO: Реализовать после создания корзины
        pass

    def test_remove_item_from_cart(self, client, authenticated_user, cart_item):
        """Удаление товара из корзины"""
        # TODO: Реализовать после создания корзины
        pass

    def test_cart_total_calculation(self, client, authenticated_user):
        """Расчёт итоговой стоимости корзины"""
        # TODO: Реализовать после создания корзины
        pass

    def test_apply_promocode(self, client, authenticated_user, promocode):
        """Применение промокода"""
        # TODO: Реализовать после создания корзины
        pass

    def test_cart_persistence(self, client, authenticated_user):
        """Сохранение корзины между сессиями"""
        # TODO: Реализовать после создания корзины
        pass


@pytest.mark.skip(reason="Корзина ещё не реализована")
class TestCartWithProducts:
    """Тесты корзины с реальными товарами"""

    def test_add_nightstand_to_cart(self, client, authenticated_user, nightstand_config):
        """Добавление тумбы в корзину"""
        # TODO: Реализовать после создания корзины
        pass

    def test_add_multiple_items(self, client, authenticated_user):
        """Добавление нескольких товаров"""
        # TODO: Реализовать после создания корзины
        pass

    def test_cart_with_different_furniture_types(self, client, authenticated_user):
        """Корзина с разными типами мебели"""
        # TODO: Реализовать после создания корзины
        pass
