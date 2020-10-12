import Vue from 'vue'
import VueRouter from 'vue-router'
import CGU from '@/views/Cgu.vue'
import About from '@/views/About.vue'
import Contact from '@/views/Contact.vue'
import Stats from '@/views/Stats.vue'
import experimentShareRoutes from '@/router/experimentshare.js'
import deprecatedRoutes from '@/router/deprecated.js'


Vue.use(VueRouter)

const baseRoutes = [
  {
    path: '/conditions-generales-d-utilisation',
    name: 'CGU',
    component: CGU
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
    path: '/stats',
    name: 'Stats',
    component: Stats,
  },
  {
    path: '*',
    redirect: {
      name: 'Landing'
    },
  },
]

const routes = [].concat(experimentShareRoutes, deprecatedRoutes, baseRoutes)

const router = new VueRouter({
  mode: 'history',
  routes,
  previousRoute: null,
  scrollBehavior() {
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

  // Since we migrated to history mode, we need to ensure old routes
  // redirect to the new URLs
  if (to.fullPath.substr(0, 2) === '/#') {
    const path = to.fullPath.substr(2)
    next(path)
    return
  }

  next()
})
router.afterEach((route, previousRoute) => {
  window.sendPageView ? window.sendPageView(route, previousRoute) : undefined
})

export default router
