<script setup>
import {computed, inject, onUnmounted, ref, watch} from "vue";

import {storeToRefs} from 'pinia';
import {usePetStore} from "@/stores/petDataStore.js";
import {useUserStore} from "@/stores/userDataStore.js";


import WaterDrops from "@/components/Animation/WaterDrops.vue";
import Smell from "@/components/Animation/Smell.vue";
import FoamBubbles from "@/components/Animation/FoamBubbles.vue";
import {usePetLiveStats} from "@/petStore.js";

const isWashing = inject("isWashing");


const roomData = inject("roomData")


const showIndicator = inject("showIndicator")


const toastMessage = inject('toastMessage')
const isToastVisible = inject('isToastVisible')


const isSad = ref(false); // Состояние "хочу есть
const isHunger = ref(false);
let smileCycleTimeout = null;
const isShowingSmileNow = ref(false);
const isHappy = ref(false); // Режим "Сыт/Ок"
const isTired = ref(false);


let blinkTimeout = null;

const petStore = usePetStore();
const userStore = useUserStore();

const {petData, sleepState} = storeToRefs(petStore);
const {isDraggingFood,foodValue} = storeToRefs(petStore);
const {isBlinking} = storeToRefs(petStore);
const {image} = storeToRefs(petStore);
const {isBoosting} = storeToRefs(petStore);
const {isShampooing} = storeToRefs(petStore);
const {liveHunger, liveEnergy, liveDirt} = usePetLiveStats(petData);


// Функция, запускающая один "морг" и планирующая следующий
const scheduleNextBlink = () => {
  // Очищаем старый таймер, если он был
  if (blinkTimeout) clearTimeout(blinkTimeout);

  // ПРОВЕРКА: Если спит — выходим и не планируем следующее моргание
  if (petData.value?.is_sleeping) {
    isBlinking.value = false;
    return;
  }

  const nextBlinkDelay = Math.random() * 5000 + 5000;

  blinkTimeout = setTimeout(() => {
    isBlinking.value = true;

    setTimeout(() => {
      isBlinking.value = false;
      // Рекурсивно вызываем следующую проверку
      scheduleNextBlink();
    }, 150);
  }, nextBlinkDelay);
};
const scheduleSmileCycle = () => {
  if (smileCycleTimeout) clearTimeout(smileCycleTimeout);
  if (!isHappy.value || petData.value?.is_sleeping || isSad.value) {
    isShowingSmileNow.value = false;
    return;
  }
  // 3 сек улыбаемся, 4 сек отдыхаем (нейтральный рот)
  const nextChangeDelay = isShowingSmileNow.value ? 5000 : 1000;
  smileCycleTimeout = setTimeout(() => {
    isShowingSmileNow.value = !isShowingSmileNow.value;
    scheduleSmileCycle();
  }, nextChangeDelay);
};


// ... твои рефы
const isShowingSadNow = ref(false); // Показываем ли грусть прямо в эту секунду
let sadCycleTimeout = null;

const scheduleSadCycle = () => {
  if (sadCycleTimeout) clearTimeout(sadCycleTimeout);

  // Если не грустим или спим — выключаем отображение грусти
  if (!isSad.value || petData.value?.is_sleeping) {
    isShowingSadNow.value = false;
    return;
  }

  const nextChangeDelay = isShowingSadNow.value ? 5000 : 1000;

  sadCycleTimeout = setTimeout(() => {
    isShowingSadNow.value = !isShowingSadNow.value;
    scheduleSadCycle();
  }, nextChangeDelay);
};
const isLiveHungry = computed(() => Number(liveHunger.value) <= 20);
const isLiveTired = computed(() => Number(liveEnergy.value) <= 30 && !petData.value?.is_sleeping);
watch([isLiveHungry, isLiveTired, () => petData.value?.is_sleeping], ([hungry, tired, sleeping]) => {
  // 1. Если спит — сразу выходим и всё чистим
  if (sleeping) {
    isSad.value = isHappy.value = isBlinking.value = isShowingSadNow.value = isShowingSmileNow.value = false;
    isTired.value = isHunger.value = false;
    [blinkTimeout, sadCycleTimeout, smileCycleTimeout].forEach(clearTimeout);
    return;
  }

  // 2. Если проснулся — запускаем моргание, если оно еще не запущено
  if (!blinkTimeout) scheduleNextBlink();

  // 3. СИНХРОНИЗАЦИЯ СОСТОЯНИЙ (теперь они не зависят друг от друга)
  isTired.value = tired;
  isHunger.value = hungry;

  // 4. ЛОГИКА ЭМОЦИЙ
  if (hungry || tired) {
    // Если есть любая проблема — радость отключаем
    isHappy.value = false;
    isShowingSmileNow.value = false;
    if (smileCycleTimeout) clearTimeout(smileCycleTimeout);

    // Если голоден — запускаем цикл грусти
    if (hungry) {
      if (!isSad.value) {
        isSad.value = true;
        isShowingSadNow.value = true;
        scheduleSadCycle();
      }
    } else {
      // Если уже не голоден (но, возможно, еще устал) — убираем грустный рот
      isSad.value = false;
      isShowingSadNow.value = false;
      if (sadCycleTimeout) clearTimeout(sadCycleTimeout);
    }
  } else {
    // Если и не голоден, и не устал — ВРЕМЯ РАДОСТИ
    isSad.value = false;
    isShowingSadNow.value = false;
    if (sadCycleTimeout) clearTimeout(sadCycleTimeout);

    if (!isHappy.value) {
      isHappy.value = true;
      isShowingSmileNow.value = true;
      scheduleSmileCycle();
    }
  }
}, {immediate: true});


const currentMouthImage = computed(() => {
  if (petData.value?.is_sleeping) return '/mouth_normal.png';

  const dragging = isDraggingFood?.value || false;

  if ((dragging || isBoosting.value) && roomData.roomType === 'livingRoom') {

    return '/mouth_open.png';
  }
  if (isSad.value && isShowingSadNow.value) return '/mouth_sad.png';
  if (isHappy.value && isShowingSmileNow.value) return '/mouth_smile.png';
  // return '/mouth_normal.png';
  return '/mouth_normal.png';
});

onUnmounted(() => {
  if (blinkTimeout) {
    clearTimeout(blinkTimeout);
    blinkTimeout = null;
    console.log("👁️ Моргание остановлено");
  }
});
</script>

<template>

  <div v-show="isWashing">
    <WaterDrops/>
  </div>


  <div class="relative flex items-center justify-center">


    <div class="relative z-20  mt-5">


      <div v-if="showIndicator" class="boost-indicator absolute top-20 left-1/2">
        <div class="flex flex-col items-center">
          <img class="w-10" src="/chicken.svg">
          <span class="text-[#dc562c]">+{{foodValue}}</span>
        </div>
      </div>
      <!-- Круг (фон) -->
      <!--      <div :class="['absolute inset-0 rounded-full ',sleepState?'bg-[#f8fafc]/95 shadow-[10px_10px_50px_10px_#CCFFFF]':'bg-[#fbf7de]']"></div>-->


      <div v-show="liveDirt>=75">
        <Smell/>
      </div>

      <!-- Персонаж поверх -->
      <div
          :class="['relative boost-char  mt-15 flex items-center justify-center h-full', isBoosting?'animate-bounce-pet':'']">

        <Transition name="fade" mode="out-in">
          <div>
            <img v-show="!isLiveHungry" :key="image" src="/body-base.png " alt="" class="w-35">
            <img v-show="isLiveHungry" :key="image" src="/body-skinny.png " alt="" class="w-35">
            <div v-show="!petData?.is_sleeping && !isBlinking" class="">
              <img v-show="isTired" src="/eyelids.png" class="absolute top-0 left-0 z-30 ">
              <img v-show="isTired" src="/eyelids.png" class="absolute top-0 left-0.5 scale-x-[-1] z-30 ">
              <img src="/eyeball.png" class="absolute top-0 left-0 z-20 ">
              <img src="/eyeball.png" class="absolute top-0 left-10 z-20 ">
              <img src="/iris.png" class="absolute top-0 left-0 z-20 ">
              <img src="/iris.png" class="absolute top-0 left-10 z-20 ">
              <img src="/pupil.png" class="animate-pupil absolute top-0 left-0 z-20 ">
              <img src="/pupil.png" class="animate-pupil absolute top-0 left-10 z-20 ">
            </div>


            <div v-show="petData?.is_sleeping || isBlinking"
                 class="absolute inset-0 z-10 flex items-center justify-center">
              <img src="/eyelashes.png" class="w-full object-contain">
            </div>

            <div class="absolute inset-0 z-20 flex items-center justify-center">
              <Transition name="mouth-switch" mode="out-in">
                <img :key="currentMouthImage"
                     :src="currentMouthImage"
                     class="w-full object-contain">
              </Transition>
            </div>

          </div>

        </Transition>

        <div v-show="isShampooing">
          <FoamBubbles/>
        </div>
      </div>

    </div>
    <div v-show="isLiveHungry"
         class="absolute ping-custom duration-200 top-0 left-3 bg-black/80 rounded-full px-5 py-1 border border-red-600">
      <img class="w-6" src="/chicken.svg" alt="">
    </div>
    <div v-show="isLiveTired"
         class="absolute  ping-custom duration-200 top-10 left-3 bg-black/80 rounded-full px-5 py-1 border border-purple-500">
      <img class="w-6" src="/sleep.svg" alt="">
    </div>
    <div v-show="sleepState">
      <p class="z-letter z-1 absolute top-25 right-30 text-sm text-blue-300 font-bold">Z</p>
      <p class="z-letter z-2 absolute top-15 right-25 text-lg text-blue-300 font-bold">Z</p>
      <p class="z-letter z-3 absolute top-10 right-20 text-2xl text-blue-300 font-bold">Z</p>
    </div>
    <div>
      <p v-show="isToastVisible"
         class="z-1 absolute top-0 right-0 bg-white rounded-full px-5 py-1 border border-red-600">{{ toastMessage }}</p>
    </div>

  </div>


</template>

<style scoped>

/* В файле CSS или tailwind.config.js */
@keyframes pingCustom {
  0% {
    transform: scale(1);
    opacity: 1;
  }
  50% {
    transform: scale(1.1); /* Увеличиваем на 10% */
    opacity: 0.9; /* Чуть приглушаем */
  }
  100% {
    transform: scale(1);
    opacity: 1;
  }
}

.ping-custom {
  animation: pingCustom 1s cubic-bezier(0, 0, 0.2, 1) infinite;
}

@keyframes z-sleep {
  0% {
    opacity: 0;
    transform: translateY(10px) scale(0.8);
  }
  50% {
    opacity: 1;
  }
  100% {
    opacity: 0;
    transform: translateY(-20px) scale(1.2);
  }
}

.z-letter {
  animation: z-sleep 3s infinite; /* Анимация идет 3 секунды и повторяется бесконечно */
  opacity: 0; /* Изначально буквы невидимы */
}

/* Раздаем задержки каждой букве */
.z-1 {
  animation-delay: 0s;
}

.z-2 {
  animation-delay: 1s;
}

/* Появится через 1 сек */
.z-3 {
  animation-delay: 2s;
}

/* Появится через 2 сек */


/* Анимация подпрыгивания */
@keyframes bounce-pet {
  0%, 100% {
    transform: scale(1);
  }
  50% {
    transform: scale(1.1) translateY(-10px);
  }
}

.animate-bounce-pet {
  animation: bounce-pet 0.5s ease-out;
}

/* Анимация вылетающих сердечек/цифр */
@keyframes float-up {
  0% {
    transform: translateY(0) scale(0.5);
    opacity: 0;
  }
  20% {
    opacity: 1;
  }
  100% {
    transform: translateY(-100px) scale(1.2);
    opacity: 0;
  }
}

.boost-indicator {
  position: absolute;
  pointer-events: none;
  animation: float-up 1s ease-out forwards;
  font-weight: bold;
  font-size: 1.5rem;
  z-index: 100;
}


:deep(.invisible-ghost) {
  opacity: 0 !important;
}


.my-ghost {
  opacity: 0.1 !important; /* Делаем оригинал почти прозрачным */
}

.my-fallback {
  opacity: 1 !important;
  z-index: 9999 !important;
  transform: scale(1.2);
}

/* Анимация "Живой взгляд" */
@keyframes eye-move {
  /* 0-15%: Смотрит прямо */
  0%, 15% {
    transform: translate(0, 0) scale(1);
  }

  /* 17%: Резко посмотрел влево и чуть вверх */
  17%, 30% {
    transform: translate(-4px, -2px) scale(1);
  }

  /* 32%: Быстрое моргание (зрачок сплющивается) */
  /* 45%: Посмотрел вправо */
  45%, 60% {
    transform: translate(1px, 1px) scale(1);
  }

  /* 75%: Посмотрел вниз (задумался) */
  75%, 85% {
    transform: translate(0, 5px) scale(1.05);
  }

  /* 100%: Вернулся в центр */
  100% {
    transform: translate(0, 0) scale(1);
  }
}

.animate-pupil {
  /* 6 секунд — оптимально, чтобы движения не мельтешили */
  animation: eye-move 6s infinite ease-in-out;
  /* Важно для масштабирования при моргании */
  transform-origin: center;
}


</style>