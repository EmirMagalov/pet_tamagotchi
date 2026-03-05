<script setup>
import { ref, computed, onMounted, onUnmounted, watch } from 'vue';

const props = defineProps({
  // Принимаем Unix Timestamp (то самое число 1771247239)
  wakeUpAt: { type: Number, required: true },
  // Нам все еще нужно знать общую длительность для анимации круга (в секундах)
  totalDuration: { type: Number, default: 240 }
});

const timeLeft = ref(0);
let timer = null;

// Математика круга
const radius = 35;
const circumference = 2 * Math.PI * radius;

const strokeDashoffset = computed(() => {
  // progress от 1 до 0
  const progress = Math.max(0, Math.min(1, timeLeft.value / props.totalDuration));
  return circumference - (progress * circumference);
});

// Форматирование времени (03:45)
const timeDisplay = computed(() => {
  const m = Math.floor(timeLeft.value / 60);
  const s = timeLeft.value % 60;
  return `${String(m).padStart(2, '0')}:${String(s).padStart(2, '0')}`;
});

const updateTimer = () => {
  // 1. Если пропса нет или он 0 — немедленно останавливаем всё
  if (!props.wakeUpAt || props.wakeUpAt === 0) {
    timeLeft.value = 0;
    if (timer) clearInterval(timer);
    return;
  }

  const now = Math.floor(Date.now() / 1000);
  const diff = props.wakeUpAt - now;

  if (diff > 0) {
    timeLeft.value = diff;
  } else {
    // 2. Время вышло — обнуляем и чистим интервал
    timeLeft.value = 0;
    if (timer) {
      clearInterval(timer);
      timer = null;
    }
  }
};

// Запуск при изменении пропса или монтировании
watch(() => props.wakeUpAt, (newVal) => {
  // Очищаем старый таймер в любом случае при изменении данных
  if (timer) clearInterval(timer);

  if (newVal && newVal > 0) {
    updateTimer();
    timer = setInterval(updateTimer, 1000);
  } else {
    // Если пришел 0 или null — обнуляем остаток
    timeLeft.value = 0;
  }
}, { immediate: true });

onUnmounted(() => {
  if (timer) clearInterval(timer);
});
</script>

<template>
  <div class="relative flex items-center justify-center">
    <svg width="120" height="120" class="transform -rotate-90">
      <circle
          cx="60" cy="60" :r="radius"
          stroke="#00FFFF" stroke-width="8" fill="transparent"
      />
      <circle
          cx="60" cy="60" :r="radius"
          stroke="#C0C0C0" stroke-width="8" fill="transparent"
          stroke-linecap="round"
          :stroke-dasharray="circumference"
          :stroke-dashoffset="strokeDashoffset"
          class="transition-all duration-1000 ease-linear"
      />
    </svg>

    <div v-if="timeLeft > 0" class="absolute flex flex-col items-center">
      <span class="text-2xl top-3 absolute font-mono font-bold text-white leading-none">
        {{ timeDisplay }}
      </span>

    </div>
  </div>
</template>