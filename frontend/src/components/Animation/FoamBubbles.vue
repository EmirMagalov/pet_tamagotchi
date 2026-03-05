<template>
  <div class="foam-container">
    <div
        v-for="bubble in bubbles"
        :key="bubble.id"
        class="bubble"
        :style="bubble.style"
    ></div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';

const props = defineProps({
  count: {
    type: Number,
    default: 25
  }
});

const bubbles = ref([]);

const generateBubbles = () => {
  const newBubbles = [];
  for (let i = 0; i < props.count; i++) {
    const size = Math.random() * 30 + 15 + 'px';
    newBubbles.push({
      id: i,
      style: {
        width: size,
        height: size,
        left: Math.random() * 70 + '%',
        top: Math.random() * 80 + '%',
        // Используем разные задержки и длительность, чтобы пена "дышала"
        animationDelay: Math.random() * 2 + 's',
        animationDuration: 2 + Math.random() * 2 + 's'
      }
    });
  }
  bubbles.value = newBubbles;
};

// Генерируем один раз при создании компонента, чтобы они не дергались
generateBubbles();
</script>

<style scoped>
.foam-container {
  position: absolute;
  inset: -10px; /* Немного выходим за границы персонажа */
  pointer-events: none;
  z-index: 30;
}

.bubble {
  position: absolute;
  background: white;
  border-radius: 50%;
  opacity: 0.7;
  filter: blur(1px); /* Размытие делает пену мягкой */
  border: 1px solid rgba(255, 255, 255, 0.4);
  /* Эффект объема пузырька */
  box-shadow: inset -3px -3px 6px rgba(0, 0, 0, 0.05),
  inset 2px 2px 4px rgba(255, 255, 255, 0.9);
  animation: float-foam ease-in-out infinite alternate;
}

@keyframes float-foam {
  0% { transform: translate(0, 0) scale(1); }
  50% { transform: translate(1px, -2px) scale(1.05); }
  100% { transform: translate(-2px, -3px) scale(1.1); }
}
</style>