<template>
  <div class="container">
    <div class="title">관내 건물</div>
    <div class="cards">
      <div 
      class="card" 
      v-for="(building, index) in buildings" 
      :key="index" 
      @click="goToDetail(building.building_id)">
        <img :src="building.img" :alt="index">
        <div class="card-content">
          <p>건물명 : {{ building.building_name }}</p>
          <p>주소 : {{ building.address }}</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { useUserStore } from '@/stores/user/'
import { onMounted, ref } from 'vue';
import router from '@/router';
import axios from 'axios';

const user = useUserStore()
const buildings = ref([])
// id, building_id, building_name, firestations, max_floor, min_floor

onMounted(() => {
  buildingdetail()
  console.log(buildings)
})

const buildingdetail = () => {
  axios({
    method: 'get',
    url: user.API_URL + 'buildings/check-building/',
    headers: {
      Authorization : `Token ${user.token}`
    }
  }).then((res) => {
    console.log(res.data)
    buildings.value = res.data.building_list
  })
}

const goToDetail = (id) => {
  router.push({ path: `/building/${id}` });
}

</script>

<style scoped>
.container {
  display: flex;
  width: 100%;
  max-width: 100%;
  padding: 20px;
  box-sizing: border-box;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  margin: 0 auto;
}

.title {
  text-align: center;
  color: black;
  font-size: 40px;
  margin-top: 54px;
}

.cards {
  display: flex;
  flex-wrap: wrap;
  gap: 30px;
  justify-content: center;
  margin-top: 50px;
}

.card {
  width: 100%;
  max-width: 396px;
  border-radius: 30px;
  overflow: hidden;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  border: 1px solid black;
}

.card img {
  width: 100%;
  height: 318px;
  object-fit: cover;
}

.card-content {
  padding: 20px;
  background: white;
  flex-grow: 1;
}

.card-content p {
  color: black;
  font-size: 20px;
  margin: 0;
  line-height: 1.4;
}

@media (max-width: 768px) {
  .title {
    font-size: 30px;
  }

  .card-content p {
    font-size: 18px;
  }
}

@media (max-width: 480px) {
  .title {
    font-size: 24px;
  }

  .card-content p {
    font-size: 16px;
  }

  .card img {
    height: auto;
  }
}
</style>