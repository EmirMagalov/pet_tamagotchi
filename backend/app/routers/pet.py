import asyncio
import math
from datetime import datetime, timezone
import aioredis
from fastapi import APIRouter, HTTPException
from schemas.pet import Pet, PetCreate, PetUpdate, PetSleepResponse
from models.pet import Pet as PetModel
from models.basket import Basket
from tortoise.exceptions import DoesNotExist
from core.redis_manager import manager
from core.constants import ITEMS
from fastapi import WebSocket
from core.publish_redis import publish
from functions.sleep_fn import sleep_calculate
from functions.pet import get_live_stats

pet_router = APIRouter(prefix="/pet", tags=["pet"])


@pet_router.get("/{tg_id}", response_model=Pet)
async def get_pet(tg_id: int):
    try:
        # Используем .get() для поиска в базе
        pet = await PetModel.get(telegram_id=tg_id)
        stats = await get_live_stats(pet)

        result = {**pet.__dict__, **stats}
        return result
    except DoesNotExist:
        raise HTTPException(status_code=404, detail="Питомец не найден")


@pet_router.post("/", response_model=Pet)
async def create_pet(pet_data: PetCreate):
    # Проверяем, нет ли уже такого пета
    existing = await PetModel.filter(telegram_id=pet_data.telegram_id).first()
    if existing:
        raise HTTPException(status_code=400, detail="Питомец уже существует")

    # Создаем запись в базе через модель
    new_pet = await PetModel.create(**pet_data.model_dump())
    return new_pet


@pet_router.post("/food/{tg_id}/{value}/{basket_id}", response_model=Pet)
async def update_pet(tg_id: int,basket_id:int,value:int = 10):
    # 1. Получаем пета из базы (там старые данные-снимки)

    basket_entry = await Basket.get_or_none(id=basket_id).prefetch_related("pet")
    # 2. Рассчитываем актуальное состояние на текущую секунду
    if not basket_entry:
        raise HTTPException(status_code=404, detail="Предмет не найден")

        # 2. Получаем статы из констант (сколько дает сытости)
    pet = await PetModel.get(telegram_id=tg_id)

    stats = await get_live_stats(pet)

    # 3. Синхронизируем модель с реальностью
    # Теперь pet.hunger — это то, сколько у него реально сейчас, а не 5 часов назад
    pet.hunger = stats["hunger"]
    pet.energy = stats["energy"]
    pet.dirt = stats["dirt"]
    pet.is_sleeping = stats["is_sleeping"]
    pet.dirt = min(100.0, pet.dirt + 25.0)
    # 4. Проверяем условие (теперь проверка честная)
    # if pet.hunger >= 100:
    #     raise HTTPException(status_code=409, detail="Pet is not hungry")

    # 5. Применяем действие (кормление)
    pet.hunger = min(100.0, pet.hunger + value)

    # 6. Создаем НОВУЮ точку отсчета
    # С этого момента время пойдет заново для новых 110% (или 100%)
    pet.last_updated = datetime.now(timezone.utc)

    # 7. Сохраняем новый "снимок" в базу
    await pet.save()
    await basket_entry.delete()
    return pet


@pet_router.post("/sleep/{tg_id}", response_model=Pet)
async def toggle_sleep(tg_id: int):
    pet = await PetModel.get(telegram_id=tg_id)
    now = datetime.now(timezone.utc)  # ОДНА точка времени
    stats = await get_live_stats(pet, now=now)
    now_ts = int(now.timestamp())


    pet.hunger = stats["hunger"]
    pet.energy = stats["energy"]
    pet.dirt = stats["dirt"]
    if pet.is_sleeping:
        # Пробуждение вручную
        pet.is_sleeping = False
        pet.wake_up_at = 0
    else:
        # Засыпание
        # if pet.hunger < 35:
        #     raise HTTPException(status_code=409, detail="hunger")
        # if pet.energy > 95:  # Если почти полный, спать нельзя
        #     raise HTTPException(status_code=409, detail="energy")

        pet.is_sleeping = True

        # РАСЧЕТ ВРЕМЕНИ ДО ПОЛНОГО ЗАРЯДА
        # 2 единицы в минуту = 1 единица за 30 секунд
        seconds_needed = int((100 - pet.energy) * 30)
        pet.wake_up_at = now_ts + seconds_needed

        print(f"💤 {tg_id} уснул на {seconds_needed // 60} мин. Проснется в {pet.wake_up_at}")

    # 3. Сохраняем точку отсчета
    pet.last_updated = now

    await pet.save()

    return pet


@pet_router.post("/bathe/{tg_id}", response_model=Pet)
async def bathe(tg_id: int):
    pet = await PetModel.get(telegram_id=tg_id)
    now = datetime.now(timezone.utc)  # ОДНА точка времени
    stats = await get_live_stats(pet, now=now)
    now_ts = int(now.timestamp())


    pet.hunger = stats["hunger"]
    pet.energy = stats["energy"]


    pet.dirt = 0

    # 3. Сохраняем точку отсчета
    pet.last_updated = now

    await pet.save()

    return pet




# @router.websocket("/ws/{tg_id}")
# async def websocket_endpoint(websocket: WebSocket, tg_id: int):
#     print(f"🔌 Новый WebSocket от tg_id={tg_id}")
#     await manager.connect(websocket, tg_id)
#     print(f"✅ Подключён, всего соединений: {len(manager.active_connections)}")
#
#     try:
#         while True:
#             await websocket.receive_text()  # можно заменить на receive_json() если клиент шлёт данные
#     except Exception as e:
#         print(f"❌ WebSocket отключился (tg_id={tg_id}): {type(e).__name__}")
#     finally:
#         manager.disconnect(tg_id)
#         print(f"🔌 Отключён tg_id={tg_id}")
