"""
API роуты для книжных полок
"""
from uuid import UUID
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.models.goods import Bookshelf, BookshelfPart
from app.api.v1.goods.dependencies import get_db
from app.api.v1.goods.bookshelf.schemas import (
    BookshelfCreate,
    BookshelfUpdate,
    BookshelfResponse,
    BookshelfPartCreate,
    BookshelfPartUpdate,
    BookshelfPartResponse,
    BookshelfWithParts,
)

router = APIRouter(prefix="/bookshelf", tags=["bookshelf"])


# === Роуты для Bookshelf ===

@router.post("/", response_model=BookshelfResponse, status_code=status.HTTP_201_CREATED)
def create_bookshelf(
    data: BookshelfCreate,
    db: Session = Depends(get_db)
):
    """Создать новую книжную полку"""
    bookshelf = Bookshelf(
        width=data.width,
        height=data.height,
        depth=data.depth,
        shelf_count=data.shelf_count,
        shelf_type=data.shelf_type,
        product_id=data.product_id,
    )
    db.add(bookshelf)
    db.commit()
    db.refresh(bookshelf)
    return bookshelf


@router.get("/", response_model=List[BookshelfResponse])
def list_bookshelves(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """Получить список всех книжных полок"""
    return db.query(Bookshelf).offset(skip).limit(limit).all()


@router.get("/{bookshelf_id}", response_model=BookshelfResponse)
def get_bookshelf(
    bookshelf_id: UUID,
    db: Session = Depends(get_db)
):
    """Получить книжную полку по ID"""
    bookshelf = db.query(Bookshelf).filter(Bookshelf.id == bookshelf_id).first()
    if not bookshelf:
        raise HTTPException(status_code=404, detail="Книжная полка не найдена")
    return bookshelf


@router.get("/{bookshelf_id}/full", response_model=BookshelfWithParts)
def get_bookshelf_with_parts(
    bookshelf_id: UUID,
    db: Session = Depends(get_db)
):
    """Получить книжную полку с деталями"""
    bookshelf = db.query(Bookshelf).filter(Bookshelf.id == bookshelf_id).first()
    if not bookshelf:
        raise HTTPException(status_code=404, detail="Книжная полка не найдена")
    return bookshelf


@router.patch("/{bookshelf_id}", response_model=BookshelfResponse)
def update_bookshelf(
    bookshelf_id: UUID,
    data: BookshelfUpdate,
    db: Session = Depends(get_db)
):
    """Обновить книжную полку"""
    bookshelf = db.query(Bookshelf).filter(Bookshelf.id == bookshelf_id).first()
    if not bookshelf:
        raise HTTPException(status_code=404, detail="Книжная полка не найдена")

    # Обновляем только переданные поля
    update_data = data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(bookshelf, field, value)

    db.commit()
    db.refresh(bookshelf)
    return bookshelf


@router.delete("/{bookshelf_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_bookshelf(
    bookshelf_id: UUID,
    db: Session = Depends(get_db)
):
    """Удалить книжную полку"""
    bookshelf = db.query(Bookshelf).filter(Bookshelf.id == bookshelf_id).first()
    if not bookshelf:
        raise HTTPException(status_code=404, detail="Книжная полка не найдена")

    db.delete(bookshelf)
    db.commit()
    return None


# === Роуты для деталей BookshelfPart ===

@router.post("/{bookshelf_id}/parts", response_model=BookshelfPartResponse, status_code=status.HTTP_201_CREATED)
def create_bookshelf_part(
    bookshelf_id: UUID,
    data: BookshelfPartCreate,
    db: Session = Depends(get_db)
):
    """Добавить деталь к книжной полке"""
    # Проверяем, что полка существует
    bookshelf = db.query(Bookshelf).filter(Bookshelf.id == bookshelf_id).first()
    if not bookshelf:
        raise HTTPException(status_code=404, detail="Книжная полка не найдена")

    part = BookshelfPart(
        bookshelf_id=bookshelf_id,
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


@router.get("/{bookshelf_id}/parts", response_model=List[BookshelfPartResponse])
def list_bookshelf_parts(
    bookshelf_id: UUID,
    db: Session = Depends(get_db)
):
    """Получить все детали книжной полки"""
    bookshelf = db.query(Bookshelf).filter(Bookshelf.id == bookshelf_id).first()
    if not bookshelf:
        raise HTTPException(status_code=404, detail="Книжная полка не найдена")
    return bookshelf.parts


@router.get("/{bookshelf_id}/parts/{part_id}", response_model=BookshelfPartResponse)
def get_bookshelf_part(
    bookshelf_id: UUID,
    part_id: UUID,
    db: Session = Depends(get_db)
):
    """Получить деталь по ID"""
    part = db.query(BookshelfPart).filter(
        BookshelfPart.id == part_id,
        BookshelfPart.bookshelf_id == bookshelf_id
    ).first()
    if not part:
        raise HTTPException(status_code=404, detail="Деталь не найдена")
    return part


@router.patch("/{bookshelf_id}/parts/{part_id}", response_model=BookshelfPartResponse)
def update_bookshelf_part(
    bookshelf_id: UUID,
    part_id: UUID,
    data: BookshelfPartUpdate,
    db: Session = Depends(get_db)
):
    """Обновить деталь"""
    part = db.query(BookshelfPart).filter(
        BookshelfPart.id == part_id,
        BookshelfPart.bookshelf_id == bookshelf_id
    ).first()
    if not part:
        raise HTTPException(status_code=404, detail="Деталь не найдена")

    update_data = data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(part, field, value)

    db.commit()
    db.refresh(part)
    return part


@router.delete("/{bookshelf_id}/parts/{part_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_bookshelf_part(
    bookshelf_id: UUID,
    part_id: UUID,
    db: Session = Depends(get_db)
):
    """Удалить деталь"""
    part = db.query(BookshelfPart).filter(
        BookshelfPart.id == part_id,
        BookshelfPart.bookshelf_id == bookshelf_id
    ).first()
    if not part:
        raise HTTPException(status_code=404, detail="Деталь не найдена")

    db.delete(part)
    db.commit()
    return None

