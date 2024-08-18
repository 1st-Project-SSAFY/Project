<template>
  <div class="content">
    <SidebarComponent 
      @select-floor="selectFloor"
      :building="building" 
      />
    <div class="main-content">
      <BuildingDetailComponent
        v-if="!floorSelected && !isLoading"
        :building="building"
      />
      <FloorDetailComponentVue
        v-if="floorSelected && !isLoading"
        :floordetail="floorDetail"
      />
      <div v-if="isLoading" class="spinner-border text-danger loading" role="status">
        <span class="visually-hidden">Loading...</span>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, watch, onMounted } from 'vue';
import { useUserStore } from '@/stores/user/';
import { useRoute } from 'vue-router';
import router from '@/router/index';
import axios from 'axios';
import SidebarComponent from '@/components/building/SidebarComponent.vue';
import FloorDetailComponentVue from './FloorDetailComponent.vue';
import BuildingDetailComponent from './BuildingDetailComponent.vue';

const route = useRoute();
const store = useUserStore();

const building = ref([]);
const buildingId = route.params.building_id
const floorDetail = ref([]);
const isLoading = ref(true);

let floorSelected = ref(false);

onMounted(() => {
  axios({
    method: 'get',
    url: `${store.API_URL}buildings/check-building/${buildingId}/`,
    headers: {
      Authorization: `Token ${store.token}`,
    },
  }).then((response) => {
    building.value = response.data;
    isLoading.value = false;

    if (route.params.floor_index) {
      floorSelected.value = true;
      selectFloor(route.params.floor_index)
    }
    console.log(response.data);
  }).catch((error) => {
    console.log(error);
    isLoading.value = false;
  });
});

watch(() => route.params.floor_index, (index) => {
  if (index) {
    floorSelected.value = true;
    selectFloor(index);
  } else {
    floorSelected.value = false;
  }
})

const selectFloor = (floor) => {
  floorSelected.value = true;
  router.push({ name: 'floor-detail', params: { building_id: buildingId, floor_index: floor } })
  axios({
    method: 'get',
    url: `${store.API_URL}buildings/check-building/${buildingId}/${floor}/`,
    headers: {
      Authorization: `Token ${store.token}`,
    },
  }).then((response) => {
    floorDetail.value = response.data;
    console.log('floordetail: ', response.data);
  }).catch((error) => {
    console.log(error);
  });
}

</script>

<style lang="scss" scoped>
.loading {
  position: absolute;
  top: 50%;
  left: 50%;
}

.content {
  display: flex;
  height: 100vh;
  position: relative;
}

.main-content {
  flex-grow: 1;
  padding: 20px;
  box-sizing: border-box;
  margin-left: 20%;
  transition: margin-left 0.3s ease;
}

@media (min-width: 768px) {
  .content {
    flex-wrap: nowrap;
  }

  .main-content {
    margin-left: 20%;
  }
}

</style>
