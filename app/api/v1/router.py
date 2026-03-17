"""
Главный роутер API v1
"""
from fastapi import APIRouter
from app.api.v1.goods.router import router as goods_router

router = APIRouter(prefix="/v1")

# Подключение роутеров
router.include_router(goods_router)
