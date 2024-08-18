<template>
  <!-- 카카오 api 지도 + 로드뷰 -->
  <div class="container">
    <div class="title">관내 건물</div>
    <div class="cards">
      <div class="card" v-for="(building, index) in buildings" :key="index">
        <div :id="'map' + index" class="map"></div>
        <div :id="'roadview' + index" class="roadview"></div>
        <div class="card-content">
          <p>건물명: {{ building.name }}</p>
          <p>주소: {{ building.location }}</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { onMounted, ref } from 'vue';

const buildings = ref([
  { name: '멀티캠퍼스', location: '서울특별시 강남구 역삼동 718-5', 기기대수: 10 },
  { name: 'GFC', location: '서울특별시 강남구 테헤란로 152 강남파이낸스센터', 기기대수: 20 },
  { name: '센터필드', location: '서울 강남구 테헤란로 231 센터필드', 기기대수: 2 },
  { name: '한국은행 강남본부', location: '서울 강남구 테헤란로 202 한국은행강남본부', 기기대수: 2 },
  { name: '태왕빌딩', location: '서울 강남구 테헤란로 226 태왕빌딩', 기기대수: 2 },
  { name: '63빌딩', location: '서울특별시 영등포구 여의도동 60', 기기대수: 2 },
  { name: '남산타워', location: '서울 용산구 남산공원길 105', 기기대수: 2 }
]);

onMounted(() => {
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

async function loadMap() {
  return new Promise((resolve, reject) => {
    if (!window.kakao || !window.kakao.maps || !window.kakao.maps.services) {
      reject(new Error('Kakao Maps API is not loaded properly.'));
      return;
    }

    const geocoder = new window.kakao.maps.services.Geocoder();

    const promises = buildings.value.map((building, index) => {
      return new Promise((resolve, reject) => {
        geocoder.addressSearch(building.location, (result, status) => {
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

            new window.kakao.maps.Marker({
              map: map,
              position: coords
            });

            const infowindow = new window.kakao.maps.InfoWindow({
              content: `<div style="width:150px;text-align:center;padding:6px 0;">${building.name}</div>`
            });
            infowindow.open(map, new window.kakao.maps.Marker({ map, position: coords }));

            resolve();
          } else {
            reject(new Error('Address search failed.'));
          }
        });
      });
    });

    Promise.all(promises).then(() => {
      console.log('All maps and roadviews are loaded.');
      resolve();
    }).catch(err => {
      console.log('Error loading maps or roadviews:', err);
      reject(err);
    });
  });
}
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
