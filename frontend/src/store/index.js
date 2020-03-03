import Vue from 'vue'
import Vuex from 'vuex'
import createPersistedState from 'vuex-persistedstate'
import Constants from '@/constants'
import formutils from '@/formutils'
import jsonCases from "../resources/cases.json"

Vue.use(Vuex)

const dataVersion = '1'
const headers = {
  'X-CSRFToken': window.CSRF_TOKEN || '',
  'Content-Type': 'application/json',
}

export default new Vuex.Store({
  plugins: [createPersistedState({ key: 'vuex-' + dataVersion })],
  state: {
    cases: jsonCases,
    selectedFarmer: null,
    selectedDepartment: null,

    formDefinitionsLoadingStatus: Constants.LoadingStatus.IDLE,
    suggestionsLoadingStatus: Constants.LoadingStatus.IDLE,
    statsLoadingStatus: Constants.LoadingStatus.IDLE,
    contactLoadingStatus: Constants.LoadingStatus.IDLE,
    implementationLoadingStatus: Constants.LoadingStatus.IDLE,
    categoriesLoadingStatus: Constants.LoadingStatus.IDLE,

    hasContributed: false,

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
    defaultPracticeImageUrl: "https://images.unsplash.com/photo-1502082553048-f009c37129b9?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=1350&q=80",
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
    SET_HAS_CONTRIBUTED(state, { hasContributed }) {
      state.hasContributed = hasContributed
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
    RESET_CONTACT_LOADING_STATUS(state) {
      state.contactLoadingStatus = Constants.LoadingStatus.IDLE
    },
    RESET_LOADERS(state) {
      state.formDefinitionsLoadingStatus = Constants.LoadingStatus.IDLE
      state.suggestionsLoadingStatus = Constants.LoadingStatus.IDLE
      state.statsLoadingStatus = Constants.LoadingStatus.IDLE
      state.contactLoadingStatus = Constants.LoadingStatus.IDLE
      state.implementationLoadingStatus = Constants.LoadingStatus.IDLE
      state.categoriesLoadingStatus = Constants.LoadingStatus.IDLE
    },
    SET_SELECTED_FARMER(state, { selectedFarmer }) {
      state.selectedFarmer = selectedFarmer
    },
    SET_SELECTED_DEPARTMENT(state, { selectedDepartment }) {
      state.selectedDepartment = selectedDepartment
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
    sendContactData(context) { // From contact page
      context.commit('SET_CONTACT_LOADING', Constants.LoadingStatus.LOADING)
      Vue.http.post('api/v1/sendTask', this.getters.contactPayload, { headers }).then(() => {
        context.commit('SET_CONTACT_LOADING', Constants.LoadingStatus.SUCCESS)
      }).catch(() => {
        context.commit('SET_CONTACT_LOADING', Constants.LoadingStatus.ERROR)
      })
    },
    sendUsageData(context) { // From form usage
      context.commit('SET_CONTACT_LOADING', Constants.LoadingStatus.LOADING)
      Vue.http.post('api/v1/sendTask', this.getters.usagePayload, { headers }).then(() => {
        context.commit('SET_CONTACT_LOADING', Constants.LoadingStatus.SUCCESS)
      }).catch(() => {
        context.commit('SET_CONTACT_LOADING', Constants.LoadingStatus.ERROR)
      })
    },
    sendContributionInfo(context) { // From contribute prompt
      context.commit('SET_CONTACT_LOADING', Constants.LoadingStatus.LOADING)
      Vue.http.post('api/v1/sendTask', this.getters.contributionPayload, { headers }).then(() => {
        context.commit('SET_CONTACT_LOADING', Constants.LoadingStatus.SUCCESS)
      }).catch(() => {
        context.commit('SET_CONTACT_LOADING', Constants.LoadingStatus.ERROR)
      })
    },
    registerUserContribution(context) {
      context.commit('SET_HAS_CONTRIBUTED', { hasContributed: true })
    },
    sendImplementation(context, { practice }) { // From implement a practice
      context.commit('SET_IMPLEMENTATION_LOADING', Constants.LoadingStatus.LOADING)
      let payload = this.getters.implementationPayload
      payload.practice_id = practice.external_id
      Vue.http.post('api/v1/sendTask', payload, { headers }).then(() => {
        context.commit('SET_IMPLEMENTATION_LOADING', Constants.LoadingStatus.SUCCESS)
      }).catch(() => {
        context.commit('SET_IMPLEMENTATION_LOADING', Constants.LoadingStatus.ERROR)
      })
    },
    discardContributionPrompt(context) {
      context.commit('SET_HAS_CONTRIBUTED', { hasContributed: true })
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
    resetImplementationForm(context) {
      context.commit('SET_IMPLEMENTATION_FORM_DATA', { fieldId: 'implementationReason', fieldValue: [] })
      context.commit('SET_IMPLEMENTATION_LOADING', Constants.LoadingStatus.IDLE)
    },
    resetContactLoadingStatus(context) {
      context.commit('RESET_CONTACT_LOADING_STATUS')
    },
    resetLoaders(context) {
      context.commit('RESET_LOADERS')
    },
    setSelectedFarmer(context, { farmer }) {
      context.commit('SET_SELECTED_FARMER', { selectedFarmer: farmer })
    },
    setSelectedDepartment(context, { department }) {
      context.commit('SET_SELECTED_DEPARTMENT', { selectedDepartment: department })
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
        name: (state.contactFormData ? state.contactFormData.name : '') + ' [IMPLEMENTATION PRATIQUE]',
        phone_number: state.contactFormData ? state.contactFormData.phone : '',
        problem: reasons.join(', ')
      }
    },
    contactPayload(state, getters) {
      return {
        email: state.contactFormData ? state.contactFormData.email : '',
        name: (state.contactFormData ? state.contactFormData.name : '') + ' [PARTAGE CONTACT]',
        phone_number: state.contactFormData ? state.contactFormData.phone : '',
        answers: getters.humanReadableMiaAnswers + '\n' + getters.humanReadableStatsAnswers,
        reason: 'A partagé ses coordonnées pour être contacté',
        practice_id: '',
      }
    },
    usagePayload(state, getters) {
      return {
        email: state.contactFormData ? state.contactFormData.email : '',
        name: (state.contactFormData ? state.contactFormData.name : '') + ' [UTILISATION FORMULAIRE]',
        phone_number: state.contactFormData ? state.contactFormData.phone : '',
        answers: getters.humanReadableMiaAnswers + '\n' + getters.humanReadableStatsAnswers,
        reason: 'A répondu au formulaire depuis l\'application web',
        practice_id: '',
      }
    },
    contributionPayload(state, getters) {
      return {
        email: state.contactFormData ? state.contactFormData.email : '',
        name: (state.contactFormData ? state.contactFormData.name : '') + ' [CONTRIBUTION]',
        phone_number: state.contactFormData ? state.contactFormData.phone : '',
        answers: getters.humanReadableMiaAnswers + '\n' + getters.humanReadableStatsAnswers,
        reason: 'A partagé ses coordonnées pour être contacté',
        practice_id: '',
      }
    },
    statsPayload(state) {
      return {
        groups: state.statsFormData ? state.statsFormData.groups : [],
        referers: state.statsFormData ? state.statsFormData.referers : [],
      }
    },
    humanReadableMiaAnswers(state) {
      return formutils.getHumanReadableAnswers(state.miaFormDefinition.schema, state.miaFormDefinition.options, state.miaFormData)
    },
    humanReadableStatsAnswers(state) {
      return formutils.getHumanReadableAnswers(state.statsFormDefinition.schema, state.statsFormDefinition.options, state.statsFormData)
    },
    practiceWithShortTitle(state) {
      // TODO: this is only while we have all practices in a state property
      // TODO: we should fetch the practice if we don't have it
      return (practiceShortTitle => {
        let suggestion = state.suggestions.find(x => x.practice.short_title === practiceShortTitle)
        if (suggestion)
          return suggestion.practice

        for (let i = 0; i < state.categories.length; i++) {
          const category = state.categories[i]
          let practice = category.practices.find(x => x.short_title === practiceShortTitle)
          if (practice)
            return practice
        }
        return undefined
      })
    },
    farmerWithName(state) {
      return (farmerName => state.cases.find(x => x.name === farmerName))
    }
  }
})
