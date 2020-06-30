import LegacyFarmer from '@/views/LegacyFarmer.vue'
import LegacyExperiment from '@/views/LegacyExperiment.vue'

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
      } else {
        next({ name: 'Map' })
      }
    }
  },
  {
    path: '/agriculteur/:legacyFarmerUrlComponent/experimentation/:legacyExperimentUrlComponent',
    name: 'DeprecatedExperiment',
    component: LegacyExperiment,
    props: (route) => {
      return {
        legacyFarmerUrlComponent: route.params.legacyFarmerUrlComponent,
        legacyExperimentUrlComponent: route.params.legacyExperimentUrlComponent
      }
    },
    beforeEnter: (route, _, next) => {
      if (!route.params.legacyFarmerUrlComponent || !route.params.legacyExperimentUrlComponent) {
        next({ name: 'Map' })
        return
      }
      const isValidFarmerComponent = route.params.legacyFarmerUrlComponent.indexOf('__') >= 0
      const isValidXPComponent = route.params.legacyExperimentUrlComponent.indexOf('__') >= 0

      if (isValidFarmerComponent && isValidXPComponent) {
        next()
      } else {
        next({ name: 'Map' })
      }
    }
  },
]