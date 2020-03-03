import Vue from 'vue'
import VueRouter from 'vue-router'
import store from '@/store/index'
import FormsContainer from '@/views/FormsContainer.vue'
import Results from '@/views/Results.vue'
import PolitiqueConfidentialite from '@/views/PolitiqueConfidentialite.vue'
import Landing from '@/views/Landing.vue'
import Category from '@/views/Category.vue'
import Practice from '@/views/Practice.vue'
import About from '@/views/About.vue'
import Contact from '@/views/Contact.vue'
import Map from '@/views/Map.vue'
import Farmer from '@/views/Farmer.vue'

Vue.use(VueRouter)

const routes = [
  {
    path: '/',
    name: 'Landing',
    component: Landing,
  },
  {
    path: '/resultats',
    name: 'Results',
    component: Results,
  },
  {
    path: '/formulaire',
    name: 'FormsContainer',
    component: FormsContainer,
  },
  {
    path: '/categorie/:categoryTitle',
    name: 'Category',
    component: Category,
    props: (route) => ({
      category: store.state.categories.find(x => x.title === route.params.categoryTitle)
    }),
    beforeEnter: (route, _, next) => {
      if (!store.state.categories.find(x => x.title === route.params.categoryTitle))
        next({name: 'Landing'})
      else
        next()
    }
  },
  {
    path: '/pratique/:practiceShortTitle',
    name: 'Practice',
    component: Practice,
    props: (route) => ({
      practice: store.getters.practiceWithShortTitle(route.params.practiceShortTitle)
    }),
    beforeEnter: (route, _, next) => {
      if (!store.getters.practiceWithShortTitle(route.params.practiceShortTitle))
        next({name: 'Landing'})
      else
        next()
    }
  },
  {
    path: '/agriculteur/:farmerName',
    name: 'Farmer',
    component: Farmer,
    props: (route) => ({
      farmer: store.getters.farmerWithName(route.params.farmerName)
    }),
    beforeEnter: (route, _, next) => {
      if (!store.getters.farmerWithName(route.params.farmerName))
        next({name: 'Landing'})
      else
        next()
    }
  },
  {
    path: '/politique-de-confidentialite',
    name: 'PolitiqueConfidentialite',
    component: PolitiqueConfidentialite,
  },
  {
    path: '/qui-sommes-nous',
    name: 'QuiSommesNous',
    component: About,
  },
  {
    path: '/contact',
    name: 'Contact',
    component: Contact,
  },
  {
    path: '/map',
    name: 'Map',
    component: Map,
  },
  {
    path: '*',
    redirect: {
      name: 'Landing'
    },
  },
]

const router = new VueRouter({
  routes,
  previousRoute: null,
  scrollBehavior () {
    return new Promise((resolve) => {
      const fadeTransitionTime = 250
      setTimeout(() => {
        resolve({ x: 0, y: 0 })
      }, fadeTransitionTime / 2)
    })
  }
})
router.beforeEach((to, from, next) => {
  router.previousRoute = from
  next()
})
router.afterEach((route, previousRoute) => {
  window.sendPageView ? window.sendPageView(route, previousRoute) : undefined
})

export default router
