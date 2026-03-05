// stores/petDataStore.js
import { defineStore, storeToRefs } from 'pinia';
import { ref, computed } from 'vue';
import axios from 'axios';
import { API_URL } from '@/config.js';
import { useUserStore } from './userDataStore.js';
import {useHaptic} from "@/helpers/haptic.js";

export const usePetStore = defineStore('pet', () => {
    const userStore = useUserStore();
    const petData = ref(null);
    const isBlinking = ref(false);
    const isDraggingFood = ref(false);
    const image = ref('')
    const sleepState = computed(() => petData.value?.is_sleeping ?? false);
    const isBoosting = ref(false);
    const foodValue = ref(0);
    const isShampooing = ref(false);
    const basket = ref([]);
    const isEnergyShaking = ref(false);
    const isHungerShaking = ref(false);
    const isFoodMenuOpen = ref(false);
    const haptic = useHaptic();
    const triggerShake = (type) => {
        if (type === 'energy') {
            isEnergyShaking.value = true;
            setTimeout(() => isEnergyShaking.value = false, 1000);
        }
        if (type === 'hunger') {
            isHungerShaking.value = true;
            setTimeout(() => isHungerShaking.value = false, 1000);
        }
    };


    const getPets = async () => {
        try {
            const { data } = await axios.get(`${API_URL}/pet/${userStore.userData.id}`);
            petData.value = data;
        } catch (error) {
            if (error.response?.status === 404) await createPet();
        }
    };

    const createPet = async () => {
        const payload = {
            telegram_id: userStore.userData.id,
            name: userStore.userData.username || "Мой питомец"
        };
        const { data } = await axios.post(`${API_URL}/pet/`, payload);
        petData.value = data;
    };

    const toggleSleep = async () => {
        if (!petData.value) return;
        try {
            const { data } = await axios.post(`${API_URL}/pet/sleep/${userStore.userData.id}`);
            petData.value = data;
            haptic.light()
        } catch (error) {
            // Здесь можно вызвать экшен из uiStore для тряски или тоста
            throw error; // Пробрасываем ошибку дальше для обработки в UI
        }
    };

    const getBasket = async () => {
        try {
            const {data} = await axios.get(`${API_URL}/buy/${userStore.userData.id}`);
            basket.value = data;
        }catch(error) {
            throw error;
        }


    }

    return { petData, sleepState, isBlinking, isDraggingFood,image,isBoosting,isShampooing,foodValue,isFoodMenuOpen,haptic, basket,getPets, toggleSleep,triggerShake,getBasket };
});