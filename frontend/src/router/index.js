import Vue from 'vue'
import VueRouter from 'vue-router'
import FormsContainer from '@/views/FormsContainer.vue'
import Results from '@/views/Results.vue'
import PolitiqueConfidentialite from '@/views/PolitiqueConfidentialite.vue'

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
    path: '/politique-de-confidentialite',
    name: 'PolitiqueConfidentialite',
    component: PolitiqueConfidentialite,
  },
  {
    path: '*',
    redirect: {
      name: 'FormsContainer'
    },
  },
]

const router = new VueRouter({
  routes,
  scrollBehavior (to, from, savedPosition) {
    if (to.name === 'PolitiqueConfidentialite')
      return { x: 0, y: 0 }
    return savedPosition
  }
})

router.afterEach((route) => window.sendPageView ? window.sendPageView(route) : undefined)

export default router
