<template>
  <div v-if="floordetail && floordetail.floor_info" class="content">
    <button class="main-btn btn btn-light" @click="goToDetail">건물 메인</button>
    <h1>{{ floordetail.floor_info.floor < 0 ? `지하${Math.abs(floordetail.floor_info.floor)}`: floordetail.floor_info.floor }}층 상세</h1>
    <div class="floordetail">
      <p>{{ floordetail.floor_info.etc ? floordetail.floor_info.etc : '특이사항 없음' }}</p>
    </div>
    <div class="image-container">
      <img class="floor-image" :src=floordetail.floor_info.img alt="">
      <div
        class="robot-detail"
        v-for="robot in floordetail.robot_info"
        :key="robot.robot_id"
        @click="selectRobot(robot)"
        :style="robotStyle(robot.location_x, robot.location_y, robot.right)">
      </div>
      <div
        v-for="(point, index) in robotRoute"
        :key="index"
        :style="pointStyle(point)">
      </div>
      <div
        v-for="sprinkler in floorDetail.sprinkler_info"
        :key="sprinkler.sprinkler_id"
        :style="sprinklerStyle(sprinkler.sprinkler_x, sprinkler.sprinkler_y)"
        >
      </div>
    </div>
    <div v-if="selectedRobot" class="action-buttons">
      <button type="button" class="btn btn-success" @click="showRobotDetail">로봇 상세</button>
      <!-- <button type="button" class="btn btn-danger" @click="showFireSituation">화재 상황</button> -->
    </div>

    <div v-if="isLoading" class="spinner-border text-danger loading" role="status"></div>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted, defineProps, computed } from 'vue';
import router from '@/router/index';
import { useRoute } from 'vue-router';
import { useUserStore } from '@/stores/user/';
import { useFireStore } from '@/stores/fire';
const store = useUserStore();
const fire = useFireStore();
const route = useRoute();

const props = defineProps({
  floordetail: Object,
});

const floorDetail = computed(() => props.floordetail);

const buildingId = route.params.building_id;
const floorIndex = 10;

const selectedRobot = ref(null);
const isLoading = ref(false);

const selectRobot = (robot) => {
  selectedRobot.value = robot;
};

// const showFireSituation = () => {
//   console.log('화재 상황 버튼 클릭');
//   router.push({ name: 'fire-communication'});
// };

const showRobotDetail = () => {
  if (selectedRobot.value) {
    router.push({ name: 'robot-detail', params: { buildingId, floor_index: floorIndex, robot_index: selectedRobot.value.pk } });
  }
};

const goToDetail = () => {
  router.push({ name: 'building-detail', params: { building_id:buildingId}});
};

const robotStyle = (x, y, right) => {
  return {
    position: 'absolute',
    top: `${x*25+10}px`, 
    left: `${y*25}px`, 
    width: '20px',
    height: '20px',
    backgroundColor: right ? 'green' : 'red',
  };
};

const pointStyle = (point) => {
  return {
    position: 'absolute',
    top: `${point[0]*25 + 10}px`,
    left: `${point[1]*25}px`,
    width: '20px',
    height: '20px',
    backgroundColor: '#fefd48',
    borderRadius: '50%',
  };
};

const sprinklerStyle = (x, y) => {
  return {
    position: 'absolute',
    top: `${x * 25 + 10}px`,
    left: `${y * 25}px`,
    width: '15px',
    height: '15px',
    backgroundColor: 'blue',
    borderRadius: '50%',
    animation: 'pulse 1s infinite',
  };
};

const styles = `
@keyframes pulse {
  0%, 100% {
    transform: scale(1);
  }
  50% {
    transform: scale(1.5); /* 크기를 1.5배로 증가 */
  }
}
`;

const styleSheet = document.createElement("style");
styleSheet.type = "text/css";
styleSheet.innerText = styles;
document.head.appendChild(styleSheet);

// SSE 연결
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
      const SSEData = JSON.parse(event.data);
      console.log(SSEData);
      console.log('floorDetail', floorDetail.value)
      // console.log(SSEData.)

      if (floorDetail.value.robot_info) {
        const robotToUpdate = floorDetail.value.robot_info.find(
          (robot) => robot.robot_id === SSEData.robot_id
        );

        if (robotToUpdate) {
          robotToUpdate.battery = SSEData.info.battery;
          robotToUpdate.guide_liquid = SSEData.info.guide_liquid;
          robotToUpdate.right = SSEData.info.right;
          robotToUpdate.mission = SSEData.info.mission;
          robotToUpdate.location_x = SSEData.info.location_x;
          robotToUpdate.location_y = SSEData.info.location_y;
          console.log(`Updated floor` );
          console.log(floorDetail.value)
        } else {
          console.warn(`Floor ${SSEData.value.floor} not found in building data`);
        }
      } else {
        console.warn('floorDetail or robot_info is not defined.');
      }
    } catch (error) {
      console.error(' error:', error);
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

let eventSource2 = null
const robotRoute = ref(fire.robotRoute ? fire.robotRoute : [])
// const robotRoute = ref([]);
const findRoute = () => {
  eventSource2 = new EventSource(`${store.API_URL}buildings/robot-escape/${buildingId}/${floorIndex}/`, {
    withCredentials: true,
    headers: {
      Authorization: `Token ${store.token}`,
    },
  });

  eventSource2.onopen = (event) => {
    console.log('SSE route connection opened:', event);
  };
  
  eventSource2.onmessage = (event) => {
    try {
      console.log('robot-escape')
      robotRoute.value = JSON.parse(event.data)
      console.log('route : ', robotRoute.value)
      fire.robotRoute = JSON.parse(event.data)

    } catch (error) {
      console.error('JSON parsing error:', error);
    }
  };

  eventSource2.addEventListener('ping', (event) => {
    console.log('Ping event received:', event.data);
  });

  eventSource2.onerror = (error) => {
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
  findRoute()
});

onUnmounted(() => {
  if (eventSource) {
    eventSource.close();
    console.log('floor connection closed');
  }
  if (eventSource2) {
    eventSource.close();
    console.log('route connection closed');
  }
});

</script>

<style lang="scss" scoped>
.content {
  display: flex;
  flex-direction: column;
  height: 100vh;
  position: relative;
  padding: 20px;
  box-sizing: border-box;
  overflow: auto;
}

.image-container {
  flex-grow: 1;
  display: flex;
  justify-content: center;
  align-items: center;
  box-sizing: border-box;
  width: 700px;
  height: 550px;
  max-height: 550px;
  // width: 100%;
  // height: 100%;
  overflow: auto;
  background-color: #f0f0f0;
  position: relative;
}

.floor-image {
  object-fit: contain;
  max-width: 100%;
  max-height: 100%;
}


.floordetail {
  align-content: center;
  justify-content: center;
}

.main-btn {
  margin-right: auto;
  margin-bottom: 10px;
}

.robot-detail {
  cursor: pointer;
  z-index: 10;
}

.action-buttons {
  display: flex;
  flex-direction: column;
  align-items: center;
  margin-top: 20px;
}

.action-buttons button {
  margin: 5px;
}

.loading {
  text-align: center;
  font-size: 24px;
  color: #000;
}
</style>
