import Vuetify from 'vuetify'
import { mount, createLocalVue } from '@vue/test-utils'
import OverlayMessage from '@/components/OverlayMessage.vue'

const localVue = createLocalVue()

describe('OverlayMessage.vue', () => {

  let vuetify

  beforeEach(() => {
    vuetify = new Vuetify()
  })

  it('does not render a retry button without an onRetry function', () => {
    const wrapper = mount(OverlayMessage, {
      localVue,
      vuetify,
      propsData: {
        visible: true,
        onRetry: null
      }
    })
    expect(wrapper.findAll('button').length).toBe(1)
  })

  it('renders a cta that triggers the ctaAction function', () => {
    const ctaAction = jest.fn()
    const wrapper = mount(OverlayMessage, {
      localVue,
      vuetify,
      propsData: {
        visible: true,
        ctaText: 'Click me',
        ctaAction: ctaAction
      }
    })
    const ctaButton = wrapper.findAll('button').wrappers.find(x => x.text() === 'Click me')
    ctaButton.trigger('click')
    expect(ctaAction).toHaveBeenCalledTimes(1)
  })
})
