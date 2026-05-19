"""
API роуты для конфигуратора
"""
from typing import Dict, Any
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, Field

from app.core.db_setup import SessionLocal
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
async def get_configurator_options():
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
    db = SessionLocal()
    try:
        service = create_configurator_service(db)
        return service.get_material_options()
    finally:
        db.close()


@router.post("/validate")
async def validate_configuration(data: ConfigurationValidate):
    """
    Валидация конфигурации
    
    Проверяет:
    - Корректность размеров
    - Допустимое количество ящиков/полок
    - Наличие обязательных материалов
    """
    furniture_type = data.furniture_type
    config = data.configuration
    
    db = SessionLocal()
    try:
        service = create_configurator_service(db)
        
        if furniture_type == "nightstand":
            result = service.validate("nightstand", config)
        elif furniture_type == "bookshelf":
            result = service.validate("bookshelf", config)
        elif furniture_type == "dresser":
            result = service.validate("dresser", config)
        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Неизвестный тип мебели: {furniture_type}"
            )
        
        return result
    finally:
        db.close()


@router.post("/calculate")
async def calculate_configuration(data: ConfigurationCalculate):
    """
    Расчёт стоимости конфигурации
    
    Возвращает:
    - materials_cost: Стоимость материалов
    - hardware_cost: Стоимость фурнитуры
    - work_cost: Стоимость работы
    - total_price: Итоговая цена
    - details: Детализация расчёта
    """
    furniture_type = data.furniture_type
    config = data.configuration
    
    db = SessionLocal()
    try:
        service = create_configurator_service(db)
        
        if furniture_type == "nightstand":
            result = service.calculate("nightstand", config)
        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Расчёт для типа '{furniture_type}' ещё не реализован"
            )
        
        return result
    finally:
        db.close()