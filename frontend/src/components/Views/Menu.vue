<script setup>
import ProgressBar from "@/components/Views/ProgressBar.vue";
import MenuButtons from "@/components/Views/MenuButtons.vue";

</script>

<template>
  <div class="backdrop-blur-2xl   rounded-3xl h-screen  p-4 ">
    <div class="bg-white/55 p-3  rounded-3xl">
      <ProgressBar/>
      <div class="mt-2">
        <MenuButtons/>
      </div>
    </div>

  </div>
</template>

