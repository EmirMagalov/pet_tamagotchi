# app/routers/pet.py
import time


async def sleep_calculate(pet):
    if  pet.is_sleeping:
        # ПЕРЕД ТЕМ как уснуть, считаем время до 100% энергии
        energy_to_restore = 100 - pet.energy
        # Например, 0.5 энергии в минуту -> 120 секунд на 1%
        seconds_needed = int((energy_to_restore / 2) * 60)

        pet.wake_up_at = int(time.time() + seconds_needed)

    else:
        # Если проснулся раньше — обнуляем
        pet.wake_up_at = 0


    await pet.save()
    return pet
