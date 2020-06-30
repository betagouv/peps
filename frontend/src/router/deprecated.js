import LegacyFarmer from '@/views/LegacyFarmer.vue'
import store from '@/store/index'

export default [
  {
    path: '/politique-de-confidentialite',
    beforeEnter: (route, _, next) => {
      next({ name: 'CGU' })
    }
  },
  {
    path: '/map',
    beforeEnter: (route, _, next) => {
      next({ name: 'Map' })
    }
  }, {
    path: '/agriculteur/:legacyFarmerUrlComponent',
    name: 'DeprecatedFarmer',
    component: LegacyFarmer,
    props: (route) => ({
      legacyFarmerUrlComponent: route.params.legacyFarmerUrlComponent
    }),
    beforeEnter: (route, _, next) => {
      if (!route.params.legacyFarmerUrlComponent) {
        next({ name: 'Map' })
        return
      }

      const isValidComponent = route.params.legacyFarmerUrlComponent.indexOf('__') >= 0
      if (isValidComponent) {
        next()
        return
      }

      const farmerName = route.params.legacyFarmerUrlComponent
      const farmer = store.state.farmers.find(x => x.name === farmerName)
      if (!farmer) {
        next({ name: 'Map' })
        return
      }
      next({
        name: 'Farmer',
        params: {
          legacyFarmerUrlComponent: store.getters.legacyFarmerUrlComponent(farmer)
        }
      })
    }
  },
]