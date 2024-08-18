<template>
  <section class="app">
  <aside class="sidebar">
    <nav class="sidebar-nav">
      <ul>
        <li 
        v-for="(floor, index) in detail.robot" 
        :key="index">
        {{ floor }}
        </li>
      </ul>
    </nav>
  </aside>
</section>
  <div class="content">
    <div class="sidebar"
         :class="{ expanded: isSidebarExpanded }"
         @mouseover="expandSidebar"
         @mouseout="collapseSidebar">
      <ul class="floors">
        <li class="floor"
            v-for="(floor, index) in floors"
            :key="index"
            @mouseover="showFloorInfo(floor, index)"
            @mouseout="clearFloorInfo"
            :class="{ 'active': activeFloor === index }">
          <div class="floor-name">{{ floor.name }}</div>
          <div class="floor-info" v-if="isSidebarExpanded">{{ floor.info }}</div>
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

<script setup>
// import { useUserStore } from '@/stores/user/';
// import { useRoute } from 'vue-router';
// import { ref } from 'vue';
// import axios from 'axios'

// const store = useUserStore();
// const route = useRoute();
// const buildingID = route.params.id;
// const detail = ref([])

// console.log(buildingID)
// axios({
//   method: 'get',
//   url: `${store.API_URL}buildings/check-building/506/`,
//   // url: `${store.API_URL}buildings/check-building/${buildingID}`,
//   headers: {
//     Authorization: `Token ${store.token}`,
//   },
// }).then((response) => {
//   console.log(response.data)
//   detail.value = response.data
// }).catch((error) => {
//   console.error(error);
// })
// export default {
//   data() {
//     return {
//       isSidebarExpanded: false,
//       floors: [
//         { name: "15층", info: "15층 정보" },
//         { name: "14층", info: "14층 정보" },
//         { name: "13층", info: "13층 정보" },
//         { name: "12층", info: "12층 정보" },
//         { name: "11층", info: "11층 정보" },
//         { name: "10층", info: "10층 정보" },
//         { name: "9층", info: "9층 정보" },
//         { name: "8층", info: "8층 정보" },
//         { name: "7층", info: "7층 정보" },
//         { name: "6층", info: "6층 정보" },
//         { name: "5층", info: "5층 정보" }
//       ],
//       activeFloor: null,
//       buildingDetails: "건물정보 : 멀티캠퍼스\n주소 : 서울특별시 강남구 테헤란로 212\n층수 : 20\n정상 로봇 갯수 : 15\n고장 로봇 갯수 : 1"
//     };
//   },
//   methods: {
//     showFloorInfo(floor, index) {
//       this.activeFloor = index;
//       this.buildingDetails = floor.info;
//     },
//     clearFloorInfo() {
//       this.buildingDetails = "건물정보 : 멀티캠퍼스\n주소 : 서울특별시 강남구 테헤란로 212\n층수 : 20\n정상 로봇 갯수 : 15\n고장 로봇 갯수 : 1";
//     },
//     expandSidebar() {
//       this.isSidebarExpanded = true;
//     },
//     collapseSidebar() {
//       this.isSidebarExpanded = false;
//     }
//   }
// };
</script>

<style lang="scss" scoped>
.content {
  display: flex;
  height: 100vh;
  position: relative;
}

.sidebar {
  width: 20%;
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
  width: 35%;
}

.sidebar .floors {
  list-style: none;
  padding: 0;
  margin: 0;
}

.sidebar .floor {
  height: 90px;
  background: white;
  display: flex;
  align-items: center;
  justify-content: space-between;
  box-sizing: border-box;
  font-size: 20px;
  color: black;
  cursor: pointer;
  text-align: center;
  transition: background 0.3s ease;
}

.sidebar .floor .floor-name {
  flex: 0 0 150px;
  height: 100%;
  border: 1px solid black;
  border-radius: 10px;
  box-sizing: border-box;
  text-align: center;
  padding: 0 10px;
  background: white;
}

.sidebar .floor .floor-info {
  flex: 1;
  padding-left: 10px;
  text-align: left;
  display: none;
}

.sidebar.expanded .floor .floor-info {
  display: block;
}

.sidebar .floor.active {
  background: #f0f0f0;
}

.main-content {
  flex-grow: 1;
  padding: 20px;
  box-sizing: border-box;
  margin-left: 20%;
  transition: margin-left 0.3s ease;
}

.sidebar.expanded + .main-content {
  margin-left: 35%;
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
    margin-left: 20%;
  }

  .sidebar.expanded + .main-content {
    margin-left: 35%;
  }
}

.sidebar::-webkit-scrollbar {
  width: 8px;
}

.sidebar::-webkit-scrollbar-track {
  background: white;
}

.sidebar::-webkit-scrollbar-thumb {
  background: #ccc;
  border-radius: 10px;
}

.sidebar::-webkit-scrollbar-thumb:hover {
  background: #aaa;
}
</style>
