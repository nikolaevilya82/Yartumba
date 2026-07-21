"""
API роуты для конфигуратора
"""
from typing import Dict, Any
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session

from app.core.dependencies import get_db
from app.services.configurator import create_configurator_service

router = APIRouter(prefix="/configurator", tags=["configurator"])


# === Схемы ===
class ConfigurationValidate(BaseModel):
    """Валидация конфигурации"""
    furniture_type: str = Field(..., description="Тип мебели: nightstand, bookshelf, dresser")
    configuration: Dict[str, Any] = Field(..., description="Конфигурация")


class ConfigurationCalculate(BaseModel):
    """Расчёт стоимости конфигурации"""
    furniture_type: str = Field(..., description="Тип мебели: nightstand, bookshelf, dresser")
    configuration: Dict[str, Any] = Field(..., description="Конфигурация")


class ConfigurationSave(BaseModel):
    """Сохранение конфигурации"""
    name: str = Field(..., description="Название конфигурации")
    furniture_type: str = Field(..., description="Тип мебели")
    configuration: Dict[str, Any] = Field(..., description="Конфигурация")
    total_price: int = Field(..., description="Итоговая цена в копейках")


# === Эндпоинты ===
@router.get("/options")
async def get_configurator_options(db: Session = Depends(get_db)):
    """
    Получить все доступные материалы и фурнитуру
    
    Возвращает:
    - sheet_materials: Листовые материалы (ДСП, МДФ, ЛДСП...)
    - edge_materials: Кромка
    - slide_guides: Направляющие для ящиков
    - hinges: Петли
    - supports: Опоры/ножки
    - wall_mounts: Крепления для подвесной мебели
    """
    service = create_configurator_service(db)
    return service.get_material_options()


@router.post("/validate")
async def validate_configuration(
    data: ConfigurationValidate,
    db: Session = Depends(get_db),
):
    """
    Валидация конфигурации
    
    Проверяет:
    - Корректность размеров
    - Допустимое количество ящиков/полок
    - Наличие обязательных материалов
    """
    service = create_configurator_service(db)
    try:
        return service.validate(data.furniture_type, data.configuration)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )


@router.post("/calculate")
async def calculate_configuration(
    data: ConfigurationCalculate,
    db: Session = Depends(get_db),
):
    """
    Расчёт стоимости конфигурации
    
    Материал рассчитывается по объёму изделия (габаритные размеры).
    BOM (спецификация деталей) формируется отдельно при оформлении заказа.

    Возвращает:
    - materials_cost: Стоимость материалов
    - hardware_cost: Стоимость фурнитуры
    - work_cost: Стоимость работы
    - total_price: Итоговая цена
    - details: Детализация расчёта (объём, количество фурнитуры)
    """
    service = create_configurator_service(db)
    try:
        return service.calculate(data.furniture_type, data.configuration)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )