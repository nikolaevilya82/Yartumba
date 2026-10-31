"""
Главное приложение FastAPI
"""
from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import text
from sqlalchemy.orm import Session

from app.api.v1.router import router as v1_router
from app.core.config import settings
from app.core.dependencies import get_db

app = FastAPI(
    title="Yartumba API",
    description="Мебельная конфигураторная система",
    version="1.0.0",
)

# CORS — читаем origins из конфига
# В DEV режиме: http://localhost:5173, http://localhost:3000
# В PROD режиме: задаётся через CORS_ORIGINS в .env
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Подключение роутеров
app.include_router(v1_router)


@app.get("/")
async def root():
    return {"message": "Yartumba API", "version": "1.0.0"}


@app.get("/health")
async def health(db: Session = Depends(get_db)):
    """
    Проверка работоспособности приложения и доступности БД.

    Возвращает 200, если БД отвечает на `SELECT 1`,
    иначе 503 с описанием проблемы.
    """
    try:
        db.execute(text("SELECT 1"))
    except Exception as exc:  # noqa: BLE001 — нужен любой сбой БД
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=f"Database is unavailable: {exc}",
        ) from exc

    return {"status": "ok", "database": "ok"}
