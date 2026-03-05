from pydantic import BaseModel, Field, ConfigDict
from datetime import datetime
from typing import Optional

# 1. Общие поля для всех схем
class PetBase(BaseModel):
    name: Optional[str] = Field(None, max_length=50)
    hunger: float = Field(100.0, ge=0, le=100)
    energy: float = Field(100.0, ge=0, le=100)
    dirt: float = Field(0.0, ge=0, le=100)
    money: float = Field(100.0, ge=0)
    is_sleeping:bool = Field(False)
    wake_up_at: int = Field(0, ge=0)

# 2. Схема для создания (что мы ждем от фронтенда при старте игры)
class PetCreate(PetBase):
    telegram_id: int

# 3. Схема для обновления (когда хотим изменить только имя или статы)
class PetUpdate(BaseModel):
    name: Optional[str] = None
    hunger: Optional[float] = None
    energy: Optional[float] = None
    money: Optional[float] = None
    is_sleeping: Optional[bool] = None
    wake_up_at:Optional[int] = None


class PetSleepResponse(BaseModel):
    id: int
    telegram_id: int
    name: str | None
    hunger: float
    energy: float
    is_sleeping: bool
    # Наши расчетные поля

    wake_up_at: int

    # Чтобы Pydantic мог читать данные из Tortoise ORM объектов
    model_config = ConfigDict(from_attributes=True)
# 4. Полная схема для ответа (то, что летит во Vue 3)
class Pet(PetBase):
    id: int
    telegram_id: int
    last_updated: datetime
    wake_up_at: int = 0
    class Config:
        # В Pydantic v2 это теперь называется from_attributes = True
        # Это позволяет Pydantic читать данные прямо из объекта Tortoise
        model_config = ConfigDict(from_attributes=True)