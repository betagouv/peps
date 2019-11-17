import Vue from 'vue'
import VueRouter from 'vue-router'
import FormsContainer from '@/views/FormsContainer.vue'
import Results from '@/views/Results.vue'

Vue.use(VueRouter)

const routes = [
  {
    path: '/',
    name: 'FormsContainer',
    component: FormsContainer,
  },
  {
    path: '/resultats',
    name: 'Results',
    component: Results,
  },
  {
    path: '*',
    redirect: {
      name: 'FormsContainer'
    },
  },
]

const router = new VueRouter({
  routes
})

export default router
