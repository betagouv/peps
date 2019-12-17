import Vue from 'vue'
import Vuex from 'vuex'
import createPersistedState from 'vuex-persistedstate'
import Constants from '@/constants'
import formutils from '@/formutils'

Vue.use(Vuex)

const dataVersion = '1'
const headers = {
  'X-CSRFToken': window.CSRF_TOKEN || '',
  'Content-Type': 'application/json',
}

export default new Vuex.Store({
  plugins: [createPersistedState({ key: 'vuex-' + dataVersion })],
  state: {
    formDefinitionsLoadingStatus: Constants.LoadingStatus.IDLE,
    suggestionsLoadingStatus: Constants.LoadingStatus.IDLE,
    statsLoadingStatus: Constants.LoadingStatus.IDLE,
    contactLoadingStatus: Constants.LoadingStatus.IDLE,
    implementationLoadingStatus: Constants.LoadingStatus.IDLE,
    categoriesLoadingStatus: Constants.LoadingStatus.IDLE,

    miaFormDefinition: {},
    statsFormDefinition: {},
    contactFormDefinition: {},

    miaFormData: {},
    statsFormData: {},
    contactFormData: {},

    implementationFormData: {},

    suggestions: [],
    blacklist: [],

    categories: [],
  },
  mutations: {
    SET_FORM_SCHEMAS_LOADING(state, status) {
      state.formDefinitionsLoadingStatus = status
    },
    SET_SUGGESTIONS_LOADING(state, status) {
      state.suggestionsLoadingStatus = status
    },
    SET_STATS_LOADING(state, status) {
      state.statsLoadingStatus = status
    },
    SET_CONTACT_LOADING(state, status) {
      state.contactLoadingStatus = status
    },
    SET_IMPLEMENTATION_LOADING(state, status) {
      state.implementationLoadingStatus = status
    },
    SET_CATEGORIES_LOADING(state, status) {
      state.categoriesLoadingStatus = status
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
    SET_IMPLEMENTATION_FORM_DATA(state, { fieldId, fieldValue }) {
      Vue.set(state.implementationFormData, fieldId, fieldValue)
    },
    SET_SUGGESTIONS(state, suggestions) {
      state.suggestions = suggestions
    },
    SET_CATEGORIES(state, categories) {
      state.categories = categories
    },
    ADD_TO_BLACKLIST(state, { practice }) {
      const blacklisted_ids = state.blacklist.map(x => x.id)
      if (blacklisted_ids.indexOf(practice.id) === -1)
        state.blacklist.push(practice)
    },
    REMOVE_FROM_BLACKLIST(state, { practice }) {
      const blacklisted_ids = state.blacklist.map(x => x.id)
      const index = blacklisted_ids.indexOf(practice.id)
      if (index !== -1)
        state.blacklist.splice(index, 1)
    },
    RESET_LOADERS(state) {
      state.formDefinitionsLoadingStatus = Constants.LoadingStatus.IDLE
      state.suggestionsLoadingStatus = Constants.LoadingStatus.IDLE
      state.statsLoadingStatus = Constants.LoadingStatus.IDLE
      state.contactLoadingStatus = Constants.LoadingStatus.IDLE
      state.implementationLoadingStatus = Constants.LoadingStatus.IDLE
      state.categoriesLoadingStatus = Constants.LoadingStatus.IDLE
    }
  },
  actions: {
    fetchFormDefinitions(context) {
      context.commit('SET_FORM_SCHEMAS_LOADING', Constants.LoadingStatus.LOADING)
      Vue.http.get('api/v1/formSchema').then(response => {
        context.commit('SET_FORM_SCHEMAS_LOADING', Constants.LoadingStatus.SUCCESS)
        context.commit('SET_FORM_SCHEMAS', response.body)
      }).catch(() => {
        context.commit('SET_FORM_SCHEMAS_LOADING', Constants.LoadingStatus.ERROR)
      })
    },
    fetchSuggestions(context) {
      context.commit('SET_SUGGESTIONS_LOADING', Constants.LoadingStatus.LOADING)
      Vue.http.post('api/v1/calculateRankings', this.getters.suggestionsPayload, { headers }).then(response => {
        context.commit('SET_SUGGESTIONS_LOADING', Constants.LoadingStatus.SUCCESS)
        context.commit('SET_SUGGESTIONS', response.body.suggestions)
      }).catch(() => {
        context.commit('SET_SUGGESTIONS_LOADING', Constants.LoadingStatus.ERROR)
      })
    },
    fetchCategories(context) {
      context.commit('SET_CATEGORIES_LOADING', Constants.LoadingStatus.LOADING)
      Vue.http.get('api/v1/categories').then(response => {
        context.commit('SET_CATEGORIES_LOADING', Constants.LoadingStatus.SUCCESS)
        context.commit('SET_CATEGORIES', response.body)
      }).catch(() => {
        context.commit('SET_CATEGORIES_LOADING', Constants.LoadingStatus.ERROR)
      })
    },
    sendStatsData(context) {
      context.commit('SET_STATS_LOADING', Constants.LoadingStatus.LOADING)
      Vue.http.post('api/v1/stats', this.getters.statsPayload, { headers }).then(() => {
        context.commit('SET_STATS_LOADING', Constants.LoadingStatus.SUCCESS)
      }).catch(() => {
        context.commit('SET_STATS_LOADING', Constants.LoadingStatus.ERROR)
      })
    },
    sendContactData(context) {
      context.commit('SET_CONTACT_LOADING', Constants.LoadingStatus.LOADING)
      Vue.http.post('api/v1/sendTask', this.getters.contactPayload, { headers }).then(() => {
        context.commit('SET_CONTACT_LOADING', Constants.LoadingStatus.SUCCESS)
      }).catch(() => {
        context.commit('SET_CONTACT_LOADING', Constants.LoadingStatus.ERROR)
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
    addImplementationFormData(context, { fieldId, fieldValue }) {
      context.commit('SET_IMPLEMENTATION_FORM_DATA', { fieldId: fieldId, fieldValue: fieldValue })
    },
    blacklistPractice(context, { practice }) {
      context.commit('ADD_TO_BLACKLIST', { practice: practice })
    },
    removeFromBlacklist(context, { practice }) {
      context.commit('REMOVE_FROM_BLACKLIST', { practice: practice })
    },
    sendImplementation(context, { practice }) {
      context.commit('SET_IMPLEMENTATION_LOADING', Constants.LoadingStatus.LOADING)
      let payload = this.getters.implementationPayload
      payload.practice_id = practice.external_id
      Vue.http.post('api/v1/sendTask', payload, { headers }).then(() => {
        context.commit('SET_IMPLEMENTATION_LOADING', Constants.LoadingStatus.SUCCESS)
      }).catch(() => {
        context.commit('SET_IMPLEMENTATION_LOADING', Constants.LoadingStatus.ERROR)
      })
    },
    resetImplementationForm(context) {
      context.commit('SET_IMPLEMENTATION_FORM_DATA', { fieldId: 'implementationReason', fieldValue: [] })
      context.commit('SET_IMPLEMENTATION_LOADING', Constants.LoadingStatus.IDLE)
    },
    resetLoaders(context) {
      context.commit('RESET_LOADERS')
    }
  },
  modules: {
  },
  getters: {
    formsAreComplete(state) {
      if (Object.keys(state.miaFormDefinition).length === 0 && Object.keys(state.statsFormDefinition).length === 0 && Object.keys(state.contactFormDefinition).length === 0) {
        return false
      }
      const miaFormIsComplete = formutils.formIsComplete(state.miaFormDefinition.schema, state.miaFormDefinition.options, state.miaFormData)
      const statsFormIsComplete = formutils.formIsComplete(state.statsFormDefinition.schema, state.statsFormDefinition.options, state.statsFormData)
      const contactFormIsComplete = formutils.formIsComplete(state.contactFormDefinition.schema, state.contactFormDefinition.options, state.contactFormData)
      return miaFormIsComplete && statsFormIsComplete && contactFormIsComplete
    },
    suggestionsPayload(state) {
      return { answers: state.miaFormData, practice_blacklist: state.blacklist.map(x => x.id) }
    },
    implementationPayload(state, getters) {
      const reasons = state.implementationFormData ? state.implementationFormData.implementationReason || [] : []
      return {
        answers: getters.humanReadableMiaAnswers + '\n' + getters.humanReadableStatsAnswers,
        email: state.contactFormData ? state.contactFormData.email : '',
        name: state.contactFormData ? state.contactFormData.name : '',
        phone_number: state.contactFormData ? state.contactFormData.phone : '',
        problem: reasons.join(', ')
      }
    },
    statsPayload(state) {
      return {
        groups: state.statsFormData ? state.statsFormData.groups : [],
        referers: state.statsFormData ? state.statsFormData.referers : [],
      }
    },
    contactPayload(state, getters) {
      return {
        email: state.contactFormData ? state.contactFormData.email : '',
        name: state.contactFormData ? state.contactFormData.name : '',
        phone_number: state.contactFormData ? state.contactFormData.phone : '',
        answers: getters.humanReadableMiaAnswers + '\n' + getters.humanReadableStatsAnswers,
        reason: 'A répondu depuis l\'application Web',
        practice_id: '',
      }
    },
    humanReadableMiaAnswers(state) {
      return formutils.getHumanReadableAnswers(state.miaFormDefinition.schema, state.miaFormDefinition.options, state.miaFormData)
    },
    humanReadableStatsAnswers(state) {
      return formutils.getHumanReadableAnswers(state.statsFormDefinition.schema, state.statsFormDefinition.options, state.statsFormData)
    },
    practiceWithId(state) {
      // TODO: this is only while we have all practices in a state property
      return (practiceId => {
        let practice = state.suggestions.find(x => x.id === practiceId)
        if (practice)
          return practice
        
        for (let i = 0; i < state.categories.length; i++) {
          const category = state.categories[i]
          practice = category.practices.find(x => x.id === practiceId)
          if (practice)
            return practice
        }
        return undefined
      })
    }
  }
})
