<template>
  <div class="building-info">
    <h1>건물상세</h1>
  </div>
  <div class="image">
    <img src="@/assets/multicampus.png" alt="building_img">
  </div>
  <div class="building-details">
    <p>건물명 : {{ building.building?.building_name }}</p>
    <p>주소 : {{ building.building?.address }}</p>
    <p>최고 층수 : {{ building.building?.max_floor }}층</p>
    <p>최저 층수 : {{ building.building?.min_floor > 0 ? building.building?.min_floor + '층' : '지하 ' + Math.abs(building.building?.min_floor) + '층' }}</p>
    <p>정상 로봇 수  : {{ rightTotal }}</p>
    <p>고장 로봇 수 : {{ wrongTotal }}</p>
    <button class="regist-btn" @click="checkManager">관리자 등록</button>
    <button type="button" class="btn btn-danger mt-2 modal-btn" data-bs-toggle="modal" data-bs-target="#fireReportModal" v-if="isfire">
      화재 기록
    </button>
  </div>
  <!-- Modal -->
  <div class="modal fade" id="fireReportModal" tabindex="-1" aria-labelledby="exampleModalLabel" aria-hidden="true">
    <div class="modal-dialog">
      <div class="modal-content">
        <div class="modal-header">
          <h2 class="modal-title fs-5 mt-2" id="exampleModalLabel">화재 기록</h2>
          <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
        </div>
        <div class="modal-body">
          <form @submit.prevent="submitFireRecord">
            <div class="form-group">
              화재 발생 건물: {{ building.building.building_name }}
            </div>
            <div class="form-group">
              <label for="extinguishDateTime" class="form-label">화재 진압 일시:</label> 
              <input type="datetime-local" class="form-control" id="extinguishDateTime" v-model="extinguishDateTime" @change="formatDate" required/>
            </div>
            <div class="form-group">
              <label for="fireDescription" class="form-label mt-2">화재 수준: </label>
              <select class="form-select" name="intensity" id="intensity" v-model="fireIntensity" required>
                <option value="" disabled selected>1~10 선택해주세요</option>
                <option value="1" selected>1</option>
                <option value="2">2</option>
                <option value="3">3</option>
                <option value="4">4</option>
                <option value="5">5</option>
                <option value="6">6</option>
                <option value="7">7</option>
                <option value="8">8</option>
                <option value="9">9</option>
                <option value="10">10</option>
              </select>
            </div>
            <div class="mb-3">
              <label for="fireDescription" class="form-label">세부내용</label>
              <textarea class="form-control" id="fireDescription" rows="3" v-model="fireDescription" required></textarea>
            </div>
          </form>
        </div>
        <div class="modal-footer">
          <button type="button" class="btn btn-danger" @click="submitFireRecord">기록 저장</button>
          <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">닫기</button>
        </div>
      </div>
    </div>
  </div>  
</template>

<script setup>
import { ref, computed, defineProps, onMounted, onUnmounted } from 'vue';
import { useUserStore } from '@/stores/user/';
import { useRoute } from 'vue-router';
import Swal from 'sweetalert2';
import axios from 'axios';
import { useFireStore } from '@/stores/fire';

const store = useUserStore();
const route = useRoute();
const fire = useFireStore();
const props = defineProps({
  building: Object,
});

const building = ref(props.building);
const buildingId = route.params.building_id;
const status = ref(null);
const manigerInfo = ref(null);
const registMsg = ref(null);

// record data
const fireDescription = ref('');
const fireIntensity = ref('')
const extinguishDateTime = ref('')

const rightTotal = computed(() => {
  if (!building.value || !building.value.robot) return 0;
  return building.value.robot.reduce((total, floor) => total + floor.right, 0);
});

const wrongTotal = computed(() => {
  if (!building.value || !building.value.robot) return 0;
  return building.value.robot.reduce((total, floor) => total + floor.wrong, 0);
});

const isfire = computed(() => {
  return building.value.robot.some(robot => robot.fire);
})

const checkManager = () => {
  axios({
    method: 'get',
    url: `${store.API_URL}buildings/check-building/${buildingId}/register-manager/`,
    headers: {
      Authorization: `Token ${store.token}`,
    }
    }).then((response) => {
      console.log(response.data)
      status.value = response.data.status;
      registMsg.value = response.data.message;
      manigerInfo.value = response.data.manager;

      if (response.data.status === 0) {
        console.log('success')
        notExistedManager();

      } else {
        existedManager();
      }
  })
}

const notExistedManager = () => {
  Swal.fire({
    title: '관리자 등록',
    icon: 'info',
    html: `${registMsg.value.replace(/\n/g, '<br>')}`,
    confirmButtonText: "확인",
    showCancelButton: true,
    cancelButtonText: "취소"
  }).then((result) => {
    if(result.isConfirmed) {
      axios({
        method: 'post',
        url: `${store.API_URL}buildings/check-building/${buildingId}/register-manager/`,
        headers: {
          Authorization: `Token ${store.token}`,
        },
        data: {
          id: manigerInfo.value.id,
          pw: manigerInfo.value.pw
        }
      }).then(() => {
        Swal.fire({
          title: `등록 완료`,
          html: `등록이 완료되었습니다.<br><br> ID : ${manigerInfo.value.id} <br> Password : ${manigerInfo.value.pw}`,
          icon: "success",
        })
      })
    }
  })
}

const existedManager = () => {
  Swal.fire({
    title: '관리자 등록',
    icon: 'error',
    html: `${registMsg.value.replace(/\n/g, '<br>')}`,
    confirmButtonText: "확인"
  })
}

let eventSource = null
const robotDetail = ref([])

const connectToSSE = () => {
  eventSource = new EventSource(`${store.API_URL}fireissues/robot-state/${buildingId}/`, {
    withCredentials: true,
    headers: {
      Authorization: `Token ${store.token}`,
    },
  });

  eventSource.onopen = (event) => {
    console.log('SSE buildingdetail connection opened:', event);
  };

  eventSource.onmessage = (event) => {
    try {
      robotDetail.value = JSON.parse(event.data);
      console.log(event.data)

    const robotToUpdate = building.value.robot.find(
      (robot) => robot.robot_id === robotDetail.value.robot_id)

    if (robotToUpdate) {
      robotToUpdate.wrong = robotDetail.value.wrong
      robotToUpdate.right = robotDetail.value.right
    } else {
      console.warn(`Floor ${robotDetail.value.floor} not found in building data`);
    }
    } catch (error) {
      console.log('JSON parsing error:', error);
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

// modal
const formatDate = () => {
  extinguishDateTime.value = extinguishDateTime.value.replace('T', ' ');
}

const submitFireRecord = () => {
  if (!extinguishDateTime.value || !fireIntensity.value || !fireDescription.value) {
    alert('모든 값을 입력해주세요.');
    return;
  }
  axios({
    method: 'patch',
    url: `${store.API_URL}buildings/check-building/${buildingId}/record/`,
    headers: {
      Authorization: `Token ${store.token}`,
    },
    data: {
      end_dt: extinguishDateTime.value,
      fire_scale: fireIntensity.value,
      detail: fireDescription.value
    }
  }).then(() => {
    fire.robotRoute = []
    Swal.fire('성공', '화재 기록이 저장되었습니다.', 'success');

  }).catch(() => {
    Swal.fire('오류', '화재 기록 저장 중 문제가 발생했습니다.', 'error');
  });
};

onMounted(() => {
  connectToSSE();
})

onUnmounted(() => {
  if (eventSource) {
    eventSource.close();
    console.log('SSE connection closed');
  }
});
</script>

<style lang="scss" scoped>
.building-info {
  font-size: 40px;
  color: black;
  margin-bottom: 60px 0;
  text-align: center;
}

.image img {
  width: 100%;
  max-width: 870px;
  border-radius: 30px;
  display: block;
  margin: 0 auto 20px;
}

.building-details {
  display: flex;
  flex-direction: column;
  width: 100%;
  max-width: 870px;
  background: white;
  border: 1px solid black;
  border-radius: 30px;
  padding: 20px;
  box-sizing: border-box;
  margin: 0 auto;
}

.regist-btn {
  align-self: flex-end;
  background-color: #454545;
  color: white;
  font-size: 16px;
  border: none;
  padding: 10px 20px;
  border-radius: 10px;
  cursor: pointer;
}

.modal-btn {
  align-self: flex-end;
  color: white;
  font-size: 16px;
  border: none;
  padding: 10px 20px;
  border-radius: 10px;
}

@media (max-width: 768px) {
  .building-info {
    font-size: 30px;
  }

  .building-details {
    padding: 15px;
  }

  .register {
    width: 100%;
    font-size: 14px;
    padding: 10px;
  }
}

@media (max-width: 480px) {
  .building-info {
    font-size: 24px;
  }

  .building-details {
    padding: 10px;
  }

  .register {
    width: 100%;
    font-size: 12px;
    padding: 8px;
  }
}
</style>
