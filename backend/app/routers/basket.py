import asyncio
import math
from datetime import datetime, timezone
from typing import List

import aioredis
from fastapi import APIRouter, HTTPException
from schemas.pet import Pet, PetCreate, PetUpdate, PetSleepResponse
from models.pet import Pet
from models.basket import Basket
from tortoise.exceptions import DoesNotExist
from core.constants import ITEMS
from fastapi import WebSocket

from schemas.basket import BasketRead,BasketCreate

basket_router = APIRouter(prefix="/buy", tags=["buy"])




@basket_router.post("/{tg_id}/{item_id}",response_model=BasketCreate)
async def buy_item(tg_id: int, item_id: int):
    # 1. Проверяем, существует ли такой товар вообще
    item = ITEMS.get(item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Товар не найден")

    # 2. Получаем пета из БД
    pet = await Pet.get(telegram_id=tg_id)

    # 3. Проверяем деньги (Берем цену из нашего словаря, а не из запроса!)
    if pet.money < item["price"]:
        raise HTTPException(status_code=400, detail="Недостаточно денег")

    # 4. Проводим сделку
    pet.money -= item["price"]
    await pet.save()

    # 5. Добавляем в корзину/инвентарь
    basket = await Basket.create(pet=pet, item_id=item_id)

    return basket


@basket_router.get("/{tg_id}", response_model=List[BasketRead])
async def get_basket(tg_id: int):
    # 1. Ищем все предметы этого питомца в базе
    # Используем dunder-синтаксис (pet__telegram_id) для фильтрации по полю связанной модели
    items = await Basket.filter(pet__telegram_id=tg_id).all()

    # 2. Если корзина пуста, возвращаем пустой список (это нормально)
    if not items:
        return []

    # 3. Превращаем объекты БД в "обогащенные" Pydantic-схемы
    # Мы используем метод from_orm_enriched, который мы писали в схеме
    return [BasketRead.from_orm_enriched(item) for item in items]