import { createRouter, createWebHistory } from 'vue-router';
import UserLogin from '@/components/user/UserLogin.vue';
import SignUp from '@/components/user/SignUp.vue';
import SelectBuilding from '@/components/building/SelectBuilding.vue';
import BuildingDetail from '@/components/building/BuildingMain.vue';
import FloorDetail from '@/components/building/FloorDetailComponent.vue';
import RobotDetail from '@/components/robot/RobotDetail.vue';
import RobotRegist from '@/components/robot/RobotRegist.vue';
import TestVue from '@/components/testVue.vue';
import UserBuildingMain from '@/components/manager/UserBuildingMain.vue';

const routes = [
  {
    path: '/',
    name: 'login',
    component: UserLogin,
    meta: { hideNavbar: true, loginBackground: true }
  },
  {
    path: '/accounts/signup',
    name: 'signup',
    component: SignUp,
    meta: { hideNavbar: true, loginBackground: true }
  },
  {
    path: '/regist',
    name: 'regist',
    component: RobotRegist,
  },
  {
    path: '/buildings/check-building',
    name: 'buildings',
    component: SelectBuilding,
  },
  {
    path: '/buildings/check-building/:building_id',
    name: 'building-detail',
    component: BuildingDetail,
    children: [
      {
        path: ':floor_index',
        name: 'floor-detail',
        component: FloorDetail,
      },
    ]
  },
  {
    path: '/buildings/check-building/:building_id/:floor_index/:robot_index',
    name: 'robot-detail',
    component: RobotDetail
  },
  {
    path: '/test',
    name: 'test',
    component: TestVue
  },
  {
    path: '/building-user/building/',
    name: 'user-building',
    component: UserBuildingMain,
  },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
  scrollBehavior(to, from, savedPosition) {
    if (savedPosition) {
      return savedPosition;
    } else {
      return { top: 0 };
    }
  }
});

export default router;
