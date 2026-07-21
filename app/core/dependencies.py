"""
Общие зависимости для FastAPI.
Вынесены из app/api/v1/goods/dependencies.py для использования всеми модулями.
"""
from typing import Generator
from sqlalchemy.orm import Session
from app.core.db_setup import SessionLocal


def get_db() -> Generator[Session, None, None]:
    """
    Зависимость для получения сессии БД.
    Использовать в роутах: db: Session = Depends(get_db)
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()