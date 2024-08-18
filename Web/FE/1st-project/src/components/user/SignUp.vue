<template>
  <div class="container">
    <form class="signup-form" @submit.prevent>
      <div class="signup-header">
        <h1 class="signup-title">신규 소방관 등록</h1>
        <h3 class="signup-subtitle">신규로 등록하기 위한 정보를 입력해주세요</h3>
      </div>
      <div class="form-group">
        <div class="form-item">
          <label class="form-item-label" for="userName">이름</label>
          <input 
          class="form-item-input" 
          type="text" 
          v-model.trim="userName"
          placeholder="이름을 입력해주세요" />
        </div>
        <div class="form-item">
          <label class="form-item-label" for="fighterNumber">소방관 번호</label>
          <input 
          class="form-item-input" 
          v-model.trim="fighterNumber"
          type="text"
          placeholder="소방관 번호 입력(7자리)" />
        </div>
        <div class="form-item">
          <label class="form-item-label">소속</label>
          <div class="form-item-static">{{ firestation }}</div>
        </div>
        <div class="form-item">
          <label class="form-item-label">담당 업무</label>
          <div class="form-item-static">{{ duty }}</div>
        </div>
      </div>
      <div class="button-group">
        <p class="error-msg">{{ errorMsg }}</p>
        <button v-if="!isVerified" class="signup-button" @click="checkFirefighter">본인 확인</button>
        <button v-if="isVerified" class="signup-button" type="button" @click="signUp">직원 등록</button>
        <router-link class="login-btn" :to="{ name: 'login' }" >로그인 이동</router-link>
      </div>
    </form>
  </div>
</template>

<script setup>
import { useUserStore } from '@/stores/user';
import { ref } from 'vue';

const store = useUserStore();
const userName = ref('');
const fighterNumber = ref('');
const duty = ref('');
const firestation = ref('');
const errorMsg = ref('');
const isVerified = ref('');

const checkFirefighter =  () => {
  const payload = {
    name: userName.value,
    number: fighterNumber.value,
  }

  const refs = {
    duty, firestation, errorMsg, isVerified
  }

  store.checkFireFighter(payload, refs)
}

const signUp = () => {
  const payload = {
    name: userName.value,
    number: fighterNumber.value,
  }
  
  store.signUp(payload)
}
</script>

<style scoped>
.container {
  min-height: 100vh;
  width: 100%;
  padding-top: 40px;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
}

.signup-header {
  align-self: center;
}

.signup-title {
  color: #c2191a;
  font-size: 35px;
  font-weight: bold;
  /* margin-bottom: 40px; */
}

.signup-subtitle {
  color: black;
  font-size: 16px;
  margin-top: 10px;
  margin-bottom: 30px;
}

.signup-form {
  width: 90%;
  max-width: 1000px;
  background: white;
  border-radius: 15px;
  border: 1px solid #ccc;
  padding: 40px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  margin: 30px auto;
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.form-item {
  display: flex;
  flex-direction: column;
  margin-bottom: 10px;
}

.form-item-label {
  font-size: 20px;
  font-weight: 600;
  color: black;
  margin-bottom: 8px;
}

.form-item-input {
  width: 100%;
  height: 48px;
  box-sizing: border-box;
  margin-top: 10px;
  padding: 12px;
  border-radius: 10px;
  border: 1px solid #ccc;
  font-size: 16px;
  font-weight: 400;
  color: #333;
  outline: none;
  transition: border-color 0.3s;
}

.form-item-input::placeholder {
  color: #b1b1b1;
}

.form-item-input:focus {
  border-color: #c2191a;
}

.form-item-static {
  padding: 10px 15px;
  margin-bottom: 10px;
  border-radius: 8px;
  font-size: 16px;
  font-weight: 400;
  color: #333;
}

.button-group {
  display: flex;
  flex-direction: column;
  align-items: flex-end;
  margin-top: 20px;
}

.error-msg {
  align-self: flex-end;
  color: #FF2222;
}

.login-btn {
  margin-left: auto;
  /* margin-right: 1%; */
  margin-top: 2%;
}

.signup-button {
  align-self: flex-end;
  width: 30%;
  max-width: 200px;
  height: 50px;
  background: #454545;
  border-radius: 15px;
  color: white;
  font-size: 17px;
  font-weight: 500;
  text-align: center;
  cursor: pointer;
  border: none;
  transition: background-color 0.3s;
}

.signup-button:hover {
  background: #333;
}

@media (max-width: 768px) {
  .signup-title {
    font-size: 28px;
  }

  .signup-subtitle {
    font-size: 14px;
  }

  .signup-form {
    width: 80%;
    padding: 30px;
  }
}

@media (max-width: 480px) {
  .signup-title {
    font-size: 24px;
  }

  .signup-subtitle {
    font-size: 12px;
  }

  .signup-button {
    font-size: 20px;
  }
}
</style>