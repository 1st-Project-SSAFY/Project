<template>
  <div class="container">
    <img class="lock-img" src="https://cdn-icons-png.flaticon.com/512/5446/5446336.png" alt="Lock Image">
    <div class="title">관리자 로그인</div>
    <form class="login-container" @submit.prevent>
      <div class="radio-select">
        <input type="radio" class="btn-check" name="options-base" id="firefighter" value="1" autocomplete="off" v-model="job" checked>
        <label class="btn" for="firefighter">소방관</label>
        <input type="radio" class="btn-check" name="options-base" id="manager" value="2" autocomplete="off" v-model="job">
        <label class="btn" for="manager">건물 관리자</label>
      </div>

      <div class="login-group">
        <!-- <img src="@/assets/사람.png" alt="User Icon"> -->
        <input type="text" placeholder="소방관 이름" v-model="username">
      </div>
      <div class="login-group">
        <!-- <img src="@/assets/열쇠.png" alt="Key Icon"> -->
        <input type="password" placeholder="소방관 코드" v-model="password">
      </div>
      <div class="signup">
        <router-link :to="{ name: 'signup' }">신규 소방관 등록</router-link>
      </div>
      <button class="login-btn" @click="logIn">Log In</button>
    </form>
  </div>
</template>

<script setup>
import { useUserStore } from '@/stores/user';
import { ref } from "vue";

const store = useUserStore();
const username = ref('');
const password = ref('');
const job = ref('1');

const logIn = () => {
  const payload = {
    username: username.value,
    password: password.value,
    job: job.value,
  }
  console.log('로그인 정보:', payload)
  store.logIn(payload)
  password.value = ''
}
</script>

<style scoped>
.container {
  display: flex;
  flex-direction: column;
	justify-content: center;
  align-items: center;
  width: 100%;
  height: 100vh;
  padding: 20px;
  box-sizing: border-box;
}

.lock-img {
  width: 100px;
  margin-bottom: 30px;
}

.title {
  color: #C2191A;
  font-size: 35px;
  font-weight: 700;
  margin-bottom: 40px;
}

.login-container {
	display: flex;
	flex-direction: column;
  width: 100%;
  max-width: 600px;
  padding: 40px;
  background-color: white;
  border-radius: 15px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
}

.radio-select {
  align-self: flex-start;
  margin-bottom: 30px;
}

.radio-select .btn-check:checked + .btn {
  border: 2px solid #EC8743;
}

.login-group {
  position: relative;
  margin-bottom: 20px;
}

.login-group input {
  width: calc(100% - 20px); 
  padding: 12px 15px;
  padding-left: 24px;
  font-size: 16px;
  border-radius: 10px;
  border: 1px solid #ccc;
  box-sizing: border-box;
  outline: none;
  transition: border-color 0.3s ease;
}

.login-group img {
	margin-left: 25px;
  position: absolute;
  width: 24px;
  left: 10px;
  top: 50%;
  transform: translateY(-50%);
}

input::placeholder {
	text-align: right;
}

.signup {
  display: flex;
  flex-direction: column;
	text-align: right;
	margin-right: 10px;
  margin-bottom: 20px;
}

.signup a {
  color: #EC8743;
  font-size: 18px;
  text-decoration: none;
}

.signup a:hover {
  text-decoration: underline;
}

.form-check-input {
  width: 0.75rem;
  height: 0.75rem;
  background-color: #EC8743;
}

.login-btn {
  width: 100%;
  padding: 12px 0;
  font-size: 18px;
  font-weight: 700;
  color: white;
  background-color: #C2191A;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  transition: background-color 0.3s ease;
}

.login-btn:hover {
  background-color: #bd4646;
}

@media (max-width: 768px) {
  .container {
    padding: 10px;
  }

  .lock-img {
    width: 100px;
  }

  .title {
    font-size: 30px;
  }

  .login-container {
    width: 80%;
    padding: 20px;
  }

  .login-group input {
    font-size: 14px;
  }

  .signup a {
    font-size: 16px;
  }

  .login-btn {
    font-size: 16px;
  }
}

@media (max-width: 480px) {
  .lock-img {
    width: 80px;
  }

  .title {
    font-size: 24px;
  }

  .login-container {
    padding: 10px;
  }

  .login-group input {
    font-size: 14px;
    padding: 10px 20px 10px 40px;
  }

  .signup a {
    font-size: 14px;
  }

  .login-btn {
    font-size: 14px;
  }

  .login-group img {
    width: 20px;
  }
}
</style>
