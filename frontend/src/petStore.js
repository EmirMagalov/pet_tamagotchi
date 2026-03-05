import {ref, computed, onMounted, onUnmounted, watch} from 'vue';

export function usePetLiveStats(petData) {
    const now = ref(Date.now());
    let timer = null;

    const HUNGER_RATE = 100 / (4 * 3600);
    const ENERGY_DECAY = 100 / (5 * 3600);
    const ENERGY_RECOVERY = 2 / 60;
    const DIRT_RATE = 100 / (6 * 3600);


    const liveDirt = computed(() => {
        if (!petData?.value?.last_updated) return 0;

        const lastUpdateTs = new Date(petData.value.last_updated).getTime();
        const delta = Math.max(0, (Date.now() - lastUpdateTs) / 1000);

        // К базовому значению грязи прибавляем то, что накопилось
        const res = Number(petData.value.dirt) + (delta * DIRT_RATE);

        return Number(Math.min(100, res).toFixed(2));
    });

    // "Будильник" - срабатывает только когда время РЕАЛЬНО вышло
    watch(now, (currentTime) => {
        if (petData.value?.is_sleeping && petData.value?.wake_up_at > 0) {
            const nowInSeconds = Math.floor(currentTime / 1000);
            if (nowInSeconds >= petData.value.wake_up_at) {
                petData.value.is_sleeping = false;
                petData.value.wake_up_at = 0;
                petData.value.energy = 100;
                petData.value.last_updated = new Date().toISOString();
            }
        }
    });

    const liveHunger = computed(() => {
        if (!petData?.value || !petData.value.last_updated) return 0;

        const lastUpdateStr = petData.value.last_updated;
        const dateSafe = lastUpdateStr.endsWith('Z') ? lastUpdateStr : lastUpdateStr + 'Z';

        // ВАЖНО: Math.max(0, ...) не дает дельте стать отрицательной
        // (защита от "прыжков" статов вверх при нажатии кнопок)
        const delta = Math.max(0, (now.value - new Date(dateSafe).getTime()) / 1000);
        const rate = petData.value.is_sleeping ? (HUNGER_RATE / 8) : HUNGER_RATE;

        const result = Number(petData.value.hunger) - (delta * rate);

        // НЕ используем Math.floor/Math.ceil для шкалы.
        // result будет 99.99, и CSS отрисует это как полную полоску.
        return Number(Math.min(100, Math.max(0, result)).toFixed(2));
    });

    const liveEnergy = computed(() => {
        if (!petData?.value || !petData.value.last_updated ) return 0;

        const lastUpdateStr = petData.value.last_updated;
        const dateSafe = lastUpdateStr.endsWith('Z') ? lastUpdateStr : lastUpdateStr + 'Z';

        const delta = Math.max(0, (now.value - new Date(dateSafe).getTime()) / 1000);

        let res = petData.value.is_sleeping
            ? Number(petData.value.energy) + (delta * ENERGY_RECOVERY)
            : Number(petData.value.energy) - (delta * ENERGY_DECAY);

        // Возвращаем число с 2 знаками после запятой для плавности полоски
        return Number(Math.min(100, Math.max(0, res)).toFixed(2));
    });

    onMounted(() => {
        timer = setInterval(() => { now.value = Date.now(); }, 1000);
    });

    onUnmounted(() => {
        if (timer) clearInterval(timer);
    });

    return { liveHunger, liveEnergy, liveDirt };
}