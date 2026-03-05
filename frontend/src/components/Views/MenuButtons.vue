<script setup>
import draggable from 'vuedraggable';
import {useHaptic} from '@/helpers/haptic.js';
import {computed, inject, ref, watch} from "vue";
import SimpleTimer from "@/components/Pet/SimpleTimer.vue";
import axios from "axios";
import {API_URL} from "@/config.js";
import {foodData} from "@/FoodData/foodData.js";


import {storeToRefs} from 'pinia';
import {usePetStore} from "@/stores/petDataStore.js";
import {useUserStore} from "@/stores/userDataStore.js";

const petStore = usePetStore();
const userStore = useUserStore();

const {petData, isFoodMenuOpen,basket} = storeToRefs(petStore);
const {userData} = storeToRefs(userStore);


let washTimer = null; // Переменная для хранения ID таймера
const onListChange = inject("onListChange")

const singleShower = ref([
  {id: 'shower', name: 'Душ', image: '/shower1.png', bgColor: 'bg-linear-to-b from-blue-500 to-white', width: 'w-8',},
  {id: 'shampoo', name: 'Шампунь', image: '/shampoo1.png', bgColor: 'bg-linear-to-b from-blue-500 to-white', width: 'w-10',},

]);

const singleLiving = computed(() => {
  if (!currentFoodItem.value) {
    // Возвращаем объект "пустого слота"
    return [{
      id: 'empty',
      name: 'Пусто',
      image: '/shop.svg', // Поставь сюда иконку замка или пустой тарелки
      bgColor: 'bg-gray-200/50', // Серый фон
      width: 'w-10',
      isEmpty: true // Наш маркер пустоты
    }];
  }

  return [{
    ...currentFoodItem.value,
    bgColor: 'bg-linear-to-t from-[#FFFF00]/50 to-[#FF9A00]',
    type: 'food',
    width: 'w-15',
    isEmpty: false
  }];
});
const roomData = inject("roomData");
const isWashing = inject("isWashing");
const haptic = useHaptic();
const {isDraggingFood} = storeToRefs(petStore);
const {isShampooing} = storeToRefs(petStore);


// const handleItemAction = (element) => {
//   // Если это кнопка сна (у которой стоит disabled: true)
//   if (element.id === 'sleep') {
//     sleep(); // Твоя функция сна
//     haptic.light();
//     return;
//   }
//
//   // Если это еда, и мы в режиме "без перетаскивания" (опционально)
//   // if (roomData.roomType === 'livingRoom') {
//   //   onListChange(element);
//   // }
// };

// const petData = inject('petData');
const isSleeping = computed(() => petData.value?.is_sleeping);
// const toggleSleep = inject('toggleSleep');

const sleep = async () => {
  await petStore.toggleSleep();
  // haptic.light();
};


// const startWash = () => {
//   // 1. Включаем флажок
//   isWashing.value = true;
//
//   // 2. Ждем 2000 мс (2 секунды) и выключаем
//   setTimeout(() => {
//     isWashing.value = false;
//   }, 1000);
// };



// 1. Фильтруем общую базу еды, оставляя только то, что есть в корзине
const ownedFood = computed(() => {
  if (!basket.value || basket.value.length === 0) return [];

  const groups = {};

  // Проходим по всем предметам в корзине (из БД)
  basket.value.forEach(basketItem => {
    const itemId = basketItem.item_id;

    if (!groups[itemId]) {
      // Находим статичные данные (картинка, название) из foodData
      // Внутри computed 'ownedFood'
      const staticData = foodData.find(f => Number(f.id) === Number(itemId));

      if (staticData) {
        groups[itemId] = {
          ...staticData,
          count: 0,
          dbIds: [] // Сюда будем складывать уникальные ID из таблицы Basket
        };
      }
    }

    if (groups[itemId]) {
      groups[itemId].count += 1;
      groups[itemId].dbIds.push(basketItem.id); // Запоминаем ID конкретной записи
    }
  });

  return Object.values(groups);
});

// 2. Выбранная еда (теперь она инициализируется из ownedFood)
const selectedFoodId = ref(null);

// Следим за тем, чтобы если еда появилась, мы её выбрали по умолчанию
watch(ownedFood, (newVal) => {
  if (newVal.length > 0) {
    // Если ничего не выбрано ИЛИ выбранный товар исчез из рюкзака
    const stillExists = newVal.find(f =>  Number(f.id) ===  Number(selectedFoodId.value));
    if (!selectedFoodId.value || !stillExists) {
      selectedFoodId.value = newVal[0].id;
    }
  } else {
    selectedFoodId.value = null;
  }
}, { immediate: true, deep: true });

// 3. Обновляем текущий индекс (теперь ищем в ownedFood)

// Обновляем список для комнаты динамически


const currentFoodItem = computed(() => {
  return ownedFood.value.find(item => item.id === selectedFoodId.value) || null;
});

// 4. Функции переключения (теперь по ownedFood)
const nextFood = () => {
  if (ownedFood.value.length === 0) return;
  haptic.light();
  const idx = ownedFood.value.findIndex(item => item.id === selectedFoodId.value);
  const nextIdx = (idx + 1) % ownedFood.value.length;
  selectedFoodId.value = ownedFood.value[nextIdx].id;
};

const prevFood = () => {
  if (ownedFood.value.length === 0) return;
  haptic.light();
  const idx = ownedFood.value.findIndex(item => item.id === selectedFoodId.value);
  const prevIdx = (idx - 1 + ownedFood.value.length) % ownedFood.value.length;
  selectedFoodId.value = ownedFood.value[prevIdx].id;
};

const currentIndex = computed(() =>
    ownedFood.value.findIndex(item => item.id === selectedFoodId.value)
);
const currentItems = computed(() => {
  const mapping = {
    livingRoom: singleLiving.value,
    showerRoom: singleShower.value,
  };
  return mapping[roomData.roomType] || [];
});

const trackMovement = async (e) => {
  const dropZone = document.getElementById('pet-drop-zone');
  if (!dropZone) return;

  // 1. Получаем координаты (Универсально: тач или мышь)
  let clientX, clientY;
  if (e.touches && e.touches.length > 0) {
    clientX = e.touches[0].clientX;
    clientY = e.touches[0].clientY;
  } else {
    clientX = e.clientX;
    clientY = e.clientY;
  }

  // 2. Проверяем попадание
  const rect = dropZone.getBoundingClientRect();
  const isInside =
      clientX >= rect.left &&
      clientX <= rect.right &&
      clientY >= rect.top &&
      clientY <= rect.bottom;

  // 3. РЕАКЦИЯ В РЕАЛЬНОМ ВРЕМЕНИ
  if (isInside) {
    // Мы ВНУТРИ зоны. Включаем анимацию!
    isWashing.value = true
    if (!washTimer) {
      console.log("🚿 Таймер запущен (5 сек)...");

      washTimer = setTimeout(async () => {
        // ЭТО СРАБОТАЕТ ЧЕРЕЗ 5 СЕКУНД
        console.log("✨ ПИТОМЕЦ ПОМЫТ!");
        window.removeEventListener('mousemove', trackMovement);
        window.removeEventListener('touchmove', trackMovement);
        if (petData.value) {

          petData.value.dirt = 0;
          isWashing.value = false
          await axios.post(`${API_URL}/pet/bathe/${userData.value?.id}`)
          isShampooing.value = false

        }

        washTimer = null;

      }, isShampooing.value === false ? 7000 : 3000); // 5000 мс = 5 секунд
    }
  } else {
    // Мы ВЫШЛИ из зоны. Выключаем.
    isWashing.value = false
    resetWashingState();

  }

};

const resetWashingState = () => {
  isWashing.value = false;
  document.body.classList.remove('water-active');

  // Если таймер тикал - отменяем его
  if (washTimer) {
    console.log("🚫 Мытье прервано");
    clearTimeout(washTimer);
    washTimer = null;
  }
};
const checkDrop = (evt) => {
  const dropZone = document.getElementById('pet-drop-zone');
  if (!dropZone) return;
  // 1. Получаем координаты пальца/мыши в момент отпускания
  // SortableJS дает нам событие. Если это тач - берем changedTouches
  const originalEvent = evt.originalEvent;
  let clientX, clientY;

  if (originalEvent.changedTouches && originalEvent.changedTouches.length > 0) {
    clientX = originalEvent.changedTouches[0].clientX;
    clientY = originalEvent.changedTouches[0].clientY;
  } else {
    clientX = originalEvent.clientX;
    clientY = originalEvent.clientY;
  }

  // 2. Получаем координаты зоны персонажа
  const rect = dropZone.getBoundingClientRect();

  // 3. Математика: Попал ли палец внутрь квадрата?
  const isInside =
      clientX >= rect.left &&
      clientX <= rect.right &&
      clientY >= rect.top &&
      clientY <= rect.bottom;

  if (isInside) {
    const item = currentItems.value[evt.oldIndex];
    if (item && item.id === 'shampoo') {
      isShampooing.value = true
    }


    // УРА! ПОПАЛИ!
    handleFeed(evt); // Вызываем твою функцию кормления
  }
};

const handleFeed = async (itemDom) => {
  if (roomData.roomType === 'livingRoom') {
    // Получаем объект еды из нашего вычисляемого списка
    const foodItem = singleLiving.value[itemDom.oldIndex];

    // ПРОВЕРКА: есть ли вообще объект и есть ли в нем массив dbIds
    if (foodItem && foodItem.dbIds && foodItem.dbIds.length > 0) {
      console.log("Кормим! ID из базы:", foodItem.dbIds[0]);

      // Передаем в onListChange сам объект и ПЕРВЫЙ ID из базы для удаления
      await onListChange(foodItem, foodItem.dbIds[0]);
    } else {
      console.warn("Попытка покормить несуществующей едой или еда без ID из БД");
    }
  }
};
const onDragStart = (evt) => {
  isDraggingFood.value = true;

  // Проверяем, что взяли именно ДУШ
  // (evt.oldIndex - индекс элемента в массиве)
  const item = currentItems.value[evt.oldIndex];

  if (item && item.id === 'shower') {
    console.log(item.id)
    // НАЧИНАЕМ СЛЕДИТЬ ЗА КООРДИНАТАМИ
    window.addEventListener('mousemove', trackMovement);
    window.addEventListener('touchmove', trackMovement, {passive: false});
  }
};

const onDragEnd = (evt) => {
  isDraggingFood.value = false;
  isWashing.value = false
  window.removeEventListener('mousemove', trackMovement);
  window.removeEventListener('touchmove', trackMovement);
  resetWashingState();
  checkDrop(evt);

};

</script>

<template>
  <div class="flex justify-center gap-5">
    <div v-if="currentItems.length > 0">
      <draggable
          :list="currentItems"
          item-key="id"
          :group="{ name: 'food', pull: 'clone', put: false }"
          class="flex gap-5"
          :sort="false"
          :disabled="currentItems[0]?.isEmpty"
          :force-fallback="true"
          :fallback-on-body="true"
          fallback-class="flying-burger"
          @start="onDragStart"
          @end="onDragEnd"
      >
        <template #item="{ element }">
          <div
              @click="isFoodMenuOpen = true? element.id ==='empty':''"
              class="relative  touch-none h-25 w-30 flex flex-col justify-center items-center p-3 rounded-3xl shadow-lg active:scale-95 cursor-grab active:cursor-grabbing"
              :class="element.bgColor"
          >
            <img

                draggable="false"
                class="select-none pointer-events-none"
                :class="element.width"
                :src="element.image"
                :alt="element.name"
            />
            <p class="absolute font-bold text-white bottom-2 right-5 " v-show="element.count" >x{{element.count}}</p>
          </div>

        </template>

      </draggable>
      <div v-if="roomData.roomType === 'livingRoom' && ownedFood.length >1" class="flex  justify-center ">
        <img @pointerdown=prevFood  class="w-15  active:scale-90 transition-transform " src="/left_icon.svg">
        <img @pointerdown=nextFood class="w-15  active:scale-90 transition-transform " src="/right_icon.svg">
      </div>
    </div>

    <div
        v-if="roomData.roomType === 'livingRoom'"
        @pointerdown="sleep"
        class="relative border border-black/60 cursor-pointer h-25 w-30 flex flex-col justify-center items-center p-3 rounded-3xl transition-transform shadow-lg bg-linear-to-b/srgb from-[#7F00FF] to-[#ab89f7]/30 active:scale-95 "
    >
      <img
          class="w-15 select-none pointer-events-none"
          :src="isSleeping ? '/alarm_icon.png' : '/sleep_icon.png'"
          alt="Сон"
      >

      <div v-if="isSleeping" class="absolute inset-0 flex items-center justify-center bg-black/20 rounded-3xl">
        <SimpleTimer
            :wake-up-at="petData?.wake_up_at"
            :total-duration="12000"
        />
      </div>

    </div>

  </div>

<!--  <div v-else class="h-10">-->

<!--  </div>-->

</template>

<style>
.flying-burger img {
  opacity: 1 !important;
  width: 45% !important;
  /* Отключаем плавность, чтобы она сразу была четкой */

}

/* Твои старые стили контейнера оставь как есть */
.flying-burger {
  opacity: 1 !important;
  background: transparent !important;
  border: none !important;
  box-shadow: none !important;

}
.flying-burger p {
  display: none !important;
}
/* ... твои старые стили для flying-burger ... */

/* 1. ПОДГОТОВКА: Маркер, что это именно душ */
.shower-item {
  position: relative;
}

/* 2. САМА ВОДА (По умолчанию скрыта) */
.shower-item::after {
  content: '';
  position: absolute;
  top: 80%; /* Начинается снизу картинки */
  left: 20%; /* Немного отступаем слева */
  width: 60%; /* Ширина потока */
  height: 0; /* Изначально воды нет */
  background: repeating-linear-gradient(
      0deg,
      transparent,
      transparent 4px,
      #60a5fa 4px,
      #60a5fa 8px
  ); /* Полоски воды */
  opacity: 0;
  transition: opacity 0.2s, height 0.2s;
  pointer-events: none;
  z-index: -1; /* Чтобы вода была как бы за/под душем, или поставь 10 если хочешь поверх */
}

/* 3. АКТИВАЦИЯ: Когда на body висит класс "water-active" */
body.water-active .flying-burger .shower-item::after {
  height: 100px; /* Длина струи */
  opacity: 1;
  animation: water-flow 0.5s linear infinite;
}

/* Анимация падения воды */
@keyframes water-flow {
  from {
    background-position: 0 0;
  }
  to {
    background-position: 0 20px;
  }
}

</style>