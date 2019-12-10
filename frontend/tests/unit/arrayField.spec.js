import Vuex from 'vuex'
import Vuetify from 'vuetify'
import { mount, createLocalVue } from '@vue/test-utils'
import ArrayField from '@/components/forms/fields/ArrayField.vue'

const localVue = createLocalVue()

describe('ArrayField.vue', () => {

  let vuetify

  const schema = {
    title: "Array field title",
  }
  const options = {
    type: "array",
    items: {
      type: "select",
      dataSource: [
        { text: "Option 1", value: "option1" },
        { text: "Option 2", value: "option2" },
        { text: "Option 3", value: "option3" },
      ],
    },
  }

  beforeEach(() => {
    vuetify = new Vuetify()
  })

  it('loads the list of selected items from the state', () => {
    const wrapper = mount(ArrayField, {
      localVue,
      vuetify,
      propsData: {
        id: 'arrayTestId',
        schema: schema,
        options: options,
        storeDataName: 'arrayTestData'
      },
      store: new Vuex.Store({
        state: {
          arrayTestData: {
            arrayTestId: ['option1', 'option3']
          }
        }
      })
    })
    const cardsTexts = wrapper.findAll('.culture-card').wrappers.map(x => x.text())
    expect(cardsTexts).toContain('Option 1')
    expect(cardsTexts).not.toContain('Option 2')
    expect(cardsTexts).toContain('Option 3')
  })
})
