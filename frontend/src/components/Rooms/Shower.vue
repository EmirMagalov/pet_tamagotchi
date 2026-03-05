<script setup>
import Home from "@/components/Base/Home.vue";
import {inject, onMounted} from "vue";
import { storeToRefs } from 'pinia';
import { usePetStore } from "@/stores/petDataStore.js";
import { useUserStore } from "@/stores/userDataStore.js";

const petStore = usePetStore();
const userStore = useUserStore();


onMounted(async () => {

  const {sleepState } = storeToRefs(petStore);



  if (sleepState.value) {
    await petStore.toggleSleep();
  }
})

</script>

<template>
  <Home backgroundImage="/shower-room.png" roomType="showerRoom"/>
</template>

<style scoped>

</style>