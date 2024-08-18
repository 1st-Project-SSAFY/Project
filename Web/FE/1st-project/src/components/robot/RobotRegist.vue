<template>
  <div class="container">
    <div class="content">
      <form class="input-form">
        <div class="input-group">
          <label>로봇 아이디</label>
          <input type="text" placeholder=" ex) R1803972">
        </div>
        <div class="input-group">
          <label>건물 이름</label>
          <input type="text" placeholder="ex) 멀티캠퍼스">
        </div>
        <div class="input-group">
          <label>건물 아이디</label>
          <input type="text" placeholder="ex) 123984">
        </div>
        <div class="input-group">
          <label>보관 장소</label>
          <div class="regist-content">
            <div>
              <select name="floors" id="floors">
                <option value="" selected disabled hidden>층</option>
                <option value="1">1층</option>
                <option value="2">2층</option>
                <option value="3">3층</option>
              </select>
            </div>
            <div>
              <select id="chargers" class="chargers">
                <option value="" selected disabled hidden>충전기 번호</option>
                <option value="1">1번</option>
                <option value="2">2번</option>
                <option value="3">3번</option>
                <option value="4">4번</option>
              </select>
            </div>
          </div>
        </div>
        <div class="register-btn">
          <button>등록</button>
        </div>
      </form>
    </div>
  </div>
</template>

<script setup>
</script>

<style scoped>
.container {
  display: flex;
  flex-direction: column;
  min-height: 100vh;
}

.content {
  flex-grow: 1;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  padding: 40px 20px;
}

.input-form {
  width: 100%;
  max-width: 1000px;
  margin-bottom: 20px;
  border: 1px solid rgba(0, 0, 0, 0.507);
  padding: 100px;
  padding-bottom: 50px;
  border-radius: 10px;
  box-sizing: border-box;
}

.input-group {
  margin-bottom: 20px;
  width: 100%;
}

.input-group label {
  display: block;
  font-size: 24px;
  color: #C2191A;
  margin-bottom: 10px;
  font-style: bold;
}

.input-group input {
  text-align: right;
  width: 100%;
  height: 50px;
  font-size: 18px;
  padding: 10px;
  border: none;
  border-radius: 10px;
  box-sizing: border-box;
}

.regist-content {
  display: flex;
  justify-content: space-between;
  gap: 20px;
}

.regist-content div {
  width: 48%;
}

.regist-content select {
  width: 100%;
  height: 50px;
  font-size: 18px;
  padding: 10px;
  border: none;
  border-radius: 10px;
  box-sizing: border-box;
}

.register-btn {
  display: flex;
  justify-content: center;
  margin-top: 40px;
}

.register-btn button {
  width: 100%;
  max-width: 250px;
  height: 60px;
  margin-top: 80px;
  background: #454545;
  border-radius: 15px;
  color: white;
  font-size: 20px;
  cursor: pointer;
}

@media (max-width: 768px) {
  .content {
    padding: 20px;
  }

  .input-form {
    padding: 40px;
  }

  .input-group label {
    font-size: 20px;
  }

  .input-group input,
  .regist-content select {
    height: 40px;
    font-size: 16px;
  }

  .regist-content {
    flex-direction: column;
    gap: 20px;
  }

  .regist-content div {
    width: 100%;
    margin-bottom: 20px;
  }

  .register-btn button {
    height: 50px;
    font-size: 20px;
  }
}

@media (max-width: 480px) {
  .input-form {
    padding: 20px;
  }

  .input-group label {
    font-size: 18px;
  }

  .input-group input,
  .regist-content select {
    height: 36px;
    font-size: 14px;
  }

  .register-btn button {
    height: 40px;
    font-size: 18px;
  }
}
</style>
