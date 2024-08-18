<template>
  <div>
    <h1>Home</h1>
  </div>
</template>

<script setup>

</script>

<style lang="scss" scoped>

</style>

<!-- <template>
  <div>
    <h1>Home</h1>
    <img :src="`data:image/png;base64,`+{imageSrc}" alt="Base64 Image" />
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import axios from 'axios';

// const imgUrl = 'https://fireroadrobot.s3.amazonaws.com/fire_image/orin.png'
const imageSrc = ref('');

onMounted(async () => {
  try {
    const response = await axios.get('https://fireroadrobot.s3.amazonaws.com/fire_image/orin.png');
    imageSrc.value = response.data.trim(); // 파일의 내용을 읽어와 이미지 URL로 설정합니다.
  } catch (error) {
    console.error('Failed to load image URL:', error);
    console.log(error)
  }
});
</script>

<style lang="scss" scoped>

</style> -->

<!-- https://fireroadrobot.s3.amazonaws.com/fire_image/orin.png -->