<template>
  <!-- bootstrap 사용 -->
  <!-- https://getbootstrap.com/docs/5.3/components/offcanvas/ -->
  <div class="content" v-if="building">
    <div class="sidebar">
      <button class="btn btn-primary" type="button" data-bs-toggle="offcanvas" data-bs-target="#offcanvasScrolling" aria-controls="offcanvasScrolling">층별 정보</button>
      <div class="offcanvas offcanvas-start" data-bs-scroll="true" tabindex="-1" id="offcanvasScrolling" aria-labelledby="offcanvasScrollingLabel">
        <div class="offcanvas-header">
          <h2 class="offcanvas-title" id="offcanvasScrollingLabel">층별 상세 정보</h2>
          <button type="button" class="btn-close" data-bs-dismiss="offcanvas" aria-label="Close"></button>
        </div>
        <div class="offcanvas-body">
          <ul class="floors">
            <li class="floor"
                v-for="(floor, index) in (building?.robot ? [...building.robot].reverse() : [])"
                :key="index"
                :class="{ 'active': activeFloor === index }"
                @mouseover="showFloorInfo(floor, index)"
                @mouseout="clearFloorInfo">
              <div class="floor-name">{{ floor.floor }}층</div>
              <div class="floor-detail">
                <span class="floor-robot" :class="{ 'visible': activeFloor === index }">정상로봇: {{ floor.right }} <br> 고장로봇: {{ floor.wrong }}</span>
                <span class="floor-info">{{ floor.etc }}</span>
              </div>
            </li>
          </ul>
        </div>
      </div>
    </div>
    <div class="main-content">
      <div class="building-info">건물상세</div>
      <div class="image">
        <img src="https://via.placeholder.com/870x491" alt="Building Image">
      </div>
      <div class="building-details">
        건물명 : {{ building?.building?.building_name }}
      </div>
    </div>
  </div>
</template>


<script setup>
import { useUserStore } from '@/stores/user/';
import { onMounted, ref } from 'vue';
import axios from 'axios'

const store = useUserStore();

const building = ref([])
const activeFloor = ref(null);

onMounted(() => {
  axios({
    method: 'get',
    url: `${store.API_URL}buildings/check-building/818/`,
    headers: {
      Authorization: `Token ${store.token}`,
    },
  }).then((response) => {
    building.value = response.data
  }).catch((error) => {
    console.log(error);
  })
})

const showFloorInfo = (floor, index) => {
  activeFloor.value = index;
}

const clearFloorInfo = () => {
  activeFloor.value = null;
}
</script>


<style lang="scss" scoped>
.content {
  display: flex;
  height: 100vh;
  position: relative;
}

.sidebar {
  width: 15%;
  padding: 30px;
  overflow-y: auto;
  border-right: 1px solid #ccc;
  box-sizing: border-box;
  position: absolute;
  left: 0;
  top: 0;
  bottom: 0;
  transition: width 0.3s ease;
  background: white;
  z-index: 10;

  &.expanded {
    width: 35%;
  }
}

.sidebar .floors {
  list-style: none;
  padding: 0;
  margin: 0;
}

.sidebar .floor {
  height: 70px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  box-sizing: border-box;
  font-size: 20px;
  color: black;
  cursor: pointer;
  text-align: center;
  transition: background 0.3s ease;
  position: relative;

  &.active {
    background: #f0f0f0;
  }
}

.sidebar .floor .floor-name {
  flex: 0 0 150px;
  height: 95%;
  border: 1px solid black;
  border-radius: 10px;
  box-sizing: border-box;
  text-align: center;
  padding: 0 10px;
  background: white;
  display: flex;
  justify-content: center;
  align-items: center;
}

.sidebar .floor .floor-detail {
  height: 100%;
  position: relative;
  box-sizing: border-box;
}

.sidebar .floor .floor-info {
  position: relative;
  padding-left: 10px;
  text-align: left;
  opacity: 1;
  transition: opacity 0.3s ease;
  width: 100%;
}

.sidebar .floor .floor-robot {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  padding-left: 10px;
  text-align: left;
  opacity: 0;
  transition: opacity 0.5s ease;
  display: flex;
  align-items: center;
  justify-content: center;
  overflow: hidden;
}

.sidebar .floor:hover .floor-info {
  opacity: 0;
}

.sidebar .floor:hover .floor-robot {
  opacity: 1;
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

.offcanvas {
  background-color: rgba(255, 255, 255, 0.9) !important; /* 투명도 90% 설정 */
}

.offcanvas-body * {
  cursor: default !important;
}

.offcanvas-backdrop {
  display: none !important;
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
