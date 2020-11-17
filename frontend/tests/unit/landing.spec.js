import Vuex from 'vuex'
import Vuetify from 'vuetify'
import { shallowMount, mount, createLocalVue } from '@vue/test-utils'
import Landing from '@/views/Landing.vue'
import ExperimentFilter from '@/components/ExperimentFilter'
import MailChimpForm from "@/components/MailChimpForm.vue"
import MapBlock from "@/components/MapBlock.vue"
import StatsCards from "@/components/StatsCards.vue"
import ReviewsBlock from "@/components/ReviewsBlock.vue"
import AboutUsCards from "@/components/AboutUsCards.vue"

const localVue = createLocalVue()

const experimentBriefs = [
  {
    images: [],
    id: '1',
    sequence_number: '1',
    tags: [],
    name: 'Test XP',
    short_name: 'Test XP',
    cultures: [],
    creation_date: '2020-11-16T14:16:21Z',
    modification_date: '2020-11-16T14:16:21Z',
    farmer: '1',
    farmer_url_slug: '1--1',
    livestock_types: [],
    postal_code: '69002',
    farmer_name: 'Test Farmer',
    agriculture_types: [],
    objectives: '',
  }
]

describe('Landing.vue', () => {

  let vuetify

  beforeEach(() => {
    vuetify = new Vuetify()
  })

  it('Includes project description', () => {
    const wrapper = shallowMount(Landing, {
      localVue,
      vuetify,
      store: new Vuex.Store({
        state: { experimentBriefs },
      })
    })
    const description = "Un service public qui soutient une agriculture plus durable, pour ceux et celles qui produisent ainsi que pour l'environnement"
    expect(wrapper.find('v-card-text-stub').text()).toEqual(description)
  })

  it('Includes experiment filter section', async () => {
    const wrapper = await shallowMount(Landing, {
      localVue,
      vuetify,
      store: new Vuex.Store({
        state: { experimentBriefs },
      })
    })
    const header = "Explorez les retours d'expérience"
    expect(wrapper.find('h2#explore-xp').text()).toEqual(header)
    expect(wrapper.findComponent(ExperimentFilter).exists()).toBe(true)
  })

  it('Includes newsletter section', async () => {
    const wrapper = await shallowMount(Landing, {
      localVue,
      vuetify,
      store: new Vuex.Store({
        state: { experimentBriefs },
      })
    })
    const header = "Actualités"
    expect(wrapper.find('h2#actualites').text()).toEqual(header)
    expect(wrapper.findComponent(MailChimpForm).exists()).toBe(true)
  })

  it('Includes map section', async () => {
    const wrapper = await shallowMount(Landing, {
      localVue,
      vuetify,
      store: new Vuex.Store({
        state: { experimentBriefs },
      })
    })
    const header = "Des exploitations sur tout le territoire"
    expect(wrapper.find('h2#location').text()).toEqual(header)
    expect(wrapper.findComponent(MapBlock).exists()).toBe(true)
  })

  it('Includes stats section', async () => {
    const wrapper = await shallowMount(Landing, {
      localVue,
      vuetify,
      store: new Vuex.Store({
        state: { experimentBriefs },
      })
    })
    const header = "Le service Peps en chiffres"
    expect(wrapper.find('h2#stats').text()).toEqual(header)
    expect(wrapper.findComponent(StatsCards).exists()).toBe(true)
  })

  it('Includes reviews section', async () => {
    const wrapper = await shallowMount(Landing, {
      localVue,
      vuetify,
      store: new Vuex.Store({
        state: { experimentBriefs },
      })
    })
    const header = "Paroles de convaincus"
    expect(wrapper.find('h2#reviews').text()).toEqual(header)
    expect(wrapper.findComponent(ReviewsBlock).exists()).toBe(true)
  })

  it('Includes about section', async () => {
    const wrapper = await shallowMount(Landing, {
      localVue,
      vuetify,
      store: new Vuex.Store({
        state: { experimentBriefs },
      })
    })
    const header = "Le projet Peps, qu'est-ce que c'est ?"
    expect(wrapper.find('h2#about').text()).toEqual(header)
    expect(wrapper.findComponent(AboutUsCards).exists()).toBe(true)
  })
})
