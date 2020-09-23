import Landing from '@/views/Landing.vue'
import Farmer from '@/views/Farmer.vue'
import Experiment from '@/views/Experiment.vue'
import ExperimentEditor from '@/views/ExperimentEditor.vue'
import FarmEditor from '@/views/FarmEditor.vue'
import PersonalInfoEditor from '@/views/PersonalInfoEditor.vue'
import Profile from '@/views/Profile.vue'
import Share from '@/views/Share.vue'
import Messages from '@/views/Messages.vue'
import store from '@/store/index'
import Map from '@/views/Map'

export default [
  {
    path: '/',
    component: Landing,
    name: 'Landing',
  },
  {
    path: '/exploitation',
    name: 'Map',
    component: Map
  },
  {
    path: '/exploitation/:farmerUrlComponent',
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
      const isValidComponent = route.params.farmerUrlComponent.indexOf('--') >= 0
      if (isValidComponent) {
        next()
      } else {
        next({ name: 'Landing' })
      }
    }
  },
  {
    path: '/exploitation/:farmerUrlComponent/expérience/:experimentUrlComponent',
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
      const isValidFarmerComponent = route.params.farmerUrlComponent.indexOf('--') >= 0
      const isValidXPComponent = route.params.experimentUrlComponent.indexOf('--') >= 0

      if (isValidFarmerComponent && isValidXPComponent) {
        next()
      } else {
        next({ name: 'Landing' })
      }
    }
  },
  {
    path: '/editeur-experience/',
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
    path: '/editeur-profil/',
    name: 'PersonalInfoEditor',
    component: PersonalInfoEditor,
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
          name: 'PersonalInfoEditor',
          query: {
            agriculteur: store.getters.farmerUrlComponent(loggedFarmer)
          }
        })
        return
      } else {
        const requestedFarmer = store.getters.farmerWithUrlComponent(route.query.agriculteur)
        if (requestedFarmer != loggedFarmer) {
          next({
            name: 'PersonalInfoEditor',
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
    path: '/editeur-exploitation/',
    name: 'FarmEditor',
    component: FarmEditor,
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
          name: 'FarmEditor',
          query: {
            agriculteur: store.getters.farmerUrlComponent(loggedFarmer)
          }
        })
        return
      } else {
        const requestedFarmer = store.getters.farmerWithUrlComponent(route.query.agriculteur)
        if (requestedFarmer != loggedFarmer) {
          next({
            name: 'FarmEditor',
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
    path: '/compte',
    component: Profile,
    name: 'Profile',
  },
  {
    path: '/partage-experience',
    component: Share,
    name: 'Share',
  },
  {
    path: '/messages/:farmerUrlComponent?',
    name: 'Messages',
    component: Messages,
    props: (route) => {
      return {
        farmerUrlComponent: route.params ? route.params.farmerUrlComponent : undefined,
      }
    }
  }
]