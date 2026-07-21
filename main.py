"""
Корневая точка входа приложения Yartumba.
Реальное FastAPI-приложение определено в app/main.py.
Использование: uvicorn main:app --reload
"""
from app.main import app  # noqa: F401

__all__ = ["app"]
