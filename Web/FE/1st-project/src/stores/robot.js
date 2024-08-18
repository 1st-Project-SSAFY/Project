import { defineStore } from "pinia"

export const usedRobotStore = defineStore('robot', () =>{
  const API_URL = 'http://3.36.55.201:8000/';
  
  return { API_URL };
}, {
  persist: true
});