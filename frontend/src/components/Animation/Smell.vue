<script setup>

</script>

<template>
  <div  class="absolute inset-0 z-10 pointer-events-none font-pixel">
    <div class="smell-cloud smell-1"></div>
    <div class="smell-cloud smell-2"></div>
    <div class="smell-cloud smell-3"></div>
    <div class="smell-cloud smell-4"></div>
    <div class="smell-cloud smell-5"></div>
<!--    <div class="smell-cloud smell-6"></div>-->


    <div class="fly fly-1"></div>
    <div class="fly fly-2"></div>
    <div class="fly fly-3"></div>
  </div>
</template>

<style scoped>
.stench-active img {
  filter: sepia(0.2) hue-rotate(80deg) saturate(1.5);
}

/* --- 1. Зеленый запах (облачка) --- */
.smell-cloud {
  position: absolute;
  background-color: rgba(135, 224, 20, 0.6); /* Ядовито-зеленый полупрозрачный */
  border-radius: 50%;
  filter: blur(4px); /* Размытие для эффекта газа */
  bottom: 20%;
  left: 50%;
  opacity: 0;
}

/* Разные размеры и задержки для натуральности */
.smell-1 { width: 40px; height: 40px; animation: smell-rise 3s infinite linear; left: 40%; }
.smell-2 { width: 40px; height: 40px; animation: smell-rise 3s infinite linear 1s; left: 60%; }
.smell-3 { width: 40px; height: 45px; animation: smell-rise 4s infinite linear 0.5s; left: 30%; }
.smell-4 { width: 40px; height: 50px; animation: smell-rise 3s infinite linear; bottom: 0; left: 70%; }
.smell-5 { width: 40px; height: 40px; animation: smell-rise 3s infinite linear 1s; bottom: 0; left: 10%; }
.smell-6 { width: 40px; height: 45px; animation: smell-rise 4s infinite linear 0.5s; bottom: -30%; left: 10%;  }
@keyframes smell-rise {
  0% {
    transform: translateY(0) scale(0.5);
    opacity: 0;
  }
  20% {
    opacity: 0.7;
  }
  100% {
    transform: translateY(-120px) scale(1.2);
    opacity: 0;
  }
}

/* --- 2. Мухи --- */
/* Рисуем муху с помощью CSS (маленький черный квадратик с крылышками) */
.fly {
  position: absolute;
  width: 4px;
  height: 4px;
  background-color: black;
  /* Пиксельные крылышки через box-shadow */
  box-shadow: -2px -2px 0 #a9a9a9, 2px -2px 0 #a9a9a9;
}

/* Разные траектории для каждой мухи */
.fly-1 { top: 30%; left: 20%; animation: fly-buzz-1 1.5s infinite linear alternate; }
.fly-2 { top: 50%; left: 90%; animation: fly-buzz-2 1.2s infinite linear alternate-reverse; }
.fly-3 { top: 20%; left: 50%; animation: fly-buzz-3 2s infinite linear alternate; }

/* Хаотичные движения мух (можно настроить под себя) */
@keyframes fly-buzz-1 {
  0%   { transform: translate(0, 0) rotate(0deg); }
  25%  { transform: translate(10px, -15px) rotate(20deg); }
  50%  { transform: translate(-5px, -25px) rotate(-10deg); }
  75%  { transform: translate(15px, -5px) rotate(15deg); }
  100% { transform: translate(-10px, 10px) rotate(-5deg); }
}

@keyframes fly-buzz-2 {
  0%   { transform: translate(0, 0); }
  50%  { transform: translate(-20px, 10px); }
  100% { transform: translate(10px, 20px); }
}

@keyframes fly-buzz-3 {
  0%   { transform: translate(0, 0) scale(1); }
  50%  { transform: translate(15px, -30px) scale(0.8); }
  100% { transform: translate(-15px, -10px) scale(1.2); }
}

</style>