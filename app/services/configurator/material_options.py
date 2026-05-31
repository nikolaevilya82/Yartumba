"""
Получение списка доступных материалов и фурнитуры
"""
from typing import Dict, List, Any

from sqlalchemy.orm import Session

from app.models.materials import (
    SheetMaterial,
    EdgeMaterial,
    SlideGuide,
    Hinge,
    Support,
    WallMount,
)
from app.services.image_service import (
    get_sheet_material_image_url,
    get_edge_material_image_url,
    get_slide_guide_image_url,
    get_hinge_image_url,
    get_support_image_url,
    get_wall_mount_image_url,
)


def get_material_options(db: Session) -> Dict[str, List[Dict[str, Any]]]:
    """
    Получить все доступные материалы и фурнитуру
    
    Args:
        db: Сессия базы данных
        
    Returns:
        Словарь с категориями материалов
    """
    options = {
        "sheet_materials": _get_sheet_materials(db),
        "edge_materials": _get_edge_materials(db),
        "slide_guides": _get_slide_guides(db),
        "hinges": _get_hinges(db),
        "supports": _get_supports(db),
        "wall_mounts": _get_wall_mounts(db),
    }
    
    return options


def _get_sheet_materials(db: Session) -> List[Dict[str, Any]]:
    """Получить листовые материалы"""
    materials = []
    
    for material in db.query(SheetMaterial).filter_by(is_active="active").all():
        materials.append({
            "id": str(material.id),
            "name": material.name,
            "material_type": material.material_type,
            "thickness": material.thickness,
            "standard_width": material.standard_width,
            "standard_height": material.standard_height,
            "decor_name": material.decor_name,
            "hex_code": material.hex_code,
            "price": material.price,
            "image_url": get_sheet_material_image_url(
                material.id, material.image_url
            ),
            "texture_url": material.texture_url,
        })
    
    return materials


def _get_edge_materials(db: Session) -> List[Dict[str, Any]]:
    """Получить кромку"""
    materials = []
    
    for edge in db.query(EdgeMaterial).all():
        materials.append({
            "id": str(edge.id),
            "sheet_material_id": str(edge.sheet_material_id),
            "edge_type": edge.edge_type,
            "thickness": edge.thickness,
            "width": edge.width,
            "decor_name": edge.decor_name,
            "price_per_meter": edge.price_per_meter,
            "image_url": get_edge_material_image_url(
                edge.id, edge.image_url
            ),
        })
    
    return materials


def _get_slide_guides(db: Session) -> List[Dict[str, Any]]:
    """Получить направляющие"""
    guides = []
    
    for guide in db.query(SlideGuide).all():
        guides.append({
            "id": str(guide.id),
            "name": guide.name,
            "guide_type": guide.guide_type,
            "extension_type": guide.extension_type,
            "length": guide.length,
            "load_capacity": guide.load_capacity,
            "has_soft_close": guide.has_soft_close,
            "price": guide.price,
            "image_url": get_slide_guide_image_url(
                guide.id, guide.image_url
            ),
        })
    
    return guides


def _get_hinges(db: Session) -> List[Dict[str, Any]]:
    """Получить петли"""
    hinges = []
    
    for hinge in db.query(Hinge).all():
        hinges.append({
            "id": str(hinge.id),
            "name": hinge.name,
            "hinge_type": hinge.hinge_type,
            "mounting_type": hinge.mounting_type,
            "opening_angle": hinge.opening_angle,
            "has_soft_close": hinge.has_soft_close,
            "price": hinge.price,
            "image_url": get_hinge_image_url(
                hinge.id, hinge.image_url
            ),
        })
    
    return hinges


def _get_supports(db: Session) -> List[Dict[str, Any]]:
    """Получить опоры/ножки"""
    supports = []
    
    for support in db.query(Support).all():
        supports.append({
            "id": str(support.id),
            "name": support.name,
            "support_type": support.support_type,
            "material": support.material,
            "height": support.height,
            "diameter": support.diameter,
            "is_adjustable": support.is_adjustable,
            "price": support.price,
            "image_url": get_support_image_url(
                support.id, support.image_url
            ),
        })
    
    return supports


def _get_wall_mounts(db: Session) -> List[Dict[str, Any]]:
    """Получить настенные крепления"""
    mounts = []
    
    for mount in db.query(WallMount).all():
        mounts.append({
            "id": str(mount.id),
            "name": mount.name,
            "mount_type": mount.mount_type,
            "wall_type": mount.wall_type,
            "max_load": mount.max_load,
            "adjustment": mount.adjustment,
            "is_hidden": mount.is_hidden,
            "price": mount.price,
            "image_url": get_wall_mount_image_url(
                mount.id, mount.image_url
            ),
        })
    
    return mounts
