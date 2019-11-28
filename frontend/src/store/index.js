import Vue from 'vue'
import Vuex from 'vuex'
import Constants from '@/constants'
import formutils from '@/formutils'

Vue.use(Vuex)

export default new Vuex.Store({
  state: {
    formDefinitionsLoadingStatus: Constants.LoadingStatus.LOADING,
    suggestionsLoadingStatus: Constants.LoadingStatus.IDLE,

    miaFormDefinition: {},
    statsFormDefinition: {},
    contactFormDefinition: {},

    miaFormData: {},
    statsFormData: {},
    contactFormData: {},

    suggestions: [],
  },
  mutations: {
    SET_FORM_SCHEMAS_LOADING(state, status) {
      state.formDefinitionsLoadingStatus = status
    },
    SET_SUGGESTIONS_LOADING(state, status) {
      state.suggestionsLoadingStatus = status
    },
    SET_FORM_SCHEMAS(state, formDefinitions) {
      state.miaFormDefinition = formDefinitions['practices_form'] || {}
      state.statsFormDefinition = formDefinitions['stats_form'] || {}
      state.contactFormDefinition = formDefinitions['contact_form'] || {}
    },
    SET_MIA_FORM_DATA(state, { fieldId, fieldValue }) {
      Vue.set(state.miaFormData, fieldId, fieldValue)
    },
    SET_STATS_FORM_DATA(state, { fieldId, fieldValue }) {
      Vue.set(state.statsFormData, fieldId, fieldValue)
    },
    SET_CONTACT_FORM_DATA(state, { fieldId, fieldValue }) {
      Vue.set(state.contactFormData, fieldId, fieldValue)
    },
    SET_SUGGESTIONS(state, suggestions) {
      state.suggestions = suggestions
    }
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
    fetchSuggestions(context) {
      const headers = {
        'X-CSRFToken': window.CSRF_TOKEN || '',
        'Content-Type': 'application/json',
      }
      context.commit('SET_SUGGESTIONS_LOADING', Constants.LoadingStatus.LOADING)
      Vue.http.post('api/v1/calculateRankings', this.getters.suggestionsPayload, { headers }).then(response => {
        if (!response || response.status < 200 || response.status >= 300) {
          context.commit('SET_SUGGESTIONS_LOADING', Constants.LoadingStatus.ERROR)
        }
        context.commit('SET_SUGGESTIONS_LOADING', Constants.LoadingStatus.SUCCESS)
        context.commit('SET_SUGGESTIONS', response.body.suggestions)
      })
    },
    addMiaFormData(context, { fieldId, fieldValue }) {
      context.commit('SET_MIA_FORM_DATA', { fieldId: fieldId, fieldValue: fieldValue })
    },
    addStatsFormData(context, { fieldId, fieldValue }) {
      context.commit('SET_STATS_FORM_DATA', { fieldId: fieldId, fieldValue: fieldValue })
    },
    addContactFormData(context, { fieldId, fieldValue }) {
      context.commit('SET_CONTACT_FORM_DATA', { fieldId: fieldId, fieldValue: fieldValue })
    },
  },
  modules: {
  },
  getters: {
    formsAreComplete(state) {
      const miaFormIsComplete = formutils.formIsComplete(state.miaFormDefinition.schema, state.miaFormDefinition.options, state.miaFormData)
      const statsFormIsComplete = formutils.formIsComplete(state.statsFormDefinition.schema, state.statsFormDefinition.options, state.statsFormData)
      const contactFormIsComplete = formutils.formIsComplete(state.contactFormDefinition.schema, state.contactFormDefinition.options, state.contactFormData)
      return miaFormIsComplete && statsFormIsComplete && contactFormIsComplete
    },
    suggestionsPayload(state) {
      return { answers: state.miaFormData }
    }
  }
})
