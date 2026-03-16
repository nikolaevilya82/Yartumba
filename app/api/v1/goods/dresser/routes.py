"""
API роуты для комодов
"""
from uuid import UUID
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.models.goods import Dresser, DresserPart
from app.api.v1.goods.dependencies import get_db
from app.api.v1.goods.dresser.schemas import (
    DresserCreate,
    DresserUpdate,
    DresserResponse,
    DresserPartCreate,
    DresserPartUpdate,
    DresserPartResponse,
    DresserWithParts,
)

router = APIRouter(prefix="/dresser", tags=["dresser"])


# === Роуты для Dresser ===

@router.post("/", response_model=DresserResponse, status_code=status.HTTP_201_CREATED)
def create_dresser(
    data: DresserCreate,
    db: Session = Depends(get_db)
):
    """Создать новый комод"""
    dresser = Dresser(
        width=data.width,
        height=data.height,
        depth=data.depth,
        drawer_count=data.drawer_count,
        drawer_rows=data.drawer_rows,
        dresser_type=data.dresser_type,
        has_legs=data.has_legs,
        product_id=data.product_id,
    )
    db.add(dresser)
    db.commit()
    db.refresh(dresser)
    return dresser


@router.get("/", response_model=List[DresserResponse])
def list_dressers(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """Получить список всех комодов"""
    return db.query(Dresser).offset(skip).limit(limit).all()


@router.get("/{dresser_id}", response_model=DresserResponse)
def get_dresser(
    dresser_id: UUID,
    db: Session = Depends(get_db)
):
    """Получить комод по ID"""
    dresser = db.query(Dresser).filter(Dresser.id == dresser_id).first()
    if not dresser:
        raise HTTPException(status_code=404, detail="Комод не найден")
    return dresser


@router.get("/{dresser_id}/full", response_model=DresserWithParts)
def get_dresser_with_parts(
    dresser_id: UUID,
    db: Session = Depends(get_db)
):
    """Получить комод с деталями"""
    dresser = db.query(Dresser).filter(Dresser.id == dresser_id).first()
    if not dresser:
        raise HTTPException(status_code=404, detail="Комод не найден")
    return dresser


@router.patch("/{dresser_id}", response_model=DresserResponse)
def update_dresser(
    dresser_id: UUID,
    data: DresserUpdate,
    db: Session = Depends(get_db)
):
    """Обновить комод"""
    dresser = db.query(Dresser).filter(Dresser.id == dresser_id).first()
    if not dresser:
        raise HTTPException(status_code=404, detail="Комод не найден")

    update_data = data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(dresser, field, value)

    db.commit()
    db.refresh(dresser)
    return dresser


@router.delete("/{dresser_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_dresser(
    dresser_id: UUID,
    db: Session = Depends(get_db)
):
    """Удалить комод"""
    dresser = db.query(Dresser).filter(Dresser.id == dresser_id).first()
    if not dresser:
        raise HTTPException(status_code=404, detail="Комод не найден")

    db.delete(dresser)
    db.commit()
    return None


# === Роуты для деталей DresserPart ===

@router.post("/{dresser_id}/parts", response_model=DresserPartResponse, status_code=status.HTTP_201_CREATED)
def create_dresser_part(
    dresser_id: UUID,
    data: DresserPartCreate,
    db: Session = Depends(get_db)
):
    """Добавить деталь к комоду"""
    dresser = db.query(Dresser).filter(Dresser.id == dresser_id).first()
    if not dresser:
        raise HTTPException(status_code=404, detail="Комод не найден")

    part = DresserPart(
        dresser_id=dresser_id,
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


@router.get("/{dresser_id}/parts", response_model=List[DresserPartResponse])
def list_dresser_parts(
    dresser_id: UUID,
    db: Session = Depends(get_db)
):
    """Получить все детали комода"""
    dresser = db.query(Dresser).filter(Dresser.id == dresser_id).first()
    if not dresser:
        raise HTTPException(status_code=404, detail="Комод не найден")
    return dresser.parts


@router.get("/{dresser_id}/parts/{part_id}", response_model=DresserPartResponse)
def get_dresser_part(
    dresser_id: UUID,
    part_id: UUID,
    db: Session = Depends(get_db)
):
    """Получить деталь по ID"""
    part = db.query(DresserPart).filter(
        DresserPart.id == part_id,
        DresserPart.dresser_id == dresser_id
    ).first()
    if not part:
        raise HTTPException(status_code=404, detail="Деталь не найдена")
    return part


@router.patch("/{dresser_id}/parts/{part_id}", response_model=DresserPartResponse)
def update_dresser_part(
    dresser_id: UUID,
    part_id: UUID,
    data: DresserPartUpdate,
    db: Session = Depends(get_db)
):
    """Обновить деталь"""
    part = db.query(DresserPart).filter(
        DresserPart.id == part_id,
        DresserPart.dresser_id == dresser_id
    ).first()
    if not part:
        raise HTTPException(status_code=404, detail="Деталь не найдена")

    update_data = data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(part, field, value)

    db.commit()
    db.refresh(part)
    return part


@router.delete("/{dresser_id}/parts/{part_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_dresser_part(
    dresser_id: UUID,
    part_id: UUID,
    db: Session = Depends(get_db)
):
    """Удалить деталь"""
    part = db.query(DresserPart).filter(
        DresserPart.id == part_id,
        DresserPart.dresser_id == dresser_id
    ).first()
    if not part:
        raise HTTPException(status_code=404, detail="Деталь не найдена")

    db.delete(part)
    db.commit()
    return None

