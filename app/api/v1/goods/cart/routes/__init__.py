"""
Эндпоинты корзины
SRP: Разделение по HTTP методам
"""
from fastapi import APIRouter

from app.api.v1.goods.cart.routes.get import router as get_router
from app.api.v1.goods.cart.routes.post import router as post_router
from app.api.v1.goods.cart.routes.patch import router as patch_router
from app.api.v1.goods.cart.routes.delete import router as delete_router
from app.api.v1.goods.cart.routes.merge import router as merge_router

router = APIRouter(prefix="/cart", tags=["Cart"])

# Объединение всех роутеров
router.include_router(get_router)
router.include_router(post_router)
router.include_router(patch_router)
router.include_router(delete_router)
router.include_router(merge_router)
