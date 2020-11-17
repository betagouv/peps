import Vuetify from 'vuetify'
import { shallowMount, createLocalVue } from '@vue/test-utils'
import AboutUsCards from "@/components/AboutUsCards.vue"

const localVue = createLocalVue()

describe('AboutUsCards.vue', () => {

  let vuetify

  beforeEach(() => {
    vuetify = new Vuetify()
  })

  it('Includes three cards', () => {
    const wrapper = shallowMount(AboutUsCards, {
      localVue,
      vuetify,
    })
    const cards = wrapper.findAll('v-card-stub')
    const titles = [
      "Un service public",
      "Sur le terrain !",
      "Une équipe autonome",
    ]

    titles.forEach(title => {
      expect(cards.filter(x => x.find('v-card-title-stub').text() === title).length).toBe(1)
    })
  })
})
