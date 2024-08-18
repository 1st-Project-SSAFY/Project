<template>
  <!-- 카카오api 지도 -->
  <div class="container">
    <div class="title">관내 건물</div>
    <div class="cards">
      <div class="card" v-for="(building, index) in buildings" :key="index">
        <div :id="'map' + index" class="map"></div>
        <div class="card-content">
          <p>건물명: {{ building.name }}</p>
          <p>주소: {{ building.location }}</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'KakaoMap',
  data() {
    return {
      buildings: [
        { name: '멀티캠퍼스', location: '서울특별시 강남구 테헤란로 212', 기기대수: 10 },
        { name: 'GFC', location: '서울특별시 강남구 테헤란로 152 강남파이낸스센터', 기기대수: 20 },
        { name: '센터필드', location: '서울특별시 강남구 역삼동 676', 기기대수: 2 },
        { name: '한국은행 강남본부', location: '서울 강남구 테헤란로 202 한국은행강남본부', 기기대수: 2 },
        { name: '역삼역', location: '서울특별시 강남구 테헤란로 156', 기기대수: 2 },
        { name: '선릉역', location: '서울특별시 강남구 테헤란로 340', 기기대수: 2 }
      ],
      map: null,
    };
  },
  mounted() {
    if (window.kakao && window.kakao.maps) {
      this.loadMap();
    } else {
      this.loadScript();
    }
  },
  methods: {
    loadScript() {
      const script = document.createElement('script');
      script.src = 'https://dapi.kakao.com/v2/maps/sdk.js?appkey=01f1b08e0b51a6a36084c1c22b333eaf&libraries=services&autoload=false';
      script.onload = () => window.kakao.maps.load(this.loadMap);
      document.body.appendChild(script);
    },
    loadMap() {
      this.buildings.forEach((building, index) => {
        const geocoder = new window.kakao.maps.services.Geocoder();
        geocoder.addressSearch(building.location, (result, status) => {
          if (status === window.kakao.maps.services.Status.OK) {
            const coords = new window.kakao.maps.LatLng(result[0].y, result[0].x);
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
              content: `<div style="width:150px;text-align:center;padding:6px 0;">${building.name}</div>`
            });
            infowindow.open(map, marker);
          } 
        });
      });
    }
  }
};

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

.map {
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
