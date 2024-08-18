<!-- <template>
  <naver-map
    style="width: 100%; height: 400px"
    :map-options="mapOptions"
  >
    <naver-marker
      latitude="37.51347"
      longitude="127.041722"
    />
  </naver-map>
  <div>

  </div>
</template>

<script>
import { NaverMap } from 'vue3-naver-maps'
import { NaverMarker } from 'vue3-naver-maps'

export default {
  components: {
    NaverMap,
    NaverMarker,
  },
  data() {
    return {
      buildings: [
        { name: '멀티캠퍼스', location: '서울특별시 강남구 역삼동 718-5', 기기대수: 10 },
        { name: 'GFC', location: '서울특별시 강남구 테헤란로 152 강남파이낸스센터', 기기대수: 20 },
        { name: '센터필드', location: '서울특별시 강남구 역삼동 676', 기기대수: 2 },
        { name: '한국은행 강남본부', location: '서울 강남구 테헤란로 202 한국은행강남본부', 기기대수: 2 },
        { name: '태왕빌딩', location: '서울 강남구 테헤란로 226 태왕빌딩', 기기대수: 2 },
        { name: '63빌딩', location: '서울 영등포구 63로 50', 기기대수: 2 },
        { name: '남산타워', location: '서울 용산구 남산공원길 105', 기기대수: 2 }
      ],
      map: null,
    };
  },
  onMounted() {
    if (window.naver && window.naver.maps) {
      this.loadMap();
    } else {
      this.loadscript();
    }
  },
  methods: {
    loadMap() {
      const map = new window.naver.maps.Map('map', {
        center: new window.naver.maps.LatLng(37.51347, 127.041722),
        zoom: 13,
      });
      this.map = map;
      this.addMarkers();
    },
    addressToCoordinate(address) {
      naver.maps.Service.geocode({
        query: address
      }, function(status, response) {
        return alert('Something Wrong')
      }
    )
    }
  }
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
</style> -->


<template>
  <div>
    <h1>텍스트 파일 내용:</h1>
    <pre>{{ fileContent }}</pre>
  </div>
</template>

<script>
import axios from 'axios';
// import { useUserStore } from '@/stores/user/';

// const store = useUserStore();


export default {
  data() {
    return {
      fileContent: '', // 텍스트 파일 내용을 저장할 변수
    };
  },
  mounted() {
    this.loadTextFile();
  },
  methods: {
    async loadTextFile() {
      try {
        const response = await axios.get('https://fireroadrobot.s3.amazonaws.com/fire_image/orin.txt', {
          responseType: 'text' // 서버에서 텍스트 파일을 가져옴
        });
        this.fileContent = response.data; // 텍스트 내용을 변수에 저장
      } catch (error) {
        console.log('파일을 불러오는 중 오류가 발생했습니다:', error);
      }
    }
  }
};
</script>