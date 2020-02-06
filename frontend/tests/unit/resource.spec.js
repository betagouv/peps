import Vuetify from 'vuetify'
import { mount, createLocalVue } from '@vue/test-utils'
import Resource from '@/components/Resource.vue'

const localVue = createLocalVue()

describe('Resource.vue', () => {

  let vuetify

  const resource = {
    "id": "8aa7f625-200c-4f56-99cb-badf33dc84e4",
    "airtable_url": "https://airtable.com/tblVb2GDuCPGUrt35/recNcdo6nC4gC41fI/",
    "name": "Fiche action variétés de betteraves sucrières résistantes",
    "description": "Dans le dispositif des CEPP la valeur associée à une variété est reliée aux résistances qu'elles comportent.",
    "resource_type": "PDF",
    "image": "http://0.0.0.0:8000/media/atteTfvdHlXVBPL5s.jpg",
    "url": "http://www.ecophytopic.fr/sites/default/files/actualites_doc/arr%C3%AAt%C3%A9%20CEPP%2005122018-48.pdf"
  }

  beforeEach(() => {
    vuetify = new Vuetify()
  })

  it('displays the resource name', () => {
    const wrapper = mount(Resource, {
      localVue,
      vuetify,
      propsData: {
        resource: resource
      }
    })
    expect(wrapper.findAll('.resource-name').length).toBe(1)
    expect(wrapper.find('.resource-name').text()).toBe(resource.name)
  })

  it('displays the resource description', () => {
    const wrapper = mount(Resource, {
      localVue,
      vuetify,
      propsData: {
        resource: resource
      }
    })
    expect(wrapper.findAll('.resource-description').length).toBe(1)
    expect(wrapper.find('.resource-description').text()).toBe(resource.description)
  })

  it('displays the image if it has one', () => {
    const wrapper = mount(Resource, {
      localVue,
      vuetify,
      propsData: {
        resource: resource
      }
    })
    expect(wrapper.findAll('.resource-image .v-icon').length).toBe(0)
    expect(wrapper.findAll('.resource-image .v-image').length).toBe(1)
    expect(wrapper.find('.resource-image .v-image').props('src')).toBe(resource.image)
  })

  it('displays an icon if it has no image', () => {
    const resource = {
      "id": "8aa7f625-200c-4f56-99cb-badf33dc84e4",
      "airtable_url": "https://airtable.com/tblVb2GDuCPGUrt35/recNcdo6nC4gC41fI/",
      "name": "Fiche action variétés de betteraves sucrières résistantes",
      "description": "Dans le dispositif des CEPP la valeur associée à une variété est reliée aux résistances qu'elles comportent.",
      "resource_type": "PDF",
      "url": "http://www.ecophytopic.fr/sites/default/files/actualites_doc/arr%C3%AAt%C3%A9%20CEPP%2005122018-48.pdf"
    }

    const wrapper = mount(Resource, {
      localVue,
      vuetify,
      propsData: {
        resource: resource
      }
    })
    expect(wrapper.findAll('.resource-image .v-icon').length).toBe(1)
    expect(wrapper.findAll('.resource-image .v-image').length).toBe(0)
    expect(wrapper.find('.resource-image .v-icon').classes()).toContain('mdi-pdf-box')
  })

})
