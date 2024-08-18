<template>
  <!-- 카카오 api 지도 + 로드뷰 -->
  <div class="container">
    <div class="title">관내 건물</div>
    <div class="cards">
      <div class="card" v-for="(building, index) in buildings" :key="index" @click="goToDetail(building.building_id)">
        <div :id="'map' + index" class="map"></div>
        <div :id="'roadview' + index" class="roadview"></div>
        <div class="card-content">
          <p>건물명: {{ building.building_name }}</p>
          <p>주소: {{ building.address }}</p>
          <p>층수: {{ building.min_floor }}층 ~ {{ building.max_floor }}층</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import axios from 'axios';
import router from '@/router';
import { useUserStore } from '@/stores/user';

const user = useUserStore();
const buildings = ref([]);

onMounted(() => {
  fetchBuildingDetails();
  if (window.kakao && window.kakao.maps) {
    loadMap();
  } else {
    loadScript();
  }
});

const fetchBuildingDetails = () => {
  axios({
    method: 'get',
    url: user.API_URL + 'buildings/check-building/',
    headers: {
      Authorization: `Token ${user.token}`
    }
  }).then((res) => {
    buildings.value = res.data.building_list;
    loadMap(); // API 호출 후에 맵 로드를 호출
  });
};

const goToDetail = (id) => {
  router.push({ path: `/building/${id}` });
};

const loadScript = () => {
  const script = document.createElement('script');
  script.src = 'https://dapi.kakao.com/v2/maps/sdk.js?appkey=01f1b08e0b51a6a36084c1c22b333eaf&libraries=services&autoload=false';
  script.onload = () => window.kakao.maps.load(loadMap);
  document.body.appendChild(script);
};

const loadMap = () => {
  buildings.value.forEach((building, index) => {
    const geocoder = new window.kakao.maps.services.Geocoder();
    geocoder.addressSearch(building.address, (result, status) => {
      if (status === window.kakao.maps.services.Status.OK) {
        const coords = new window.kakao.maps.LatLng(result[0].y, result[0].x);
        const mapContainer = document.getElementById('map' + index);
        const roadviewContainer = document.getElementById('roadview' + index);
        const roadviewClient = new window.kakao.maps.RoadviewClient();
        const mapOption = {
          center: coords,
          level: 3,
          draggable: false,
        };
        const map = new window.kakao.maps.Map(mapContainer, mapOption);

        roadviewClient.getNearestPanoId(coords, 60, function(panoId) {
          if (panoId) {
            const roadview = new window.kakao.maps.Roadview(roadviewContainer);
            roadview.setPanoId(panoId, coords);
          }
        });

        const marker = new window.kakao.maps.Marker({
          map: map,
          position: coords
        });

        const infowindow = new window.kakao.maps.InfoWindow({
          content: `<div style="width:150px;text-align:center;padding:6px 0;">${building.building_name}</div>`
        });
        infowindow.open(map, marker);
      }
    });
  });
};
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
  position: relative;
  width: 100%;
  max-width: 396px;
  overflow: hidden;
  border-radius: 30px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  border: 1px solid black;
  cursor: pointer;
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
