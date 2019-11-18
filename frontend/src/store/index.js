import Vue from 'vue'
import Vuex from 'vuex'
import Constants from '@/constants'

Vue.use(Vuex)

export default new Vuex.Store({
  state: {
    formDefinitionsLoadingStatus: Constants.LoadingStatus.LOADING,

    miaFormDefinition: {},
    statsFormDefinition: {},
    contactFormDefinition: {},

    miaFormData: {},
    statsFormData: {},
    contactFormData: {},
  },
  mutations: {
    SET_FORM_SCHEMAS_LOADING(state, status) {
      state.formDefinitionsLoadingStatus = status
    },
    SET_FORM_SCHEMAS(state, formDefinitions) {
      state.miaFormDefinition = formDefinitions['practices_form'] || {}
      state.statsFormDefinition = formDefinitions['stats_form'] || {}
      state.contactFormDefinition = formDefinitions['contact_form'] || {}
    },
    SET_MIA_FORM_DATA(state, {fieldId, fieldValue}) {
      state.miaFormData[fieldId] = fieldValue
    },
    SET_STATS_FORM_DATA(state, {fieldId, fieldValue}) {
      state.statsFormData[fieldId] = fieldValue
    },
    SET_CONTACT_FORM_DATA(state, {fieldId, fieldValue}) {
      state.contactFormData[fieldId] = fieldValue
    },
  },
  actions: {
    fetchFormDefinitions(context) {
      context.commit('SET_FORM_SCHEMAS_LOADING', Constants.LoadingStatus.LOADING)
      Vue.http.get('api/v1/formSchema').then(response => {
        if (!response || response.status < 200 || response.status >= 300) {
          context.commit('SET_FORM_SCHEMAS_LOADING', Constants.LoadingStatus.ERROR)
        }
        context.commit('SET_FORM_SCHEMAS_LOADING', Constants.LoadingStatus.SUCCESS)
        context.commit('SET_FORM_SCHEMAS', response.body)
      })
    },
    addMiaFormData(context, {fieldId, fieldValue}) {
      context.commit('SET_MIA_FORM_DATA', {fieldId: fieldId, fieldValue: fieldValue})
    },
    addStatsFormData(context, {fieldId, fieldValue}) {
      context.commit('SET_STATS_FORM_DATA', {fieldId: fieldId, fieldValue: fieldValue})
    },
    addContactFormData(context, {fieldId, fieldValue}) {
      context.commit('SET_CONTACT_FORM_DATA', {fieldId: fieldId, fieldValue: fieldValue})
    },
  },
  modules: {
  }
})
