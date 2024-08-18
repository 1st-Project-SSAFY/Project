<template>
  <div class="container">
    <div class="sidebar">
      <ul class="robots">
        <li
          class="robot"
          v-for="(robot, index) in robots"
          :key="index"
          @click="selectRobot(index)"
          :class="{ 'selected': selectedRobotIndex === index }"
        >
          {{ robot.id }}
        </li>
      </ul>
    </div>
    <div class="main-content" v-if="selectedRobot">
      <h1>{{ selectedRobot.id }}</h1>
      <ul class="robot-status">
        <li class="robot-detail" v-for="(value, key) in filteredRobotDetails" :key="key">
          <span class="status-title">{{ formatKey(key) }}</span>
          <span class="status-item">{{ value }}</span>
        </li>
      </ul>
      <button class="unregister-btn">등록 해제</button>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      robots: [
        { id: 'R0052148', submit_date: '2022.09.19', charge_state: 'Y', battery_level: '89%', light_gas_level: '100%', fault_yn: 'N', active_yn: 'N', location: '3층 2번 충전기' },
        { id: 'R0052149', submit_date: '2022.09.20', charge_state: 'Y', battery_level: '56%', light_gas_level: '0%', fault_yn: 'N', active_yn: 'N', location: '3층 4번 충전기' },
        { id: 'R0052150', submit_date: '2022.09.21', charge_state: 'Y', battery_level: '11%', light_gas_level: '100%', fault_yn: 'N', active_yn: 'N', location: '3층 1번 충전기' },
        { id: 'R0052151', submit_date: '2022.09.22', charge_state: 'Y', battery_level: '94%', light_gas_level: '100%', fault_yn: 'N', active_yn: 'N', location: '3층 3번 충전기' },
        { id: 'R0052152', submit_date: '2022.09.23', charge_state: 'Y', battery_level: '100%', light_gas_level: '50%', fault_yn: 'N', active_yn: 'N', location: '3층 5번 충전기' },
        { id: 'R0052152', submit_date: '2022.09.23', charge_state: 'Y', battery_level: '100%', light_gas_level: '50%', fault_yn: 'N', active_yn: 'N', location: '3층 5번 충전기' },
        { id: 'R0052152', submit_date: '2022.09.23', charge_state: 'Y', battery_level: '100%', light_gas_level: '50%', fault_yn: 'N', active_yn: 'N', location: '3층 5번 충전기' },
        { id: 'R0052152', submit_date: '2022.09.23', charge_state: 'Y', battery_level: '100%', light_gas_level: '50%', fault_yn: 'N', active_yn: 'N', location: '3층 5번 충전기' },
        { id: 'R0052152', submit_date: '2022.09.23', charge_state: 'Y', battery_level: '100%', light_gas_level: '50%', fault_yn: 'N', active_yn: 'N', location: '3층 5번 충전기' },
        { id: 'R0052152', submit_date: '2022.09.23', charge_state: 'Y', battery_level: '100%', light_gas_level: '50%', fault_yn: 'N', active_yn: 'N', location: '3층 5번 충전기' },
        { id: 'R0052152', submit_date: '2022.09.23', charge_state: 'Y', battery_level: '100%', light_gas_level: '50%', fault_yn: 'N', active_yn: 'N', location: '3층 5번 충전기' },
        { id: 'R0052152', submit_date: '2022.09.23', charge_state: 'Y', battery_level: '100%', light_gas_level: '50%', fault_yn: 'N', active_yn: 'N', location: '3층 5번 충전기' },
        { id: 'R0052152', submit_date: '2022.09.23', charge_state: 'Y', battery_level: '100%', light_gas_level: '50%', fault_yn: 'N', active_yn: 'N', location: '3층 5번 충전기' },
        // 로봇 데이터 추가
      ],
      selectedRobotIndex: null,
    };
  },
  computed: {
    selectedRobot() {
      return this.robots[this.selectedRobotIndex] || null;
    },
    filteredRobotDetails() {
      if (!this.selectedRobot) return [];
      const details = { ...this.selectedRobot };
      delete details.id;
      return details;
    }
  },
  methods: {
    selectRobot(index) {
      this.selectedRobotIndex = index;
    },
    formatKey(key) {
      switch (key) {
        case 'id':
          return '로봇 ID';
        case 'submit_date':
          return '등록일';
        case 'charge_state':
          return '충전 상태';
        case 'battery_level':
          return '배터리 잔량';
        case 'light_gas_level':
          return '형광 용액 잔량';
        case 'fault_yn':
          return '고장 여부';
        case 'active_yn':
          return '활성화 여부';
        case 'location':
          return '로봇 위치';
        default:
          return key;
      }
    }
  }
}
</script>

<style scoped>
.container {
  height: 100%;
  display: flex;
  flex-direction: column;
}

.sidebar {
  overflow-y: auto;
  display: flex;
  flex-direction: column;
  align-items: center;
  border-right: 1px solid #ccc;
  padding: 20px;
  width: 100%;
  background-color: #f9f9f9;
  box-sizing: border-box;
  min-height: 200px;
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

.main-content {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 20px;
  background: white;
  flex-grow: 1;
  margin: 50px;
  border: 1px solid black;
  border-radius: 15px;
  box-sizing: border-box;
  width: 100%;
}

.robot-status {
  display: flex;
  flex-direction: column;
  align-items: center;
  align-content: center;
  justify-content: center;
  width: 100%;
  padding: 20px;
  margin: 20px;
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
  margin: 10px 10px;
  margin-left: auto;
}

.unregister-btn:hover {
  background-color: #333;
}

@media (min-width: 768px) {
  .container {
    flex-direction: row;
    justify-content: space-between;
  }

  .sidebar {
    width: 20%;
    min-height: 200px;
  }

  .main-content {
    width: 75%;
  }
}

@media (max-width: 767px) {
  .container {
    flex-direction: column;
  }

  .sidebar, .main-content {
    width: 100%;
  }

  .main-content {
    margin: 20px 0;
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
