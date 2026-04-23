"""
Placeholder тесты для не реализованных функций конфигуратора

Эти тесты помечены как skipped и будут активированы после реализации соответствующего функционала.
"""
import pytest


@pytest.mark.skip(reason="Сохранение конфигураций ещё не реализовано")
class TestConfigurationSave:
    """Тесты сохранения конфигураций"""

    def test_save_configuration(self):
        """Сохранение конфигурации"""
        pass

    def test_get_saved_configurations(self):
        """Получение сохранённых конфигураций"""
        pass

    def test_update_saved_configuration(self):
        """Обновление сохранённой конфигурации"""
        pass

    def test_delete_saved_configuration(self):
        """Удаление сохранённой конфигурации"""
        pass

    def test_user_can_only_view_own_configurations(self):
        """Пользователь видит только свои конфигурации"""
        pass


@pytest.mark.skip(reason="Создание товара из конфигурации ещё не реализовано")
class TestConfigurationToProduct:
    """Тесты создания товара из конфигурации"""

    def test_create_product_from_configuration(self):
        """Создание товара из конфигурации"""
        pass

    def test_configuration_becomes_furniture(self):
        """Конфигурация становится мебелью"""
        pass

    def test_parts_generated_from_configuration(self):
        """Детали генерируются из конфигурации"""
        pass


@pytest.mark.skip(reason="Получение опций требует рефакторинга сервиса для инъекции зависимостей")
class TestConfiguratorOptions:
    """Тесты получения опций конфигуратора"""

    def test_get_materials_list(self):
        """Получение списка материалов"""
        pass

    def test_get_hardware_list(self):
        """Получение списка фурнитуры"""
        pass

    def test_get_available_colors(self):
        """Получение доступных цветов"""
        pass
