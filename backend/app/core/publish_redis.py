import json
import redis
import time
from schemas.pet import Pet
from functions.sleep_fn import sleep_calculate
r = redis.from_url("redis://localhost")


async def publish(pet: Pet):
    try:
        now = int(time.time())
        # 1. Базовые дельты
        hunger_change = -0.4
        energy_change = -0.2

        if pet.is_sleeping:
            hunger_change = -0.05
            energy_change = 2

        # 2. ПРИМЕНЯЕМ ИЗМЕНЕНИЯ СРАЗУ
        pet.hunger = round(max(0, min(100, pet.hunger + hunger_change)), 2)
        pet.energy = round(max(0, min(100, pet.energy + energy_change)), 2)

        # 3. ТЕПЕРЬ ПРОВЕРЯЕМ: не пора ли будить?
        if pet.is_sleeping and pet.wake_up_at > 0:
            if now >= pet.wake_up_at:
                pet.is_sleeping = False
                pet.energy = 100.0
                pet.wake_up_at = 0
                print(f"☀️ {pet.telegram_id} проснулся по времени")

        # 4. Считаем минуты (уже после изменения энергии)
        # Если шаг 2.0, то делим на 2
        await sleep_calculate(pet)


        # 5. Формируем сообщение (только целые числа для фронта)
        msg = {
            "tg_id": pet.telegram_id,
            "money": int(pet.money),
            "energy":pet.energy,
            "hunger":pet.hunger,
            "wake_up_at": pet.wake_up_at,       # Или готовое время "До скольки"
            "is_sleeping": pet.is_sleeping
        }


        r.publish("game_updates", json.dumps(msg))

    except Exception as e:
        print(f"❌ Ошибка в задаче: {e}")