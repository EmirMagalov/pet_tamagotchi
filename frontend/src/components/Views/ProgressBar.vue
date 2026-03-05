<script setup>
import {inject} from "vue";
import { storeToRefs } from 'pinia';
import { usePetStore } from "@/stores/petDataStore.js";
import { useUserStore } from "@/stores/userDataStore.js";

const petStore = usePetStore();
const userStore = useUserStore();

const { petData, sleepState } = storeToRefs(petStore);
const { isEnergyShaking } = storeToRefs(petStore);
// const petData = inject('petData')


import {usePetLiveStats} from "@/petStore.js";
const { liveHunger, liveEnergy, liveDirt } = usePetLiveStats(petData);
const { isHungerShaking } = usePetLiveStats(petData);


</script>

<template>
  <div class="relative flex flex-col w-full gap-5  p-2">
    <div :class="['flex items-center justify-center',isHungerShaking?'animate-shake':''] ">
      <div>
        <img class="w-7" src="/plus_icon.svg" alt="">
        <p v-show="isHungerShaking" class=" absolute text-[#dc562c] mx-auto text-sm"> <40% </p>
      </div>
      <div class="flex items-center justify-center gap-2">
        <div class="w-64 h-4 bg-gray-300 rounded-full overflow-hidden">
          <div class="h-full bg-[#00bd16] transition-all duration-700" :style="{ width: liveHunger + '%' }"></div>
        </div>

      </div>
    </div>
    <div :class="['flex items-center justify-center',isEnergyShaking?'animate-shake':''] ">
      <div class="">

        <img class="w-7" src="/energy.svg" alt="">
        <p v-show="isEnergyShaking" class=" absolute text-[#6666FF] mx-auto text-sm"> >85% </p>
      </div>

      <div class="flex items-center justify-center gap-2">
        <div class="w-64 h-4 bg-gray-300 rounded-full overflow-hidden">
          <div class="h-full bg-[#6666FF] transition-all duration-700" :style="{ width: liveEnergy + '%' }"></div>
        </div>

      </div>

    </div>

    <div :class="['flex items-center justify-center',isHungerShaking?'animate-shake':''] ">
      <div>
        <img class="w-7" src="/chicken.svg" alt="">
        <p v-show="isHungerShaking" class=" absolute text-[#dc562c] mx-auto text-sm"> <40% </p>
      </div>
      <div class="flex items-center justify-center gap-2">
        <div class="w-64 h-4 bg-gray-300 rounded-full overflow-hidden">
          <div class="h-full bg-[#dc562c] transition-all duration-700" :style="{ width: liveHunger + '%' }"></div>
        </div>

      </div>
    </div>

<!--    <p class="text-yellow-400">{{ Math.round(liveEnergy) }}%</p>-->
<!--    <p class="text-yellow-400">{{ Math.round(liveHunger) }}%</p>-->
<!--    <p class="text-yellow-400">{{liveDirt }}%</p>-->
  </div>
</template>

<style scoped>
.animate-shake {
  animation: shake 0.5s cubic-bezier(.36, .07, .19, .97) both;
  animation-iteration-count: 4; /* 0.5с * 4 = 2 секунды */
}

@keyframes shake {
  10%, 90% {
    transform: translate3d(-1px, 0, 0);
  }
  20%, 80% {
    transform: translate3d(2px, 0, 0);
  }
  30%, 50%, 70% {
    transform: translate3d(-4px, 0, 0);
  }
  40%, 60% {
    transform: translate3d(4px, 0, 0);
  }
}
</style>