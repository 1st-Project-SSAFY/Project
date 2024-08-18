<template>
  <div class="container">
    <div class="sidebar">
      <ul class="robots">
        <li
          class="robot"
          v-for="(robot, index) in floorInfo?.robot_info || []"
          :key="index"
          @click="() => selectRobot(index)"
          :class="{ 'selected': selectedRobotIndex === index }"
        >
          {{ robot.robot_id }}
        </li>
      </ul>
    </div>
    <div class="main-content">
      <button class="main-btn btn btn-light" @click="goToDetail">건물 메인</button>
      <h2 class="floor-info">{{ floorIndex }}층 로봇 정보</h2>
      <div class="robot-container" v-if="selectedRobot">
        <h2>{{ selectedRobot.robot_id }}</h2>
        <ul class="robot-status">
          <li class="robot-detail" v-for="(value, key) in filteredRobotDetails" :key="key">
            <span class="status-title">{{ formatKey(key) }}</span>
            <span class="status-item">{{ value }}</span>
          </li>
        </ul>
        <button class="unregister-btn">등록 해제</button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed, onUnmounted } from 'vue';
import { useRoute } from 'vue-router';
import { useUserStore } from '@/stores/user';
import axios from 'axios';
import router from '@/router/index';

const store = useUserStore();
const route = useRoute();

const buildingId = route.params.building_id;
const floorIndex = route.params.floor_index;
// const robotIndex = route.params.robot_index;

const floorInfo = ref(null); 
const selectedRobotIndex = ref(null);

onMounted(() => {
  axios({
    method: 'get',
    url: store.API_URL + `buildings/check-building/${buildingId}/${floorIndex}/`,
    headers: {
      'Authorization': `Token ${store.token}`,
    }
  })
  .then((response) => {
    floorInfo.value = response.data;
    console.log(floorInfo.value);
  })
  .catch((error) => {
    console.error("Error loading floor info:", error);
  });
  connectToSSE();
});

const goToDetail = () => {
  router.push({ name: 'building-detail', params: { building_id:buildingId}});
};

const selectedRobot = computed(() => {
  return floorInfo.value?.robot_info?.[selectedRobotIndex.value] || null;
});

const filteredRobotDetails = computed(() => {
  if (!selectedRobot.value) return [];
  const details = { ...selectedRobot.value };
  delete details.robot_id;
  return details;
});

const selectRobot = (index) => {
  selectedRobotIndex.value = index;
  const robotId = floorInfo.value.robot_info[index].robot_id;
  
  router.push({
    path: `/buildings/check-building/${buildingId}/${floorIndex}/${robotId}`
  });

  axios({
    method: 'get',
    url: store.API_URL + `fireissues/robot-state/${buildingId}/${floorIndex}/`,
    headers: {
      'Authorization': `Token ${store.token}`,
    }
  }).then((response) =>{
    console.log(response.data);
  }).catch((error) => {
    console.log(error.message);
  });
};

const formatKey = (key) => {
  switch (key) {
    case 'battery':
      return '배터리 잔량';
    case 'guide_liquid':
      return '형광 용액 잔량';
    case 'location_x':
      return '로봇 x좌표';
    case 'location_y':
      return '로봇 y좌표';
    case 'right':
      return '정상 작동 여부';
    case 'mission':
      return '활성화 여부';
    default:
      return key;
  }
};

let eventSource = null

const connectToSSE = () => {
  eventSource = new EventSource(`${store.API_URL}fireissues/robot-state/${buildingId}/${floorIndex}/`, {
    withCredentials: true,
    headers: {
      Authorization: `Token ${store.token}`,
    },
  });

  eventSource.onopen = (event) => {
    console.log('SSE floor connection opened:', event);
  };
  
  eventSource.onmessage = (event) => {
    try {
      console.log(event)
      const SSEData = JSON.parse(event.data)

      const robotToUpdate = floorInfo.value.robot_info.find(
        (robot) => robot.robot_id === SSEData.robot_id)

        if (robotToUpdate) {
        robotToUpdate.battery = SSEData.info.battery;
        robotToUpdate.guide_liquid = SSEData.info.guide_liquid;
        robotToUpdate.right = SSEData.info.right;
        robotToUpdate.mission = SSEData.info.mission;
        robotToUpdate.location_x = SSEData.info.location_x;
        robotToUpdate.location_y = SSEData.info.location_y;
        console.log(`Updated floor ${SSEData.value.floor} data:`, robotToUpdate);
      } else {
        console.warn(`Floor ${SSEData.value.floor} not found in building data`);
      }

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

});

onUnmounted(() => {
  if (eventSource) {
    eventSource.close();
    console.log('SSE connection closed');
  }
});


</script>

<style scoped>
.container {
  margin: 0;
  height: 100vh;
  width: 100vw;
  display: flex;
  flex-direction: row;
}

.sidebar {
  overflow-y: auto;
  display: flex;
  flex-direction: column;
  align-items: center;
  border-right: 1px solid #ccc;
  padding: 20px;
  width: 20%;
  background-color: #f9f9f9;
  box-sizing: border-box;
}

.main-content {
  width: 100%;
  justify-content: center;
  align-items: center;
}

.floor-info {
  margin: 30px;
  align-self: center;
}

.robots {
  list-style: none;
  padding: 0;
  margin: 0;
  width: 100%;
}

.robot {
  font-size: 18px;
  color: #333;
  margin: 5px 0;
  padding: 10px;
  cursor: pointer;
  border-radius: 5px;
  transition: background 0.3s;
  text-align: center;
}

.robot:hover {
  background-color: #e0e0e0;
}

.robot.selected {
  background-color: #d3d3d3;
}

.robot-container {
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  padding: 20px;
  background: white;
  flex-grow: 1;
  margin: 20px;
  border: 1px solid black;
  border-radius: 15px;
}

.robot-status {
  display: flex;
  flex-direction: column;
  align-items: center;
  width: 100%;
  padding: 20px;
  margin: 20px 0;
  gap: 30px;
  box-sizing: border-box;
}

.robot-detail {
  display: flex;
  justify-content: space-between;
  align-items: center;
  width: 100%;
  padding: 5px 0;
  border-bottom: 1px solid #ccc;
}

.status-title, .status-item {
  font-size: 24px;
}

.status-title {
  font-weight: 600;
}

.unregister-btn {
  background-color: #454545;
  color: white;
  font-size: 16px;
  border: none;
  padding: 10px 20px;
  border-radius: 15px;
  cursor: pointer;
  margin: 10px;
  margin-left: auto;
}

.unregister-btn:hover {
  background-color: #333;
}

@media (max-width: 768px) {
  .container {
    flex-direction: column;
  }

  .robot-status {
    font-size: 18px;
  }

  .status-title, .status-item {
    font-size: 18px;
  }

  .unregister-btn {
    font-size: 12px;
  }
}
</style>
