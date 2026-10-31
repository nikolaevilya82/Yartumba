"""
Реестр типов мебели.

Единая точка сопоставления строкового типа мебели и SQLAlchemy-модели.
Используется везде, где нужно получить объект мебели по `furniture_type`
(корзина, сервисы), чтобы не дублировать цепочки if/elif.
"""
from typing import Dict, Optional, Type

from sqlalchemy.orm import Session

from app.core.db_setup import Base
from app.core.identifiers import to_uuid
from app.models.goods import Bookshelf, Dresser, Nightstand

# Тип мебели -> модель
FURNITURE_MODELS: Dict[str, Type[Base]] = {
    "bookshelf": Bookshelf,
    "nightstand": Nightstand,
    "dresser": Dresser,
}


def get_furniture_model(furniture_type: str) -> Optional[Type[Base]]:
    """
    Вернуть модель мебели по её типу.

    Args:
        furniture_type: Тип мебели (bookshelf, nightstand, dresser)

    Returns:
        Класс модели или None, если тип неизвестен
    """
    return FURNITURE_MODELS.get(furniture_type)


def get_furniture(db: Session, furniture_type: str, furniture_id):
    """
    Получить объект мебели по типу и ID.

    Args:
        db: Сессия БД
        furniture_type: Тип мебели (bookshelf, nightstand, dresser)
        furniture_id: ID мебели

    Returns:
        Bookshelf | Nightstand | Dresser | None
    """
    model = get_furniture_model(furniture_type)
    if model is None:
        return None
    return db.query(model).filter(model.id == to_uuid(furniture_id)).first()


__all__ = [
    "FURNITURE_MODELS",
    "get_furniture_model",
    "get_furniture",
]
