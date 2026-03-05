<script setup>
import Character from "@/components/Pet/Character.vue";
import Lavel from "@/components/Views/Lavel.vue";
import Menu from "@/components/Views/Menu.vue";
import Shop from "@/components/Rooms/Shop.vue";
import axios from 'axios';
import {API_URL} from "@/config.js";
import {provide, ref} from "vue";
import { storeToRefs } from 'pinia';
import {usePetStore} from "@/stores/petDataStore.js";
import {useUserStore} from "@/stores/userDataStore.js";
const petStore = usePetStore();
const userStore = useUserStore();
import {useHaptic} from "@/helpers/haptic.js";
const haptic = useHaptic();
// Достаем реактивные данные через storeToRefs
const { petData, sleepState,isBoosting,foodValue} = storeToRefs(petStore);
const {isFoodMenuOpen, basket} = storeToRefs(petStore);
const { userData } = storeToRefs(userStore);

// Функции (actions) берем напрямую


const isWashing = ref(false)
const isFoodOver = ref(false);


const showIndicator = ref(false);



import {useRouter} from 'vue-router';

const router = useRouter();
const props = defineProps({
  backgroundImage: {type: String, default: '/home.png'},
  menuButton: {type: String, default: 'livingRoom'},
  roomType: {type: String, default: 'livingRoom'},
})

// const roomIcon = computed(() => {
//   const icons = {
//     'shower': '/living-navigate.svg', // Если мы в душе, кнопка ведет в гостиную
//     'livingRoom': '/shower-navigate.svg',  // Если в гостиной, кнопка ведет в душ
//     'sleepRoom': '/living-navigate.svg',    // Добавляй сколько угодно комнат
//     // 'kitchen': '/bedroom.svg'
//   };
//
//   // Возвращаем иконку по ключу, либо дефолтную
//   return icons[props.roomType] || '/living-navigate.svg';
// });

const roomNavigate = ref([
  {name: "livingRoom", image: "/living-navigate.svg"},
  {name: "showerRoom", image: "/shower-navigate.svg"},
  // {name: "sleepRoom", image: "/sleep-navigate.svg"},
])


const navigate = (room) => {
  let target
  if (room === 'livingRoom') {
    target = '/'
  } else if (room === 'showerRoom') {
    target = '/shower'
  } else if (room === 'sleepRoom') {
    target = '/sleepRoom'
  }

  router.push(target);
  haptic.light(); // Опционально: вибрация при переходе
};
const onListChange = async (foodData, basketId) => {
  // Библиотека сама делит события на "добавлено", "удалено", "перемещено"

  if (foodData) {
    setTimeout(() => {
      isBoosting.value = false;
      showIndicator.value = false;
      foodValue.value = 0
    }, 1000);
    // const item = event.id;

    try {
      // 1. Если спит — будим первым делом
      if (petData.value?.is_sleeping) {
        await petStore.toggleSleep();
      }

      // 2. Теперь кормим
      const {data} = await axios.post(`${API_URL}/pet/food/${userData.value?.id}/${foodData.value}/${basketId}`);
      // 3. Обновляем данные результатом КОРМЛЕНИЯ (он теперь приоритетный)
      petData.value = data;
      const index = basket.value.findIndex(item => item.id === basketId);

      if (index !== -1) {
        basket.value.splice(index, 1);
        console.log("✅ Предмет удален из локального стора. Осталось в корзине:", basket.value.length);
      } else {
        console.warn("❌ Предмет не найден в массиве basket. Проверь, откуда пришел basketId");
      }
      isBoosting.value = true;
      showIndicator.value = true;
      foodValue.value = foodData.value;
      isFoodOver.value = false;
      haptic.success();

    } catch (error) {
      console.log(error);
    }

    // 2. Убираем классы анимации после завершения, чтобы их можно было запустить снова


    // alert(`Вы положили в корзину: ${item.name}`);
  }
};


provide("roomData", props)
provide("isFoodOver", isFoodOver)

provide("showIndicator", showIndicator)
provide("onListChange", onListChange)
provide("isWashing", isWashing)

</script>

<template>
  <div class="absolute  top-5 left-25 z-20 h-60 w-40" id="pet-drop-zone">

  </div>
  <div v-if="petData" class="min-h-screen overflow-hidden">

    <div
        :class="[
        'absolute inset-0 bg-gradient-to-b from-[#FAF1B6] via-[#f8f0c1] to-white transition-opacity duration-1000 ease-in-out',
        sleepState ? 'opacity-0' : 'opacity-100'
      ]"
    ></div>

    <div
        :class="[
        'absolute inset-0 bg-gradient-to-b from-[#000000] via-[#202020] to-white transition-opacity duration-1000 ease-in-out',
        sleepState ? 'opacity-100' : 'opacity-0'
      ]"
    ></div>

    <Transition name="sky" mode="out-in">

      <div
          v-if="!sleepState"
          key="sun"
          class="absolute top-10  h-30 w-30 rounded-full bg-[#fbf7de] shadow-[0_0_20px_rgba(251,247,222,0.6)]"
      ></div>

      <div
          v-else
          key="moon"
          class="absolute top-10  h-30 w-30 rounded-full bg-[#f8fafc]/95 shadow-[10px_10px_50px_10px_#CCFFFF]"
      ></div>

    </Transition>

    <img class="absolute  z-10" :src="props.backgroundImage || '/home.png' " alt="">

    <div class="absolute z-50 top-20  right-3 flex flex-col justify-center gap-2">
      <div @pointerdown="isFoodMenuOpen = true"
           class="cursor-pointer touch-none select-none active:scale-95 transition-transform">
        <img src="/shop.svg" alt="" class=" bg-red-400 rounded-full w-13 p-1 border  shadow-md">
      </div>

    </div>
    <div class="absolute z-50 top-55  right-3 flex flex-col justify-center gap-2 pointer-events-none">

      <div
          v-for="room in roomNavigate"
          :key="room.name"
          v-show="props.roomType !== room.name"
          class="pointer-events-auto"
      >
        <div
            @pointerdown="navigate(room.name)"
            class="cursor-pointer touch-none select-none active:scale-95 transition-transform"
            style="-webkit-tap-highlight-color: transparent;"
        >
          <img
              class="bg-white rounded-full w-13 p-1 border border-gray-200 shadow-md"
              :src="room.image"
              alt="Переход"
          >
        </div>
      </div>

    </div>
    <!--    <div v-show="props.roomType!='showerRoom'" class="absolute top-45 z-20   right-3 cursor-pointer active:scale-95">-->
    <!--      <div-->
    <!--          @pointerdown="navigate('showerRoom')"-->
    <!--          class="cursor-pointer touch-none select-none active:scale-95 transition-transform"-->
    <!--          style="-webkit-tap-highlight-color: transparent;"-->
    <!--      >-->
    <!--        <img-->
    <!--            class="bg-white rounded-full w-13 p-1 border border-gray-200"-->
    <!--            src="/shower-navigate.svg"-->
    <!--            alt="Переход"-->
    <!--        >-->
    <!--      </div>-->

    <!--    </div>-->
    <!--    <div v-show="props.roomType!='sleepRoom'" class="absolute top-60 right-3 z-20 cursor-pointer active:scale-95">-->
    <!--      <div-->
    <!--          @pointerdown="navigate('sleepRoom')"-->
    <!--          class="cursor-pointer touch-none select-none active:scale-95 transition-transform"-->
    <!--          style="-webkit-tap-highlight-color: transparent;"-->
    <!--      >-->
    <!--        <img-->
    <!--            class="bg-white rounded-full w-13 p-1 border border-gray-200"-->
    <!--            src="/sleep-navigate.svg"-->
    <!--            alt="Переход"-->
    <!--        >-->
    <!--      </div>-->

    <!--    </div>-->
    <div class="relative z-10 ">
      <div class="mt-2">
        <Lavel/>
      </div>


      <div class="relative z-1">
        <Character/>
      </div>

      <div class="relative z-10  mt-5 ">
        <Menu/>
      </div>


    </div>

  </div>
  <Shop v-if="isFoodMenuOpen" @close="isFoodMenuOpen = false"/>
</template>

<style>
.sky-enter-active,
.sky-leave-active {
  transition: all 0.5s cubic-bezier(0.4, 0, 0.2, 1);
}

/* Новое светило (входит) */
.sky-enter-from {
  opacity: 0;
  transform: translateY(100%); /* Начинает путь снизу */
}

/* Старое светило (уходит) */
.sky-leave-to {
  opacity: 0;
  transform: translateY(-100%); /* Улетает вверх */
}


</style>

