<template>
  <div class="header">
    <div class="logo">
      <img src="@/assets/logo.png" alt="Logo">
      <div>프라리</div>
    </div>
    <nav class="navbar">
      <div class="top-btn">
        <ul>
          <li @click="fireSituation">화재상황</li>
          <li class="divider">|</li>
          <li @click="userLogout">로그아웃</li>
        </ul>
      </div>
      <div class="main-nav">
        <ul>
          <li><router-link to="/regist">로봇 등록</router-link></li>
          <li><router-link to="/building">관내 건물</router-link></li>
        </ul>
      </div>
    </nav>
  </div>
</template>

<script setup>
import router from "@/router/index"
import { useUserStore } from '@/stores/user';

const store = useUserStore();

const userLogout = () => {
  store.logOut();
}

const fireSituation = () => {
  router.push({ path: "/fire-building"});
}

</script>

<style scoped>
.header {
  display: flex;
  justify-content: space-between;
  width: 100%;
  height: 150px;
  background: #C2191A;
  align-items: center;
  padding: 0 20px;
  box-sizing: border-box;
}

.header .logo {
    display: flex;
    align-items: center;
}

.header .logo img {
    border-radius: 50%;
    width: 98px;
    height: 97px;
    margin-right: 10px;
}

.header .logo div {
    color: white;
    font-size: 40px;
}

.navbar {
  display: flex;
  flex-direction: column;
  align-items: center;
  background-color: #C2191A;
  overflow: hidden;
}

.navbar .top-btn ul {
  display: flex;
  align-items: center;
  margin: 0;
  padding: 0;
  list-style-type: none;
}

.navbar .top-btn li {
  color: #FFD429;
  margin: 0 10px;
  cursor: pointer;
}

.navbar ul {
  list-style-type: none;
  padding: 0;
}

.navbar .top-btn {
  color : #FFD429;
  text-decoration: none;
  margin-left: auto;
  margin-left: 50px;
}

.navbar .top-btn .divider {
  color: white;
}

.navbar .main-nav ul {
  display: flex;
  margin: 0;
  margin-top: 20px;
  
  padding: 0;
  list-style-type: none;
}

.navbar .main-nav li {
  margin-left: 10px;
}

.navbar .main-nav li a {
  display: block;
  color: white;
  padding: 14px 16px;
  text-decoration: none;
  font-size: 20px;
}

.navbar .main-nav li a:hover {
  background-color: #aa202c;
}

.navbar li {
  float: left;
}

.navbar li a {
  display: block;
  color: white;
  padding: 14px 16px;
  text-decoration: none;
  font-size: 20px;
}

.navbar li a:hover {
  background-color: #C2191A;
}

@media (max-width: 768px) {
  .header {
    height: auto;
    padding: 10px;
  }

  .navbar .top-btn ul,
  .navbar .main-nav ul {
    flex-direction: row;
    justify-content: center;
    margin: 0;
  }

  .navbar .top-btn li,
  .navbar .main-nav li {
    margin: 5px;
  }

  .navbar .main-nav li a {
    padding: 10px;
    font-size: 16px;
  }
}

@media (max-width: 480px) {
  .header .logo div {
    font-size: 30px;
  }

  .navbar .main-nav li a {
    padding: 8px;
    font-size: 14px;
  }

  .navbar .top-btn li {
    font-size: 14px;
  }
}
</style>