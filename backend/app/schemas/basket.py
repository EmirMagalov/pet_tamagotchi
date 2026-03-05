from pydantic import BaseModel, Field, ConfigDict, field_validator
from typing import Optional
from core.constants import ITEMS  # Твой словарь с данными о еде


# 1. Базовая схема (общие поля)
class BasketBase(BaseModel):
    item_id: int = Field(..., description="ID предмета из constants.py")
    quantity: int = Field(default=1, ge=1, le=99, description="Количество предметов")


# 2. Схема для СОЗДАНИЯ (POST запрос от фронтенда)
class BasketCreate(BasketBase):
    id: int = Field(..., description="ID записи в таблице инвентаря")
    pet_id:int
    # Мы наследуем item_id и quantity.
    # Валидатор проверяет, существует ли такой товар в нашем словаре перед тем как лезть в БД
    @field_validator('item_id')
    @classmethod
    def validate_item_id(cls, v: int):
        if v not in ITEMS:
            raise ValueError(f"Предмет с ID {v} не найден в базе магазина")
        return v


# 3. Схема для ОБНОВЛЕНИЯ (например, изменить количество)
class BasketUpdate(BaseModel):
    quantity: int = Field(..., ge=0, le=99)


# 4. Схема для ЧТЕНИЯ (То, что летит на фронтенд в Vue)
class BasketRead(BasketBase):
    id: int = Field(..., description="ID записи в таблице инвентаря")

    # Добавляем "виртуальные" поля, которых нет в БД, но они есть в ITEMS
    name: str = ""
    image: str = ""
    value: float = 0.0
    price: float = 0.0

    # Настройка для работы с Tortoise ORM
    model_config = ConfigDict(from_attributes=True)

    @classmethod
    def from_orm_enriched(cls, obj):
        """
        Метод-помощник: берет объект из БД и "докидывает" в него инфу из констант
        """
        # Превращаем объект БД в словарь через Pydantic
        basket_data = cls.model_validate(obj).model_dump()

        # Ищем данные в словаре ITEMS по item_id
        item_info = ITEMS.get(basket_data['item_id'], {})

        # Склеиваем и возвращаем готовую схему
        return cls(**{**basket_data, **item_info})


