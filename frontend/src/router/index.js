import Vue from 'vue'
import VueRouter from 'vue-router'
import store from '@/store/index'
import FormsContainer from '@/views/FormsContainer.vue'
import Results from '@/views/Results.vue'
import PolitiqueConfidentialite from '@/views/PolitiqueConfidentialite.vue'
import Landing from '@/views/Landing.vue'
import Category from '@/views/Category.vue'
import PracticeView from '@/views/PracticeView.vue'
import About from '@/views/About.vue'

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
    path: '/categorie/:categoryId',
    name: 'Category',
    component: Category,
    props: (route) => ({
      category: store.state.categories.find(x => x.id === route.params.categoryId)
    })
  },
  {
    path: '/pratique/:practiceId',
    name: 'Practice',
    component: PracticeView,
    props: (route) => ({
      practice: store.getters.practiceWithId(route.params.practiceId)
    })
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
    path: '*',
    redirect: {
      name: 'Landing'
    },
  },
]

const router = new VueRouter({
  routes,
  scrollBehavior (to, from, savedPosition) {
    if (to.name === 'PolitiqueConfidentialite' || to.name === 'QuiSommesNous')
      return { x: 0, y: 0 }
    return savedPosition
  }
})

router.afterEach((route) => window.sendPageView ? window.sendPageView(route) : undefined)

export default router
