import { createRouter, createWebHistory } from 'vue-router'
import StationList from '../components/StationList.vue'
import StationDetail from '../components/StationDetail.vue'

const routes = [
  { path: '/', component: StationList },
  { path: '/station/:id', component: StationDetail, props: true }
]

export default createRouter({
  history: createWebHistory(),
  routes
})
