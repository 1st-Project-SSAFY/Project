<template>
  <div class="sidebar">
    <button class="btn btn-warning" type="button" data-bs-toggle="offcanvas" data-bs-target="#offcanvasScrolling" aria-controls="offcanvasScrolling">
      층별 정보
    </button>
    <div class="offcanvas offcanvas-start" data-bs-scroll="true" tabindex="-1" id="offcanvasScrolling" aria-labelledby="offcanvasScrollingLabel" ref="offcanvasElement">
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
              @mouseover="floorInfo(index)"
              @mouseout="clearFloorInfo"
              @click="handleFloorClick(floor.floor)">
              <div class="floor-name">{{ floor.floor }}층</div>
              <div class="floor-detail">
                <p class="floor-robot" :class="{ 'visible': activeFloor === index }">정상로봇: {{ floor.right }} <br> 고장로봇: {{ floor.wrong }}</p>
                <p class="floor-info">{{ floor.etc }}</p>
              </div>
              <img class="fire-icon" src="@/assets/fire2.gif" alt="불" v-if="floor.fire" >
          </li>
        </ul>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, defineProps, defineEmits } from 'vue';

defineProps({
  building: Object,
});

const activeFloor = ref(null);
const offcanvasElement = ref(null);

// emit 사용
const emit = defineEmits(['select-floor']);

const floorInfo = (index) => {
  activeFloor.value = index;
};

const clearFloorInfo = () => {
  activeFloor.value = null;
};

const handleFloorClick = (floor) => {
  emit('select-floor', floor);
  const exitButton = document.getElementsByClassName('btn-close')
  exitButton[0].click();
};

</script>

<style lang="scss" scoped>
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
  text-align: center;
  transition: background 0.3s ease;
}

.sidebar .floor .fire-icon {
  display: inline;
  width: 40px;
  height: 40px;
  margin-right: 10px;
}

.sidebar .floor .floor-name {
  flex: 0 0 150px;
  height: 95%;
  border: 1px solid black;
  border-radius: 10px;
  box-sizing: border-box;
  text-align: center;
  padding: 0 10px;
  display: flex;
  justify-content: center;
  align-items: center;
}

.sidebar .floor .floor-detail {
  position: relative;
  width: 100%;
  height: 100%;
  display: flex;
  justify-content: center;
  align-items: center;
  overflow: hidden;
}

.sidebar .floor .floor-info {
  position: absolute;
  padding-left: 10px;
  text-align: left;
  opacity: 1;
  transition: opacity 0.3s ease;
  width: 100%;
  height: 100%;
  margin-top: 3px;
}

.sidebar .floor .floor-robot {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  display: flex;
  align-items: center;
  justify-content: center;
  padding-left: 10px;
  text-align: left;
  width: 100%;
  height: 100%;
  opacity: 0;
  transition: opacity 0.3s ease;
}

.sidebar .floor:hover .floor-info {
  opacity: 0;
}

.sidebar .floor:hover .floor-robot {
  opacity: 1;
}

.offcanvas {
  background-color: rgba(255, 255, 255, 0.9) !important;
}

.offcanvas-body * {
  cursor: default !important;
}

.offcanvas-backdrop {
  display: none !important;
}

.sidebar::-webkit-scrollbar {
  width: 8px;
}

.sidebar::-webkit-scrollbar-track {
  background: white;
}
</style>
