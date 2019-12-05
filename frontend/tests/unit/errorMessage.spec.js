import Vue from 'vue'
import Vuetify from 'vuetify'
import { mount } from '@vue/test-utils'
import ErrorMessage from '@/components/ErrorMessage.vue'

Vue.use(Vuetify)

describe('ErrorMessage.vue', () => {

  it('does not render a retry button without an onRetry function', () => {
    const wrapper = mount(ErrorMessage, {
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
