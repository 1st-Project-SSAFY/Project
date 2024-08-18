<template>
  <div :class="{ 'login-background' : isLoginBackground }" id="app">
    <NavbarComponent v-if="showNavbar" />

    <router-view @route-changed="onRouteChange"></router-view>
    <router-link to="/login">login</router-link>
    <br>
    <router-link to="/regist">regist</router-link>
    <br>
    <router-link to="/building">building</router-link>
    <br>
    <router-link to="/detail">detail</router-link>
    <br>
    <router-link to="/robot-detail">robot-detail</router-link>
    <br>
    <router-link to="/fire-building">fire-building</router-link>
    <br>
    <router-link to="/test">maptest</router-link>
    <br>
    <router-link to="/signup">signup</router-link>
  </div>
</template>


<script>


import { computed, watch } from 'vue';
import { useRoute } from 'vue-router';
import NavbarComponent from './components/NavbarComponent.vue';
// import { KakaoMap } from 'vue3-kakao-maps';


export default {
  name: 'App',
  components: {
    NavbarComponent,
    // KakaoMap
  },
  setup() {
    const route = useRoute();
    const showNavbar = computed(() => !route.meta.hideNavbar);
    const isLoginBackground = computed(() => route.meta.loginBackground);

    watch(isLoginBackground, (value) => {
      if (value) {
        document.body.style.backgroundColor = 'rgba(255, 255, 255, 0.49)';
      } else {
        document.body.style.backgroundColor = 'white';
      }
    }, {immediate: true});

    return { showNavbar, isLoginBackground };
  }
};
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