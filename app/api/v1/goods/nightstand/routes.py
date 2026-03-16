"""
API роуты для прикроватных тумб
"""
from uuid import UUID
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.models.goods import Nightstand, NightstandPart
from app.api.v1.goods.dependencies import get_db
from app.api.v1.goods.nightstand.schemas import (
    NightstandCreate,
    NightstandUpdate,
    NightstandResponse,
    NightstandPartCreate,
    NightstandPartUpdate,
    NightstandPartResponse,
    NightstandWithParts,
)

router = APIRouter(prefix="/nightstand", tags=["nightstand"])


# === Роуты для Nightstand ===

@router.post("/", response_model=NightstandResponse, status_code=status.HTTP_201_CREATED)
def create_nightstand(
    data: NightstandCreate,
    db: Session = Depends(get_db)
):
    """Создать новую прикроватную тумбу"""
    nightstand = Nightstand(
        width=data.width,
        height=data.height,
        depth=data.depth,
        drawer_count=data.drawer_count,
        has_open_shelf=data.has_open_shelf,
        leg_type=data.leg_type,
        product_id=data.product_id,
    )
    db.add(nightstand)
    db.commit()
    db.refresh(nightstand)
    return nightstand


@router.get("/", response_model=List[NightstandResponse])
def list_nightstands(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """Получить список всех прикроватных тумб"""
    return db.query(Nightstand).offset(skip).limit(limit).all()


@router.get("/{nightstand_id}", response_model=NightstandResponse)
def get_nightstand(
    nightstand_id: UUID,
    db: Session = Depends(get_db)
):
    """Получить прикроватную тумбу по ID"""
    nightstand = db.query(Nightstand).filter(Nightstand.id == nightstand_id).first()
    if not nightstand:
        raise HTTPException(status_code=404, detail="Прикроватная тумба не найдена")
    return nightstand


@router.get("/{nightstand_id}/full", response_model=NightstandWithParts)
def get_nightstand_with_parts(
    nightstand_id: UUID,
    db: Session = Depends(get_db)
):
    """Получить прикроватную тумбу с деталями"""
    nightstand = db.query(Nightstand).filter(Nightstand.id == nightstand_id).first()
    if not nightstand:
        raise HTTPException(status_code=404, detail="Прикроватная тумба не найдена")
    return nightstand


@router.patch("/{nightstand_id}", response_model=NightstandResponse)
def update_nightstand(
    nightstand_id: UUID,
    data: NightstandUpdate,
    db: Session = Depends(get_db)
):
    """Обновить прикроватную тумбу"""
    nightstand = db.query(Nightstand).filter(Nightstand.id == nightstand_id).first()
    if not nightstand:
        raise HTTPException(status_code=404, detail="Прикроватная тумба не найдена")

    update_data = data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(nightstand, field, value)

    db.commit()
    db.refresh(nightstand)
    return nightstand


@router.delete("/{nightstand_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_nightstand(
    nightstand_id: UUID,
    db: Session = Depends(get_db)
):
    """Удалить прикроватную тумбу"""
    nightstand = db.query(Nightstand).filter(Nightstand.id == nightstand_id).first()
    if not nightstand:
        raise HTTPException(status_code=404, detail="Прикроватная тумба не найдена")

    db.delete(nightstand)
    db.commit()
    return None


# === Роуты для деталей NightstandPart ===

@router.post("/{nightstand_id}/parts", response_model=NightstandPartResponse, status_code=status.HTTP_201_CREATED)
def create_nightstand_part(
    nightstand_id: UUID,
    data: NightstandPartCreate,
    db: Session = Depends(get_db)
):
    """Добавить деталь к прикроватной тумбе"""
    nightstand = db.query(Nightstand).filter(Nightstand.id == nightstand_id).first()
    if not nightstand:
        raise HTTPException(status_code=404, detail="Прикроватная тумба не найдена")

    part = NightstandPart(
        nightstand_id=nightstand_id,
        name=data.name,
        part_width=data.part_width,
        part_height=data.part_height,
        part_depth=data.part_depth,
        quantity=data.quantity,
        sheet_material_id=data.sheet_material_id,
    )
    db.add(part)
    db.commit()
    db.refresh(part)
    return part


@router.get("/{nightstand_id}/parts", response_model=List[NightstandPartResponse])
def list_nightstand_parts(
    nightstand_id: UUID,
    db: Session = Depends(get_db)
):
    """Получить все детали прикроватной тумбы"""
    nightstand = db.query(Nightstand).filter(Nightstand.id == nightstand_id).first()
    if not nightstand:
        raise HTTPException(status_code=404, detail="Прикроватная тумба не найдена")
    return nightstand.parts


@router.get("/{nightstand_id}/parts/{part_id}", response_model=NightstandPartResponse)
def get_nightstand_part(
    nightstand_id: UUID,
    part_id: UUID,
    db: Session = Depends(get_db)
):
    """Получить деталь по ID"""
    part = db.query(NightstandPart).filter(
        NightstandPart.id == part_id,
        NightstandPart.nightstand_id == nightstand_id
    ).first()
    if not part:
        raise HTTPException(status_code=404, detail="Деталь не найдена")
    return part


@router.patch("/{nightstand_id}/parts/{part_id}", response_model=NightstandPartResponse)
def update_nightstand_part(
    nightstand_id: UUID,
    part_id: UUID,
    data: NightstandPartUpdate,
    db: Session = Depends(get_db)
):
    """Обновить деталь"""
    part = db.query(NightstandPart).filter(
        NightstandPart.id == part_id,
        NightstandPart.nightstand_id == nightstand_id
    ).first()
    if not part:
        raise HTTPException(status_code=404, detail="Деталь не найдена")

    update_data = data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(part, field, value)

    db.commit()
    db.refresh(part)
    return part


@router.delete("/{nightstand_id}/parts/{part_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_nightstand_part(
    nightstand_id: UUID,
    part_id: UUID,
    db: Session = Depends(get_db)
):
    """Удалить деталь"""
    part = db.query(NightstandPart).filter(
        NightstandPart.id == part_id,
        NightstandPart.nightstand_id == nightstand_id
    ).first()
    if not part:
        raise HTTPException(status_code=404, detail="Деталь не найдена")

    db.delete(part)
    db.commit()
    return None

