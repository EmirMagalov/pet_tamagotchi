// stores/userDataStore.js
import { defineStore } from 'pinia';
import { ref } from 'vue';

export const useUserStore = defineStore('user', () => {
    const userData = ref(null);
    const tg = window.Telegram.WebApp;

    const getUserData = async () => {
        // В реальности тут будет tg.initDataUnsafe.user
        userData.value = { id: 7287871980, username: '⚙️springtrap⚙️' };
        tg.expand();
    };

    return { userData, getUserData, tg };
});