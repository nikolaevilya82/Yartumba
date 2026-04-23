"""
Главный роутер API v1
"""
from fastapi import APIRouter
from app.api.v1.goods.router import router as goods_router
from app.api.v1.configurator import router as configurator_router

router = APIRouter(prefix="/v1")

# Подключение роутеров
router.include_router(goods_router)
router.include_router(configurator_router)
