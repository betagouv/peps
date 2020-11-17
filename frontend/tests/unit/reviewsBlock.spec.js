import Vuex from 'vuex'
import Vuetify from 'vuetify'
import { shallowMount, mount, createLocalVue } from '@vue/test-utils'
import ReviewsBlock from "@/components/ReviewsBlock.vue"

const localVue = createLocalVue()
const mockRouter = {
  push: jest.fn()
}

describe('ReviewsBlock.vue', () => {

  let vuetify

  beforeEach(() => {
    vuetify = new Vuetify()
  })

  it('Includes farmer info', () => {
    const wrapper = shallowMount(ReviewsBlock, {
      localVue,
      vuetify,
      mocks: { $router: mockRouter },
      store: new Vuex.Store({
        state: {},
      })
    })
    expect(wrapper.find('div.body-2').text()).toEqual('Thierry Desvaux')
    expect(wrapper.find('div.caption').text()).toEqual('Grandes cultures')
  })

  it('Includes register button if not authenticated', async () => {
    const wrapper = shallowMount(ReviewsBlock, {
      localVue,
      vuetify,
      mocks: { $router: mockRouter },
      store: new Vuex.Store({
        state: {},
      })
    })
    expect(wrapper.find('#reviews-register').exists()).toEqual(true)
  })

  it('Hides register button if authenticated', async () => {
    const wrapper = shallowMount(ReviewsBlock, {
      localVue,
      vuetify,
      mocks: { $router: mockRouter },
      store: new Vuex.Store({
        state: { loggedUser: {} },
      })
    })
    expect(wrapper.find('#reviews-register').exists()).toEqual(false)
  })

  it('Farmer button goes to farmer page', async () => {
    global.sendTrackingEvent = jest.fn()

    const wrapper = mount(ReviewsBlock, {
      localVue,
      vuetify,
      mocks: { $router: mockRouter },
      store: new Vuex.Store({
        state: { loggedUser: {} },
      })
    })

    const button = wrapper.find('#reviews-farmer-btn')
    await button.trigger('click')
    expect(mockRouter.push).toHaveBeenCalled()
  })

  it('Farmer button sends tracking event', async () => {
    global.sendTrackingEvent = jest.fn()

    const wrapper = mount(ReviewsBlock, {
      localVue,
      vuetify,
      mocks: { $router: mockRouter },
      store: new Vuex.Store({
        state: { loggedUser: {} },
      })
    })

    const button = wrapper.find('#reviews-farmer-btn')
    await button.trigger('click')
    expect(global.sendTrackingEvent).toHaveBeenCalled()
  })
})
