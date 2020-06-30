import VueRouter from 'vue-router'
import Vuex from 'vuex'
import Vuetify from 'vuetify'
import { mount, createLocalVue } from '@vue/test-utils'
import Practice from '@/views/Practice.vue'

const localVue = createLocalVue()
localVue.use(VueRouter)

describe('Practice.vue', () => {

  let vuetify

  const practice = {
    "mechanism": {
      "name": "Détruire mécaniquement les adventices",
      "description": "Le principe des outils disponibles est d’arracher ou de sectionner les adventices."
    },
    "title": "Utiliser un rouleau à lames pour détruire un couvert",
    "short_title": "Rouleau à lames pour détruire le couvert",
    "description": "Le rouleau à lame blesse plus le couvert que le simple rouleau.",
    "equipment": "Rouleau à lames tranchantes",
    "schedule": "Hiver",
    "impact": "Couche et coupe les végétaux",
    "additional_benefits": "Maintient une couverture sur le sol",
    "success_factors": "Choisir les espèces du mélange en vue de les détruire de cette manière.",
    "image": "http://0.0.0.0:8000/media/att8Y4r6TdpLFqJFj.jpeg",
    "main_resource": {
      "name": "Choisir son rouleau destructeur de couverts",
      "description": "La page d'Entraid présente les différents types de rouleaux.",
      "resource_type": "SITE_WEB",
      "image": "http://0.0.0.0:8000/media/att6Sxb1aQdWqQycx.jpg",
      "url": "https://www.entraid.com/articles/rouleau-destructeur-de-couverts-faire-le-bon-choix#"
    },
    "main_resource_label": "Quel rouleau choisir ?",
    "secondary_resources": [{
      "airtable_url": "https://airtable.com/tblVb2GDuCPGUrt35/rec88En2C26RplllJ/",
      "name": "Quatre outils de destruction de couverts au banc d’essai",
      "description": "Entraid présente dans cet article un essai ayant eu lieu dans les Landes.",
      "resource_type": "SITE_WEB",
      "image": "http://0.0.0.0:8000/media/att6Sxb1aQdWqQycx.jpg",
      "url": "https://www.entraid.com/articles/detruire-les-couverts-vegetaux-arvalis-2"
    }],
  }


  beforeEach(() => {
    vuetify = new Vuetify()
  })

  const router = new VueRouter({
    routes: [
      {
        path: '/',
        name: 'Map',
      }
    ]
  })

  it('displays the practice title', () => {
    const wrapper = mount(Practice, {
      localVue,
      vuetify,
      propsData: {
        practice: practice,
      },
      router: router,
      store: new Vuex.Store(),
    })
    expect(wrapper.findAll('.title').length).toBe(1)
    expect(wrapper.find('.title').text()).toBe(practice.title)
  })

  it('displays the practice description', () => {
    const wrapper = mount(Practice, {
      localVue,
      vuetify,
      propsData: {
        practice: practice,
      },
      router: router,
      store: new Vuex.Store(),
    })
    expect(wrapper.findAll('.practice-description').length).toBe(1)
    expect(wrapper.find('.practice-description').text()).toBe(practice.description)
  })

})
