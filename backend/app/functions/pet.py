from datetime import datetime, timezone
from schemas.pet import Pet


async def get_live_stats(pet: Pet, now: datetime = None):
    # Если время не передано, берем текущее UTC
    if now is None:
        now = datetime.now(timezone.utc)

    # Разница во времени (теперь это объект timedelta)
    delta_td = now - pet.last_updated
    # Переводим в секунды (float)
    delta = max(0, delta_td.total_seconds())

    # КОНСТАНТЫ
    HUNGER_RATE = 100 / (4 * 3600)  # 4 часа до 0
    ENERGY_DECAY = 100 / (5 * 3600)  # 5 часов до 0
    ENERGY_RECOVERY = 2 / 60  # 2 ед в минуту
    DIRT_RATE = 100 / (6 * 3600)
    current_hunger = pet.hunger
    current_energy = pet.energy

    current_dirt = pet.dirt + (delta * DIRT_RATE)

    if pet.is_sleeping:
        # Проверка на авто-просыпание
        now_ts = int(now.timestamp())
        if pet.wake_up_at > 0 and now_ts >= pet.wake_up_at:
            # Логика просыпания (как у тебя была)
            sleep_duration = pet.wake_up_at - int(pet.last_updated.timestamp())
            awake_after_sleep = now_ts - pet.wake_up_at

            current_energy = min(100.0, current_energy + (sleep_duration * ENERGY_RECOVERY))
            current_energy = max(0.0, current_energy - (awake_after_sleep * ENERGY_DECAY))
            current_hunger -= (sleep_duration * (HUNGER_RATE / 8)) + (awake_after_sleep * HUNGER_RATE)
            is_sleeping = False
        else:
            current_energy = min(100.0, current_energy + (delta * ENERGY_RECOVERY))
            current_hunger -= (delta * (HUNGER_RATE / 8))
            is_sleeping = True
    else:
        current_energy = max(0.0, current_energy - (delta * ENERGY_DECAY))
        current_hunger -= (delta * HUNGER_RATE)
        is_sleeping = False

    return {
        "hunger": round(max(0, current_hunger), 2),
        "energy": round(max(0, current_energy), 2),
        "is_sleeping": is_sleeping,
        "dirt": round(min(100, current_dirt), 2),
        # Возвращаем время в ISO строке для фронтенда
        "last_updated": now.isoformat().replace("+00:00", "Z")
    }