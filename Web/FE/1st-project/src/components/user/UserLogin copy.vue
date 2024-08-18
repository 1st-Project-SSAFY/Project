<template>
  <div class="container">
    <img class="lock-img" src="https://cdn-icons-png.flaticon.com/512/5446/5446336.png" alt="Lock Image">
    <div class="title">관리자 로그인</div>
    <div class="login-container">
      <div class="login-group">
        <img src="@/assets/사람.png" alt="User Icon">
        <input type="text" placeholder="소방관 ID">
      </div>
      <div class="login-group">
        <img src="@/assets/열쇠.png" alt="Key Icon">
        <input type="password" placeholder="Password">
      </div>
      <div class="signup">
        <router-link to="/signup">회원가입</router-link>
      </div>
      <button class="login-btn">LOG IN</button>
    </div>
  </div>
</template>

<script setup>

</script>

<style scoped>
.container {
  display: flex;
  width: 100%;
  max-width: 100%;                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                         
  height: 100vh;
  padding: 20px;
  margin: auto;
  flex-direction: column;
  align-items: center;
	justify-content: center;
  text-align: center;
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
  max-width: 500px;
  padding: 40px;
  background-color: white;
  border-radius: 20px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
}

.login-group {
  position: relative;
  margin-bottom: 20px;
	justify-content: space-between;
}

.login-group input {
  width: calc(100% - 40px); 
  padding: 10px 20px;
  font-size: 16px;
  border-radius: 20px;
  border: 1px solid #ccc;
  box-sizing: border-box;
  outline: none;
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
