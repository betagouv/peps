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
import Experiment from '@/views/Experiment.vue'
import Contribution from '@/views/Contribution.vue'
import Profile from '@/views/Profile.vue'
import ExperimentEditor from '@/views/ExperimentEditor.vue'
import FarmerEditor from '@/views/FarmerEditor.vue'

Vue.use(VueRouter)

const routes = [
  {
    path: '/',
    component: Landing,
    name: 'Landing',
  },
  {
    path: '/simulateur',
    beforeEnter: (route, _, next) => {
      next({ name: 'Landing' })
    }
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
    path: '/contribution',
    name: 'Contribution',
    component: Contribution,
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
        next({ name: 'Landing' })
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
        next({ name: 'Landing' })
      else
        next()
    }
  },
  {
    path: '/agriculteur/:farmerUrlComponent',
    name: 'Farmer',
    component: Farmer,
    props: (route) => ({
      farmerUrlComponent: route.params.farmerUrlComponent
    }),
    beforeEnter: (route, _, next) => {
      if (!route.params.farmerUrlComponent) {
        next({ name: 'Landing' })
        return
      }

      const isValidComponent = route.params.farmerUrlComponent.indexOf('__') >= 0
      if (isValidComponent) {
        next()
        return
      }

      const farmerName = route.params.farmerUrlComponent
      const farmer = store.state.farmers.find(x => x.name === farmerName)
      if (!farmer) {
        next({ name: 'Landing' })
        return
      }
      next({
        name: 'Farmer',
        params: {
          farmerUrlComponent: store.getters.farmerUrlComponent(farmer)
        }
      })
    }
  },
  {
    path: '/agriculteur/:farmerUrlComponent/experimentation/:experimentUrlComponent',
    name: 'Experiment',
    component: Experiment,
    props: (route) => {
      return {
        farmerUrlComponent: route.params.farmerUrlComponent,
        experimentUrlComponent: route.params.experimentUrlComponent
      }
    },
    beforeEnter: (route, _, next) => {
      if (!route.params.farmerUrlComponent || !route.params.experimentUrlComponent) {
        next({ name: 'Landing' })
        return
      }
      const isValidFarmerComponent = route.params.farmerUrlComponent.indexOf('__') >= 0
      const isValidXPComponent = route.params.experimentUrlComponent.indexOf('__') >= 0

      if (isValidFarmerComponent && isValidXPComponent) {
        next()
        return
      }

      let farmerUrlComponent = route.params.farmerUrlComponent
      let experimentUrlComponent = route.params.experimentUrlComponent
      if (!isValidFarmerComponent) {
        const farmerName = route.params.farmerUrlComponent
        const farmer = store.state.farmers.find(x => x.name === farmerName)
        if (!farmer) {
          next({ name: 'Landing' })
          return
        }
        farmerUrlComponent = store.getters.farmerUrlComponent(farmer)
      }
      if (!isValidXPComponent) {
        const xpFarmer = store.getters.farmerWithUrlComponent(farmerUrlComponent)
        if (!xpFarmer) {
          next({ name: 'Landing' })
          return
        }
        const experimentName = route.params.experimentUrlComponent
        const experiment = xpFarmer.experiments.find(x => x.name === experimentName)
        if (!experiment) {
          next({ name: 'Landing' })
          return
        }
        experimentUrlComponent = store.getters.experimentUrlComponent(experiment)
      }
      next({
        name: 'Experiment',
        params: {
          farmerUrlComponent,
          experimentUrlComponent
        }
      })
    }
  },
  {
    path: '/editeurXP/',
    name: 'ExperimentEditor',
    component: ExperimentEditor,
    props: (route) => {
      return {
        experimentUrlComponent: route.query.xp
      }
    },
    beforeEnter: (route, _, next) => {
      // This view is not accessible to unlogged users
      if (!store.state.loggedUser) {
        next({ name: 'Landing' })

        // This view is always accessible to superusers
      } else if (store.state.loggedUser.is_superuser) {
        next()

        // This view is not accessible to users without a farmer profile
      } else if (!store.state.loggedUser.farmer_id) {
        next({ name: 'Landing' })

        // If we are creating a new XP, we an access the view
      } else if (!route.query.xp) {
        next()

        // If we are editing an existing XP, it must belong to the logged farmer
      } else {
        const farmer = store.getters.farmerWithId(
          store.state.loggedUser.farmer_id
        )
        let experiment = store.getters.experimentWithUrlComponent(farmer, route.query.xp)
        if (experiment) {
          next()
        } else {
          next({ name: 'Landing' })
        }
      }
    }
  },
  {
    path: '/editeurProfil/',
    name: 'FarmerEditor',
    component: FarmerEditor,
    props: (route) => {
      return {
        farmerUrlComponent: route.query.agriculteur
      }
    },
    beforeEnter: (route, _, next) => {
      // If the user is not logged or the logged user has no farmer profile we redirect
      if (!store.state.loggedUser || !store.state.loggedUser.farmer_id) {
        next({ name: 'Profile' })
        return
      }

      const loggedFarmer = store.getters.farmerWithId(store.state.loggedUser.farmer_id)
      const hasFarmerQuery = route.query && route.query.agriculteur

      // A logged used can only modify its own farmer profile
      if (!hasFarmerQuery) {
        next({
          name: 'FarmerEditor',
          query: {
            agriculteur: store.getters.farmerUrlComponent(loggedFarmer)
          }
        })
        return
      } else {
        const requestedFarmer = store.getters.farmerWithUrlComponent(route.query.agriculteur)
        if (requestedFarmer != loggedFarmer) {
          next({
            name: 'FarmerEditor',
            query: {
              agriculteur: store.getters.farmerUrlComponent(loggedFarmer)
            }
          })
          return
        }
      }
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
    path: '/pratiques',
    name: 'Practices',
    component: Landing,
  },
  {
    path: '/map',
    component: Map,
    name: 'Map',
  },
  {
    path: '/compte',
    component: Profile,
    name: 'Profile',
    beforeEnter: (route, _, next) => {
      if (!store.state.loggedUser) {
        next({ name: 'Map' })
      } else {
        next()
      }
    }
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
  next()
})
router.afterEach((route, previousRoute) => {
  window.sendPageView ? window.sendPageView(route, previousRoute) : undefined
})

export default router
