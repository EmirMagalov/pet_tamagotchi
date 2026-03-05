<script setup>
import Home from "@/components/Base/Home.vue";
import {computed, onMounted, provide, ref} from "vue";
import axios from "axios";
import {API_URL} from "@/config.js";

import {useUserStore} from "@/stores/userDataStore.js";
import {usePetStore} from "@/stores/petDataStore.js";
import SimpleTimer from "@/components/Pet/SimpleTimer.vue";

const userStore = useUserStore();
const petStore = usePetStore();

const toastMessage = ref('');
const isToastVisible = ref(false);


const tg = window.Telegram.WebApp;
tg.expand()


// const isDraggingFood = ref(false);


const showToast = (message, duration = 1000) => {
  toastMessage.value = message;
  isToastVisible.value = true;

  // Убираем сообщение через указанное время
  setTimeout(() => {
    isToastVisible.value = false;
  }, duration);
};


onMounted(async () => {
  await userStore.getUserData();
  await petStore.getPets();
  await petStore.getBasket()
})


</script>

<template>

  <main>
    <RouterView/>
  </main>
</template>
