<template>
  <div class="container">
    <div class="title">관내 건물</div>
    <div class="form-check">
      <input class="form-check-input" type="checkbox" id="flexCheckChecked" v-model="showFireOnly">
      <label class="form-check-label" for="flexCheckChecked">
        화재 발생 건물
      </label>
    </div>
    <form class="searchForm">
      <div class="input-group mt-3">
      <input type="text" class="form-control" placeholder="건물 이름을 입력하세요" v-model="searchQuery">
    </div>
    </form>
    <div class="cards">
      <div class="card" v-for="(building, index) in filteredBuildings" :key="index" @click="goToDetail(building.id)">
        <img class="fire-image" src="@/assets/fire2.gif" alt="" v-if="building.fire">
        <div :id="'map' + (index + (currentPage - 1) * itemsPerPage)" class="map"></div>
        <div class="card-content">
          <p>건물명: {{ building.building_name }}</p>
          <p>주소: {{ building.address }}</p>
          <p>층수: {{ building.min_floor }}층 ~ {{ building.max_floor }}층</p>
        </div>
      </div>
    </div>

    <div class="pagination">
      <button @click="changePage(page)" :class="{ active: page === currentPage }" v-for="page in totalPages" :key="page">
        {{ page }}
      </button>
    </div>
  </div>
</template>

<script setup>
import { useUserStore } from '@/stores/user/';
import { onMounted, ref, computed, watch } from 'vue';
import router from '@/router/index';
import axios from 'axios';

const store = useUserStore();
const buildings = ref([]);
const currentPage = ref(1);
const itemsPerPage = ref(8);
const showFireOnly = ref(false);
const searchQuery = ref('')

const updateItemsPerPage = () => {
  const width = window.innerWidth;
  if (width >= 1440) {
    itemsPerPage.value = 8;
  } else if (width >= 768) {
    itemsPerPage.value = 6;
  } else {
    itemsPerPage.value = 4;
  }
};

const filteredBuildings = computed(() => {
  let filtered = showFireOnly.value
    ? buildings.value.filter(building => building.fire)
    : buildings.value;

  if (searchQuery.value) {
    filtered = filtered.filter(building =>
      building.building_name.toLowerCase().includes(searchQuery.value.toLowerCase())
    );
  }

  const start = (currentPage.value - 1) * itemsPerPage.value;
  const end = start + itemsPerPage.value;

  return filtered.slice(start, end);
})

// 페이지 관리
const totalPages = computed(() => {
  const filtered = showFireOnly.value
    ? buildings.value.filter(building => building.fire)
    : buildings.value;
  return Math.ceil(filtered.length / itemsPerPage.value);
});

const changePage = (page) => {
  currentPage.value = page;
};

onMounted(async () => {
  updateItemsPerPage();
  window.addEventListener('resize', updateItemsPerPage);
  console.log('route', router.params)

  await buildingdetail();

  if (window.kakao && window.kakao.maps) {
    loadMap();
  } else {
    loadScript();
  }
});


const loadScript = () => {
  const script = document.createElement('script');
  script.src = 'https://dapi.kakao.com/v2/maps/sdk.js?appkey=01f1b08e0b51a6a36084c1c22b333eaf&libraries=services&autoload=false';
  script.onload = () => window.kakao.maps.load(loadMap);
  document.body.appendChild(script);
};

const loadMap = () => {
  buildings.value.forEach((building, index) => {
    const coords = new window.kakao.maps.LatLng(building.latitude, building.longitude);
    const container = document.getElementById('map' + index);
    const options = {
      center: coords,
      draggable: false,
      level: 3
    };
    const map = new window.kakao.maps.Map(container, options);
    const marker = new window.kakao.maps.Marker({
      map: map,
      position: coords
    });
    const infowindow = new window.kakao.maps.InfoWindow({
      content: `<div style="width:150px;text-align:center;padding:6px 0;">${building.building_name}</div>`
    });
    infowindow.open(map, marker);
  });
};

const buildingdetail = async () => {
  try {
    const res = await axios({
      method: 'get',
      url: store.API_URL + 'buildings/check-building/',
      headers: {
        Authorization: `Token ${store.token}`,
      },
    });
    buildings.value = res.data.building_list;
    console.log(buildings.value);
  } catch (error) {
    console.log('Error fetching building details:', error);
  }
};

const goToDetail = (id) => {
  router.push({ name: 'building-detail', params: { building_id: id } });
};

watch(() => store.duty, (duty) => {
  if (duty === 0) {
    showFireOnly.value = true;
  } else {
    showFireOnly.value = false;
  }
});
</script>

<style scoped>
p {
  margin-bottom: 10px;
}

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

.form-check {
  margin-left: auto;
  margin-right: 80px;
}

.searchForm {
  margin-left: auto;
  margin-right: 80px;
  width: 100%;
  max-width: 400px;
}

.cards {
  display: flex;
  flex-wrap: wrap;
  gap: 30px;
  justify-content: center;
  margin-top: 50px;
}

.card {
  cursor: pointer;
  position: relative;
  width: 100%;
  max-width: 396px;
  overflow: hidden;
  border-radius: 30px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  border: 1px solid black;
}

.fire-image {
  position: absolute;
  top: 10px;
  right: 10px;
  width: 80px; 
  height: auto;
  z-index: 10;
}

.map, .roadview {
  width: 100%;
  height: 318px;
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

.pagination {
  margin-top: 20px;
  display: flex;
  justify-content: center;
}

.pagination button {
  margin: 0 5px;
  padding: 8px 16px;
  border: none;
  background-color: #ccc;
  cursor: pointer;
  border-radius: 5px;
}

.pagination button.active {
  background-color: #007bff;
  color: white;
}

.pagination button:hover:not(.active) {
  background-color: #ddd;
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
