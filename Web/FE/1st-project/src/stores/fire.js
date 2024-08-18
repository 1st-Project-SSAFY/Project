import { defineStore } from 'pinia';
import { ref } from 'vue';

export const useFireStore = defineStore('fire', () => {
  const robotLocation = {
    pk: ref(''),
    location_x: ref(''),
    location_y: ref(''),
  }
  const robotRoute = ref([]);

  return { robotLocation, robotRoute } 
}, {
  persist: true
})