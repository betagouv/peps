import Landing from '@/views/Landing.vue'
import Results from '@/views/Results.vue'
import FormsContainer from '@/views/FormsContainer.vue'
import Category from '@/views/Category.vue'
import Practice from '@/views/Practice.vue'
import store from '@/store/index'

export default [
  {
    path: '/simulateur',
    component: Landing,
    name: 'Simulator',
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
        next({ name: 'Simulator' })
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
        next({ name: 'Simulator' })
      else
        next()
    }
  },
  {
    path: '/pratiques',
    name: 'Practices',
    component: Landing,
  },
]