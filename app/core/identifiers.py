"""
Приведение идентификаторов к типу UUID.

Колонки с UUID принимают объекты `uuid.UUID`. Значения, приходящие из HTTP
(path- и query-параметры, JSON), всегда строковые, поэтому перед подстановкой
в фильтры их нужно привести к UUID. На PostgreSQL сравнение со строкой тоже
работает, но приведение делает поведение одинаковым на всех СУБД
(включая SQLite в тестах).
"""
import uuid
from typing import Any, Optional


# UUID, который не может совпасть ни с одной реальной записью.
# Используется для заведомо некорректных идентификаторов — запрос вернёт пусто,
# и вызывающий код отдаст 404 вместо ошибки драйвера.
_INVALID_ID = uuid.UUID(int=0)


def to_uuid(value: Optional[Any]) -> Optional[uuid.UUID]:
    """
    Привести значение к UUID.

    Args:
        value: UUID, строка с UUID или None

    Returns:
        uuid.UUID для корректного значения, None если значение пустое,
        заведомо несуществующий UUID для некорректной строки.
    """
    if value is None:
        return None
    if isinstance(value, uuid.UUID):
        return value
    try:
        return uuid.UUID(str(value))
    except (ValueError, AttributeError, TypeError):
        return _INVALID_ID


__all__ = ["to_uuid"]
