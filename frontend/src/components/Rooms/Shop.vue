<script setup>
import {foodData} from "@/FoodData/foodData.js";
import {inject} from "vue";
import { storeToRefs } from 'pinia';
import { usePetStore } from "@/stores/petDataStore.js";
import { useUserStore } from "@/stores/userDataStore.js";
import axios from "axios";
import {API_URL} from "@/config.js";

const petStore = usePetStore();
const userStore = useUserStore();
import {useHaptic} from "@/helpers/haptic.js";
const haptic = useHaptic();
const { petData, basket } = storeToRefs(petStore);
// const petData = inject('petData')
const buyItem = async (itemId) => {
  try {
    const { data } = await axios.post(`${API_URL}/buy/${userStore.userData.id}/${itemId}`);
    console.log(data);
    // Добавляем купленный предмет в массив basket
    // Теперь computed 'ownedFood' автоматически увидит новый товар!
    basket.value.push(data);

    haptic.success();
  } catch (error) {
    console.error("Ошибка при покупке", error);
  }
};
const emit = defineEmits(['close']); // Мы говорим: "Этот компонент умеет кричать 'close'"

const closeMenu = () => {
  emit('close'); // Вот здесь мы фактически "кричим"
};

const getCountInBasket = (foodId) => {
 return basket.value.filter(item => Number(item.item_id) === Number(foodId)).length;
};

</script>

<template>
  <div class="fixed inset-0 z-50 bg-gray-50/95 backdrop-blur-md font-bold overflow-hidden flex flex-col">

    <div class="pt-5 pb-3 border-b border-gray-200 bg-white/50">
      <div class="grid grid-cols-3 items-center w-full px-4">

        <div class="w-10 flex items-center gap-1">
          <img class="w-5" src="/coin.svg">
          <p>{{ petData.money }}</p>


        </div>

        <h1 class="text-center text-2xl font-black uppercase tracking-wide text-gray-800">
          Еда
        </h1>

        <div class="flex justify-end">
          <button
              @click="closeMenu"
              class="w-10 h-10 p-2 bg-gray-100 rounded-full active:scale-90 transition-transform"
          >
            <img src="/cancel.svg" class="w-full h-full " alt="Закрыть">
          </button>
        </div>
      </div>
    </div>

    <div class="flex flex-col gap-5 overflow-y-auto  p-4">
      <div v-for="food in foodData" :key="food.id">
        <div class="flex justify-center items-center gap-10 bg-[#E0E0E0]/30 p-2">
          <div class="flex flex-col justify-center items-center">
            <img class="w-20" :src="food.image" alt="">
            <div class="flex gap-1 min-w-20">
              <p class="text-xl">{{ food.name }}</p>
              <p class="text-[#dc562c]/50" v-show="getCountInBasket(food.id) >=1">x{{getCountInBasket(food.id)}}</p>
            </div>

          </div>

          <div class="flex flex-col gap-3 justify-center items-center">
            <div class="flex gap-1 justify-center items-center">
              <img class="w-5" src="/chicken.svg" alt="">
              <p>+{{ food.value }}%</p>
            </div>

            <div class="flex gap-1 justify-center items-center">
              <img class="w-5" src="/coin.svg" alt="">
              <p>{{ food.price }}</p>

            </div>
            <button @click = 'buyItem(food.id)' class="text-2xl bg-[#99FF33] p-2 rounded-2xl active:scale-80 transition-transform">Купить</button>


          </div>

        </div>
      </div>
    </div>

  </div>
</template>

<style scoped>

</style>