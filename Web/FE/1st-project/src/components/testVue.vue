<template>
  <div class="image-container">
    <img src="@/assets/7층.jpg" alt="Image" class="image" />
    <div
      v-for="(point, index) in points"
      :key="index"
      :style="pointStyle(point)"
      class="point"
    ></div>
  </div>
</template>

<script setup>
import { ref } from 'vue';

// JSON 좌표 데이터
const points = ref([
  { x: 50, y: 100 },
  { x: 50, y: 110 },
  { x: 50, y: 120 },
  { x: 50, y: 130 },
  { x: 50, y: 140 },
  { x: 50, y: 150 },
  { x: 50, y: 160 },
  { x: 50, y: 170 },
  { x: 50, y: 180 },
  { x: 50, y: 190 },
  { x: 50, y: 200 },
  { x: 50, y: 210 },
  { x: 50, y: 220 },
  { x: 50, y: 230 },
  { x: 50, y: 240 },
  { x: 50, y: 250 },
  { x: 50, y: 260 },
  { x: 50, y: 270 },
  { x: 50, y: 280 },
  { x: 50, y: 290 },
  { x: 50, y: 300 },
  { x: 50, y: 310 },
  { x: 50, y: 320 },
  { x: 50, y: 330 },
  { x: 50, y: 340 },
  { x: 50, y: 350 },
  { x: 50, y: 360 },
  { x: 50, y: 370 },
  { x: 50, y: 380 },
  { x: 50, y: 390 },
  { x: 50, y: 400 },
  { x: 50, y: 410 },
  { x: 50, y: 420 },
  { x: 60, y: 420 },
  { x: 70, y: 420 },
  { x: 80, y: 420 },
  { x: 90, y: 420 },
  { x: 100, y: 420 },
  { x: 110, y: 420 },
  { x: 120, y: 420 },
  { x: 130, y: 420 },
  { x: 140, y: 420 },
  { x: 150, y: 420 },
  { x: 160, y: 420 },
  { x: 170, y: 420 },
  { x: 180, y: 420 },
  { x: 190, y: 420 },
  { x: 200, y: 420 },
  { x: 200, y: 420 },
  // 추가 좌표...
]);

const pointStyle = (point) => {
  return {
    position: 'absolute',
    top: `${point.y}px`,
    left: `${point.x}px`,
    width: '10px',
    height: '10px',
    backgroundColor: 'green',
    borderRadius: '50%',
  };
};
</script>

<style scoped>
.image-container {
  position: relative;
  display: inline-block;
}

.image {
  width: 100%;
  max-width: 600px;
}

.point {
  position: absolute;
  transform: translate(-50%, -50%);
}
</style>
