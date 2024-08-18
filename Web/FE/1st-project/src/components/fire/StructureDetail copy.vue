<!-- <template>
  <div class="content">
    <div class="sidebar"
         :style="{ width: sidebarWidth + 'rem' }"
         @mouseover="expandSidebar"
         @mouseout="collapseSidebar">
      <ul class="floors">
        <li class="floor"
            v-for="(floor, index) in floors"
            :key="index"
            @mouseover="showFloorInfo(floor.info)"
            @mouseout="clearFloorInfo"
            :class="{ 'active': activeFloor === index }">
          {{ floor.name }}
        </li>
      </ul>
    </div>
    <div class="main-content">
      <div class="building-info">건물상세</div>
      <div class="image">
        <img src="https://via.placeholder.com/870x491" alt="Building Image">
      </div>
      <div class="building-details">
        {{ buildingDetails }}
      </div>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      sidebarWidth: 25, // 초기 사이드바 너비
      isSidebarExpanded: false, // 사이드바 확장 여부
      floors: [
        { name: "15층", info: "15층 정보" },
        { name: "14층", info: "14층 정보" },
        { name: "13층", info: "13층 정보" },
        { name: "12층", info: "12층 정보" },
        { name: "11층", info: "11층 정보" },
        { name: "10층", info: "10층 정보" },
        { name: "9층", info: "9층 정보" }
      ],
      activeFloor: null,
      buildingDetails: "건물정보 : 멀티캠퍼스\n주소 : 서울특별시 강남구 테헤란로 212\n층수 : 20\n정상 로봇 갯수 : 15\n고장 로봇 갯수 : 1"
    };
  },
  methods: {
    showFloorInfo(info) {
      this.buildingDetails = info;
    },
    clearFloorInfo() {
      this.buildingDetails = "건물정보 : 멀티캠퍼스\n주소 : 서울특별시 강남구 테헤란로 212\n층수 : 20\n정상 로봇 갯수 : 15\n고장 로봇 갯수 : 1";
    },
    expandSidebar() {
      this.isSidebarExpanded = true;
      this.sidebarWidth = 800; // 확장할 때 사이드바 너비
    },
    collapseSidebar() {
      this.isSidebarExpanded = false;
      this.sidebarWidth = 100; // 축소할 때 사이드바 너비
    }
  }
};
</script>

<style scoped>
.content {
  display: flex;
  flex-wrap: nowrap;
  height: 100vh;
}

.sidebar {
  width: 100px; /* 초기 사이드바 너비 */
  max-width: 400px; /* 최대 너비 */
  height: calc(100vh - 194px);
  overflow-y: auto;
  border-right: 1px solid #ccc;
  box-sizing: border-box;
  padding: 30px;
  transition: width 0.3s ease; /* 너비 변화 애니메이션 */
}

.sidebar.expanded {
  width: 400px; /* 확장된 사이드바 너비 */
}

.sidebar .floors {
  list-style: none;
  padding: 0;
  margin: 0;
}

.sidebar .floor {
  width: 100%;
  height: 110px;
  background: white;
  border: 1px solid black;
  margin-bottom: 10px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 20px;
  color: black;
  cursor: pointer;
  text-align: center;
  transition: background 0.3s ease;
}

.sidebar .floor.active {
  background: #f0f0f0;
}

.main-content {
  flex-grow: 1;
  padding: 20px;
  box-sizing: border-box;
}

.building-info {
  text-align: center;
  font-size: 40px;
  color: black;
  margin-bottom: 20px;
}

.image img {
  width: 100%;
  max-width: 870px;
  border-radius: 30px;
  display: block;
  margin: 0 auto 20px;
}

.building-details {
  width: 100%;
  max-width: 870px;
  background: white;
  border: 1px solid black;
  border-radius: 30px;
  padding: 20px;
  box-sizing: border-box;
  margin: 0 auto;
}

@media (min-width: 768px) {
  .content {
    flex-wrap: nowrap;
  }

  .sidebar {
    max-width: 400px;
  }

  .main-content {
    margin-left: 20px;
  }
}
</style> -->

<!-- 
<template>
  <div class="content">
    <div class="sidebar"
         :style="{ width: isSidebarExpanded ? '1000px' : '400px' }"
         @mouseover="expandSidebar"
         @mouseout="collapseSidebar">
      <ul class="floors">
        <li class="floor"
            v-for="(floor, index) in floors"
            :key="index"
            @mouseover="showFloorInfo(floor.info)"
            @mouseout="clearFloorInfo"
            :class="{ 'active': activeFloor === index }">
          {{ floor.name }}
        </li>
      </ul>
    </div>
    <div class="main-content">
      <div class="building-info">건물상세</div>
      <div class="image">
        <img src="https://via.placeholder.com/870x491" alt="Building Image">
      </div>
      <div class="building-details">
        {{ buildingDetails }}
      </div>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      isSidebarExpanded: false,
      floors: [
        { name: "15층", info: "15층 정보" },
        { name: "14층", info: "14층 정보" },
        { name: "13층", info: "13층 정보" },
        { name: "12층", info: "12층 정보" },
        { name: "11층", info: "11층 정보" },
        { name: "10층", info: "10층 정보" },
        { name: "9층", info: "9층 정보" }
      ],
      activeFloor: null,
      buildingDetails: "건물정보 : 멀티캠퍼스\n주소 : 서울특별시 강남구 테헤란로 212\n층수 : 20\n정상 로봇 갯수 : 15\n고장 로봇 갯수 : 1"
    };
  },
  methods: {
    showFloorInfo(info) {
      this.buildingDetails = info;
    },
    clearFloorInfo() {
      this.buildingDetails = "건물정보 : 멀티캠퍼스\n주소 : 서울특별시 강남구 테헤란로 212\n층수 : 20\n정상 로봇 갯수 : 15\n고장 로봇 갯수 : 1";
    },
    expandSidebar() {
      this.isSidebarExpanded = true;
    },
    collapseSidebar() {
      this.isSidebarExpanded = false;
    }
  }
};
</script>

<style scoped>
.content {
  display: flex;
  height: 100vh;
}

.sidebar {
  height: calc(100vh - 194px);
  overflow-y: auto;
  border-right: 1px solid #ccc;
  box-sizing: border-box;
  padding: 30px;
  transition: width 0.3s ease;
}

.sidebar .floors {
  list-style: none;
  padding: 0;
  margin: 0;
}

.sidebar .floor {
  width: 100%;
  height: 110px;
  background: white;
  border: 1px solid black;
  margin-bottom: 10px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 20px;
  color: black;
  cursor: pointer;
  text-align: center;
  transition: background 0.3s ease;
}

.sidebar .floor.active {
  background: #f0f0f0;
}

.main-content {
  flex-grow: 1;
  padding: 20px;
  box-sizing: border-box;
}

.building-info {
  text-align: center;
  font-size: 40px;
  color: black;
  margin-bottom: 20px;
}

.image img {
  width: 100%;
  max-width: 870px;
  border-radius: 30px;
  display: block;
  margin: 0 auto 20px;
}

.building-details {
  width: 100%;
  max-width: 870px;
  background: white;
  border: 1px solid black;
  border-radius: 30px;
  padding: 20px;
  box-sizing: border-box;
  margin: 0 auto;
}

@media (min-width: 768px) {
  .content {
    flex-wrap: nowrap;
  }

  .main-content {
    margin-left: 20px;
  }
}
</style> -->

<template>
  <div class="content">
    <div class="sidebar"
         :class="{ expanded: isSidebarExpanded }"
         @mouseover="expandSidebar"
         @mouseout="collapseSidebar">
      <ul class="floors">
        <li class="floor"
            v-for="(floor, index) in floors"
            :key="index"
            @mouseover="showFloorInfo(floor.info)"
            @mouseout="clearFloorInfo"
            :class="{ 'active': activeFloor === index }">
            {{ floor.name }}
            {{ floor.info }}
        </li>
      </ul>
    </div>
    <div class="main-content">
      <div class="building-info">건물상세</div>
      <div class="image">
        <img src="https://via.placeholder.com/870x491" alt="Building Image">
      </div>
      <div class="building-details">
        {{ buildingDetails }}
      </div>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      isSidebarExpanded: false,
      floors: [
        { name: "15층", info: "15층 정보" },
        { name: "14층", info: "14층 정보" },
        { name: "13층", info: "13층 정보" },
        { name: "12층", info: "12층 정보" },
        { name: "11층", info: "11층 정보" },
        { name: "10층", info: "10층 정보" },
        { name: "9층", info: "9층 정보" }
      ],
      activeFloor: null,
      buildingDetails: "건물정보 : 멀티캠퍼스\n주소 : 서울특별시 강남구 테헤란로 212\n층수 : 20\n정상 로봇 갯수 : 15\n고장 로봇 갯수 : 1"
    };
  },
  methods: {
    showFloorInfo(info) {
      this.buildingDetails = info;
    },
    clearFloorInfo() {
      this.buildingDetails = "건물정보 : 멀티캠퍼스\n주소 : 서울특별시 강남구 테헤란로 212\n층수 : 20\n정상 로봇 갯수 : 15\n고장 로봇 갯수 : 1";
    },
    expandSidebar() {
      this.isSidebarExpanded = true;
    },
    collapseSidebar() {
      this.isSidebarExpanded = false;
    }
  }
};
</script>

<style scoped>
.content {
  display: flex;
  height: 100vh;
  position: relative;
}

.sidebar {
  width: 400px;
  height: calc(100vh - 194px);
  overflow-y: auto;
  border-right: 1px solid #ccc;
  box-sizing: border-box;
  padding: 30px;
  position: absolute;
  left: 0;
  top: 0;
  bottom: 0;
  transition: width 0.3s ease;
  background: white;
  z-index: 10;
}

.sidebar.expanded {
  width: 1300px;
}

.sidebar .floors {
  list-style: none;
  padding: 0;
  margin: 0;
}

.sidebar .floor {
  width: 400px;
  height: 110px;
  background: white;
  border: 1px solid black;
  margin-bottom: 10px;
  display: flex;
  align-items: center;
  justify-content: center;
  box-sizing: border-box;
  font-size: 20px;
  color: black;
  cursor: pointer;
  text-align: center;
  transition: background 0.3s ease;
}

.sidebar .floor.active {
  background: #f0f0f0;
}

.main-content {
  flex-grow: 1;
  padding: 20px;
  box-sizing: border-box;
  margin-left: 100px; /* 초기 사이드바 너비 */
  transition: margin-left 0.3s ease;
}

.sidebar.expanded + .main-content {
  margin-left: 600px; /* 확장된 사이드바 너비 */
}

.building-info {
  text-align: center;
  font-size: 40px;
  color: black;
  margin-bottom: 20px;
}

.image img {
  width: 100%;
  max-width: 870px;
  border-radius: 30px;
  display: block;
  margin: 0 auto 20px;
}

.building-details {
  width: 100%;
  max-width: 870px;
  background: white;
  border: 1px solid black;
  border-radius: 30px;
  padding: 20px;
  box-sizing: border-box;
  margin: 0 auto;
}

@media (min-width: 768px) {
  .content {
    flex-wrap: nowrap;
  }

  .main-content {
    margin-left: 100px;
  }

  .sidebar.expanded + .main-content {
    margin-left: 400px;
  }
}
</style>
