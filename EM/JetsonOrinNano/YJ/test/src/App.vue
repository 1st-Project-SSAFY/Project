<template>
  <img id="outputImage" width="960" height="320">
</template>

<script setup>
  // const url = 
  async function fetchImageFromS3(url) {
        try {
            const response = await fetch(url, {
              credentials: 'include',
            });
            const blob = await response.blob();
            const reader = new FileReader();
            reader.onloadend = function() {
                let base64String = reader.result.replace("data:", "").replace(/^.+,/, "");
                console.log(base64String)
                document.getElementById('outputImage').src = `data:image/png;base64,${base64String}`;
            };
            reader.readAsDataURL(blob);
        } catch (error) {
            console.error('Error fetching or converting image:', error);
        }
    }

    // S3 이미지 URL을 여기에 입력하세요
    const s3ImageUrl = 'https://ssafyfiretestnew.s3.amazonaws.com/fire_img/orin.png';
    console.log(s3ImageUrl)
    fetchImageFromS3(s3ImageUrl);
</script>

<style scoped>

</style>
