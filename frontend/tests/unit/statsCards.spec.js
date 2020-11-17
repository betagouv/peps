import Vuex from 'vuex'
import Vuetify from 'vuetify'
import { shallowMount, mount, createLocalVue } from '@vue/test-utils'
import StatsCards from "@/components/StatsCards.vue"

const localVue = createLocalVue()
const mockRouter = {
  push: jest.fn()
}

describe('StatsCards.vue', () => {

  let vuetify

  beforeEach(() => {
    vuetify = new Vuetify()
  })

  it('Includes stats info', () => {
    const wrapper = shallowMount(StatsCards, {
      localVue,
      vuetify,
      mocks: { $router: mockRouter },
      store: new Vuex.Store({
        state: {
          stats: {
            approvedExperimentCount: 157,
            approvedFarmerCount: 93,
            contactCount: 10
          }
        },
      })
    })
    const cards = wrapper.findAll('v-card-stub')
    const values = {
      "Retours d'expérience d'agriculteurs": "157",
      "Profils d'exploitations": "93",
      "Mises en relation entre agriculteurs": "10",
    }

    cards.wrappers.forEach(card => {
      const subtitle = card.find('v-card-subtitle-stub').text()
      expect(card.find('v-card-title-stub').text()).toEqual(values[subtitle])
    })
  })

  it('Button goes to stats page', async () => {
    global.sendTrackingEvent = jest.fn()

    const wrapper = mount(StatsCards, {
      localVue,
      vuetify,
      mocks: { $router: mockRouter },
      store: new Vuex.Store({
        state: {
          stats: {
            approvedExperimentCount: 157,
            approvedFarmerCount: 93,
            contactCount: 10
          }
        },
      })
    })
    const button = wrapper.find('#stats-button')
    await button.trigger('click')
    expect(mockRouter.push).toHaveBeenCalled()
  })

  it('Button triggers event', async () => {
    global.sendTrackingEvent = jest.fn()

    const wrapper = mount(StatsCards, {
      localVue,
      vuetify,
      mocks: { $router: mockRouter },
      store: new Vuex.Store({
        state: {
          stats: {
            approvedExperimentCount: 157,
            approvedFarmerCount: 93,
            contactCount: 10
          }
        },
      })
    })

    const button = wrapper.find('#stats-button')
    await button.trigger('click')
    expect(global.sendTrackingEvent).toHaveBeenCalled()
  })
})
