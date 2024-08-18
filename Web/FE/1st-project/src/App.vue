<template>
  <div :class="{ 'login-background': isLoginBackground }" id="app">
    <NavbarComponent v-if="showNavbar" />
    <UserNavbarComponent v-if="store.IsManager" />
    <router-view></router-view>
  </div>
</template>

<script setup>
import { computed, onMounted, watch } from 'vue';
import { useRoute } from 'vue-router';
import { useUserStore } from '@/stores/user';
import { useFireStore } from '@/stores/fire';
import Swal from 'sweetalert2';
import router from '@/router/index';
import NavbarComponent from './components/UserNavbarComponent.vue';
import UserNavbarComponent from './components/UserNavbarComponent.vue';


const store = useUserStore();
const fireStore = useFireStore();
const route = useRoute();

const showNavbar = computed(() => !route.meta.hideNavbar);
const isLoginBackground = computed(() => route.meta.loginBackground);

let eventSource = null;

const connectToSSE = () => {
  eventSource = new EventSource(`${store.API_URL}fireissues/fire-popup/ `, {
    withCredentials: true,
    headers: {
      Authorization: `Token ${store.token}`,
    },
  });

  eventSource.onopen = (event) => {
    console.log('SSE connection opened:', event);
  };

  eventSource.onmessage = (event) => {
    try {
      const fireData = JSON.parse(event.data);
      console.log(event.data)
      fireStore.fireData = fireData
      Swal.fire({
        title: '화재 알림',
        icon: 'warning',
        text: `${fireData.building_name}에 화재가 발생하였습니다.!`,
        confirmButtonText: '건물상세',
        confirmButtonColor: '#C2191A',
        showCancelButton: true,
        cancelButtonText: '확인',
      }).then((result) => {
        if (result.isConfirmed) {
          router.push({ name: 'building-detail', params: { 'building_id': fireData.building_pk }})
        }
      })
    } catch (error) {
      console.error('JSON parsing error:', error);
    }
  };

  eventSource.addEventListener('ping', (event) => {
    console.log('Ping event received:', event.data);
  });

  eventSource.onerror = (error) => {
    console.error('SSE error:', error);
    if (error.eventPhase === EventSource.CLOSED) {
      console.log('SSE connection closed');
    } else {
      console.log('Reconnecting...');
      setTimeout(() => {
        connectToSSE();
      }, 3000);
    }
  };
};

onMounted(() => {
  connectToSSE();
});

// onUnmounted(() => {
//   if (eventSource) {
//     eventSource.close();
//     console.log('SSE connection closed');
//   }
// });

watch(isLoginBackground, (value) => {
  document.body.style.backgroundColor = value ? 'rgba(255, 255, 255, 0.49)' : 'white';
}, { immediate: true });
</script>

<style>
body {
  font-family: 'Inter', sans-serif;
  justify-content: center;
  align-items: center;
  align-content: center;
  height: 100%;
  margin: 0;
  padding: 0;
}

.login-background {
  background-color: rgba(194, 25, 26, 0.49);
}
</style>
