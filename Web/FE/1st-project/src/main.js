import { createApp } from 'vue'
import { createPinia } from 'pinia';
import App from './App.vue'
import router from './router'
import piniaPluginPersistedstate from 'pinia-plugin-persistedstate';

import { useKakao } from 'vue3-kakao-maps/@utils'

import 'bootstrap'
import 'bootstrap/dist/css/bootstrap.min.css'

import VueSSE from 'vue-sse';

const app = createApp(App)
const pinia = createPinia();

pinia.use(piniaPluginPersistedstate);

useKakao('01f1b08e0b51a6a36084c1c22b333eaf')
app.use(pinia);
app.use(router);
app.use(VueSSE)

app.mount('#app')