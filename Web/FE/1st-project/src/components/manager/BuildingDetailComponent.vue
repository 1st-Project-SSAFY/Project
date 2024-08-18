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
  </div>
</template>

<script setup>
import { ref, computed, defineProps, onMounted, onUnmounted } from 'vue';
import { useUserStore } from '@/stores/user/';

const store = useUserStore();
const props = defineProps({
  building: Object,
});

const building = ref(props.building);
const buildingId = store.userBuildingIndex

const rightTotal = computed(() => {
  if (!building.value || !building.value.robot) return 0;
  return building.value.robot.reduce((total, floor) => total + floor.right, 0);
});

const wrongTotal = computed(() => {
  if (!building.value || !building.value.robot) return 0;
  return building.value.robot.reduce((total, floor) => total + floor.wrong, 0);
});

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
