import Vuetify from 'vuetify'
import { mount, createLocalVue } from '@vue/test-utils'
import ErrorMessage from '@/components/ErrorMessage.vue'

const localVue = createLocalVue()

describe('ErrorMessage.vue', () => {

  let vuetify

  beforeEach(() => {
    vuetify = new Vuetify()
  })

  it('does not render a retry button without an onRetry function', () => {
    const wrapper = mount(ErrorMessage, {
      localVue,
      vuetify,
      propsData: {
        visible: true,
        onRetry: null
      }
    })
    expect(wrapper.findAll('button').length).toBe(1)
  })

  it('renders a retry button that triggers onRetry function', () => {
    const onRetry = jest.fn()
    const wrapper = mount(ErrorMessage, {
      localVue,
      vuetify,
      propsData: {
        visible: true,
        onRetry: onRetry
      }
    })
    const retryButton = wrapper.findAll('button').wrappers.find(x => x.text() === 'Ressayer')
    retryButton.trigger('click')
    expect(onRetry).toHaveBeenCalledTimes(1)
  })
})
