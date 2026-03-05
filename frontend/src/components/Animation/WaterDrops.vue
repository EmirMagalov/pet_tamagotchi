<script setup>
// Генерируем 20 случайных капель
const drops = Array.from({ length: 40 }, (_, i) => ({
  id: i,
  left: Math.random() * 100 + '%', // Случайная позиция по ширине
  delay: Math.random() * 0.5 + 's', // Случайная задержка
  duration: 0.5 + Math.random() * 0.5 + 's' // Случайная скорость
}));
</script>

<template>
  <div class="absolute w-30 left-30 inset-0 -top-5 z-40 pointer-events-none overflow-hidden rounded-full">
    <div
        v-for="drop in drops"
        :key="drop.id"
        class="water-drop"
        :style="{
        left: drop.left,
        animationDelay: drop.delay,
        animationDuration: drop.duration
      }"
    ></div>
  </div>
</template>

<style scoped>
.water-drop {
  position: absolute;
  top: -20px;
  width: 2px;
  height: 10px;
  background: #60a5fa; /* Голубой цвет (blue-400) */
  border-radius: 2px;
  opacity: 0.8;
  animation: fall linear infinite;
}

@keyframes fall {
  0% {
    transform: translateY(0);
    opacity: 1;
  }
  80% {
    opacity: 0.8;
  }
  100% {
    transform: translateY(300px); /* Падают вниз */
    opacity: 0;
  }
}
</style>