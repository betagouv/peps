import Vue from 'vue'
import Vuetify from 'vuetify'
import { mount } from '@vue/test-utils'
import TextField from '@/components/forms/fields/TextField.vue'

Vue.use(Vuetify)

describe('TextField.vue', () => {

  it('shows a placeholder if included in the options', () => {
    const schema = {
      "title": "Nom et prénom",
      "type": "string",
    }
    const options = {
      "placeholder": "Nom Prénom",
    }
    const wrapper = mount(TextField, {
      propsData: {
        id: 'test-id',
        schema: schema,
        options: options
      }
    })
    const textInput = wrapper.find('input[type="text"]')
    expect(textInput.attributes('placeholder')).toBe('Nom Prénom')
  })
})
