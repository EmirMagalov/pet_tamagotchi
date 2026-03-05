// 1. Сначала ВСЕ импорты
import { createApp } from 'vue'
import { createPinia } from 'pinia'
import App from './App.vue'
import { createWebHashHistory, createRouter } from 'vue-router'

import './assets/main.css'
import Home from "@/components/Base/Home.vue"
import Shower from "@/components/Rooms/Shower.vue"
import SleepRoom from "@/components/Rooms/SleepRoom.vue";
// 2. Создаем экземпляры
const app = createApp(App)
const pinia = createPinia()

// 3. Настраиваем роутер
const routes = [
    { path: '/', component: Home },
    { path: '/shower', component: Shower },
    { path: '/sleepRoom', component: SleepRoom },
    { path: '/:pathMatch(.*)*', redirect: '/' }
]

const router = createRouter({
    history: createWebHashHistory(),
    routes,
})

// 4. ПРАВИЛЬНЫЙ ПОРЯДОК ПОДКЛЮЧЕНИЯ
app.use(pinia)   // Сначала Pinia!
app.use(router)  // Потом роутер
app.mount('#app') // И только в конце монтируем