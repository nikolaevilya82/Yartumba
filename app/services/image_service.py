"""
Сервис для работы с изображениями.

Генерация URL изображений на основе типа объекта и ID.
Поддерживает fallback-пути, если изображение не задано в БД.
"""

from typing import Optional
from uuid import UUID

from app.core.image_config import (
    SHEET_MATERIALS_PATH,
    EDGE_MATERIALS_PATH,
    SLIDE_GUIDES_PATH,
    HINGES_PATH,
    SUPPORTS_PATH,
    WALL_MOUNTS_PATH,
    FURNITURE_IMAGE_PATHS,
    UI_LOGOS_PATH,
    CONFIGURATOR_TEXTURES_PATH,
)


def _format_id(obj_id) -> str:
    """Привести ID к строке."""
    if isinstance(obj_id, UUID):
        return str(obj_id)
    return str(obj_id)


def get_sheet_material_image_url(
    material_id,
    stored_url: Optional[str] = None,
    extension: str = "jpg",
) -> Optional[str]:
    """
    URL изображения листового материала.

    Args:
        material_id: UUID материала
        stored_url: URL из поля image_url в БД (если задан)
        extension: расширение файла
    """
    if stored_url:
        return stored_url
    return f"{SHEET_MATERIALS_PATH}/{_format_id(material_id)}.{extension}"


def get_edge_material_image_url(
    edge_id,
    stored_url: Optional[str] = None,
    extension: str = "jpg",
) -> Optional[str]:
    """URL изображения кромки."""
    if stored_url:
        return stored_url
    return f"{EDGE_MATERIALS_PATH}/{_format_id(edge_id)}.{extension}"


def get_slide_guide_image_url(
    guide_id,
    stored_url: Optional[str] = None,
    extension: str = "jpg",
) -> Optional[str]:
    """URL изображения направляющих."""
    if stored_url:
        return stored_url
    return f"{SLIDE_GUIDES_PATH}/{_format_id(guide_id)}.{extension}"


def get_hinge_image_url(
    hinge_id,
    stored_url: Optional[str] = None,
    extension: str = "jpg",
) -> Optional[str]:
    """URL изображения петель."""
    if stored_url:
        return stored_url
    return f"{HINGES_PATH}/{_format_id(hinge_id)}.{extension}"


def get_support_image_url(
    support_id,
    stored_url: Optional[str] = None,
    extension: str = "jpg",
) -> Optional[str]:
    """URL изображения опор/ножек."""
    if stored_url:
        return stored_url
    return f"{SUPPORTS_PATH}/{_format_id(support_id)}.{extension}"


def get_wall_mount_image_url(
    mount_id,
    stored_url: Optional[str] = None,
    extension: str = "jpg",
) -> Optional[str]:
    """URL изображения настенных креплений."""
    if stored_url:
        return stored_url
    return f"{WALL_MOUNTS_PATH}/{_format_id(mount_id)}.{extension}"


def get_furniture_image_url(
    furniture_type: str,
    furniture_id,
    stored_url: Optional[str] = None,
    extension: str = "jpg",
) -> Optional[str]:
    """
    URL изображения изделия (тумба, полка, комод).

    Args:
        furniture_type: bookshelf, nightstand, dresser
        furniture_id: UUID изделия
        stored_url: URL из поля image_url в БД
        extension: расширение файла
    """
    if stored_url:
        return stored_url
    base_path = FURNITURE_IMAGE_PATHS.get(furniture_type)
    if not base_path:
        return None
    return f"{base_path}/{_format_id(furniture_id)}.{extension}"


def get_texture_url(
    texture_name: str,
    stored_url: Optional[str] = None,
) -> Optional[str]:
    """
    URL текстуры для конфигуратора (3D-визуализация).

    Args:
        texture_name: имя файла текстуры без расширения
        stored_url: URL из поля texture_url в БД
    """
    if stored_url:
        return stored_url
    if not texture_name:
        return None
    return f"{CONFIGURATOR_TEXTURES_PATH}/{texture_name}.jpg"


def get_logo_url(logo_name: str = "logo", extension: str = "svg") -> str:
    """URL логотипа приложения."""
    return f"{UI_LOGOS_PATH}/{logo_name}.{extension}"
