<script setup>
import {inject} from "vue";


import { storeToRefs } from 'pinia';
import { usePetStore } from "@/stores/petDataStore.js";
import { useUserStore } from "@/stores/userDataStore.js";

const petStore = usePetStore();
const userStore = useUserStore();

const { petData, sleepState } = storeToRefs(petStore);
const {userData } = storeToRefs(userStore);
// const petData = inject('petData')
</script>

<template>
<div  class="flex justify-between items-center bg-white rounded-3xl  py-3 px-5 mb-5">
  <div class="flex gap-1">
    <h1>{{userData?.username}}</h1>

  </div>
  <div class="text-xl">


    <div class="flex gap-1 items-center">
      <img class="w-5" src="/coin.svg" alt="">
      <p>{{petData?.money}}</p>
    </div>

  </div>
</div>
</template>

