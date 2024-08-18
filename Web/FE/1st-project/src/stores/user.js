import { defineStore } from 'pinia';
import axios from 'axios';
import router from '@/router';
import { ref } from 'vue';

export const useUserStore = defineStore('user', () => {
  const API_URL = 'http://3.36.55.201:8000/'; // server
  // const API_URL = 'http://127.0.0.1:8000/'; // local
  const token = ref('');
  const duty = ref('');

  const userBuildingIndex = ref('');
  const IsManager = ref('');

  const checkFireFighter = (payload, refs) => {
    const { name, number } = payload;
    const { duty, firestation, errorMsg, isVerified } = refs;

    duty.value = '';
    firestation.value = '';
    errorMsg.value = '';
    isVerified.value = false;

    axios({
      method: 'get',
      url: API_URL + 'accounts/signup/',
      params: {
        name, number
      },
    }).then((response) => {
      console.log('정보조회 완료');
      if (response.data.data){
        duty.value = response.data.data.duty === 0 ? '현장직' : '관리직';
        firestation.value = response.data.data.firestation;
        isVerified.value = true;
      }
      else {
        errorMsg.value = response.data.error
      }
    }).catch(() => {
      errorMsg.value = '소방관 정보를 찾을 수 없습니다. 입력하신 정보를 확인해주세요';

    });
  };

  const signUp = (payload) => {
    const { name, number } = payload;

    axios({
      method: 'post',
      url: API_URL + 'accounts/signup/',
      data: {
        name, number
      },
    }).then(() => {
      console.log('회원가입 완료')
      router.push({ name: 'login'})
    }).catch((err) =>{
      console.log(err)
    })
  }

  const logIn = (payload) => {
    const { username, password, job } = payload;
    axios({
      method: 'POST',
      url: API_URL + (job == 1 ? 'accounts/login/' : 'accounts/manager-login/'),
      data: {
        username, 
        password
      },
    }).then((res) => {
      // 관리직 1, 현장직 0
      console.log('로그인 완료');
      console.log('data:', res.data)
      token.value = res.data.key;
      if (res.data.duty) {
        duty.value = res.data.duty;
      }
      IsManager.value = false;

      if (duty.value === 1 || duty.value === 0) {
        router.push({ 
          name: 'buildings',
          params: { duty: duty.value }
      });
      } else {
        userBuildingIndex.value = res.data.building_pk;

        IsManager.value = true;
        router.push({ name: 'user-building', params: { 'building_id': userBuildingIndex.value }});
        console.log('관리자 로그인 완료')
        console.log('userBuildingIndex', userBuildingIndex)
      }
    }).catch((err) => {
      console.log('로그인 불가', err.response)
      alert('ID와 비밀번호를 확인해주세요.')
    })
  }

  const logOut = async() => {
    axios({
      method: 'post',
      url: API_URL + (IsManager.value ? 'accounts/manager-logout/' : 'logout/'),
      headers: {
        Authorization: `Token ${token.value}`
      },
    }).then(() => {
      console.log('로그아웃')
      token.value = '';
      duty.value = '';
      router.push({ name: 'login' })
    }).catch((err) => {
      console.log(this.Authorization)
      console.log(err)
    })
  }  

  return { API_URL, checkFireFighter, signUp, logIn, logOut, token };
}, {
  persist: true
});