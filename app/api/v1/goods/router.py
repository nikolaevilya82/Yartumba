"""
Объединение всех роутов товаров
"""
from fastapi import APIRouter
from app.api.v1.goods.bookshelf.routes import router as bookshelf_router
from app.api.v1.goods.nightstand.routes import router as nightstand_router
from app.api.v1.goods.dresser.routes import router as dresser_router

router = APIRouter(prefix="/goods", tags=["goods"])

# Подключение роутов
router.include_router(bookshelf_router)
router.include_router(nightstand_router)
router.include_router(dresser_router)

