from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class ItemBase(BaseModel):
    """Базовая модель для элемента"""
    name: str = Field(..., min_length=1, max_length=100, description="Название элемента")
    description: Optional[str] = Field(None, max_length=500, description="Описание элемента")
    price: Optional[float] = Field(None, ge=0, description="Цена элемента")
    quantity: Optional[int] = Field(0, ge=0, description="Количество")

class ItemCreate(ItemBase):
    """Модель для создания нового элемента"""
    pass

class ItemUpdate(BaseModel):
    """Модель для обновления элемента"""
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    description: Optional[str] = Field(None, max_length=500)
    price: Optional[float] = Field(None, ge=0)
    quantity: Optional[int] = Field(None, ge=0)

class Item(ItemBase):
    """Модель для отображения элемента"""
    id: int
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True

class HealthResponse(BaseModel):
    """Модель для ответа проверки здоровья"""
    status: str
    service: str
    timestamp: str

class ErrorResponse(BaseModel):
    """Модель для ошибок"""
    detail: str