import Vue from 'vue'
import Vuex from 'vuex'
import createPersistedState from 'vuex-persistedstate'
import Constants from '@/constants'
import short from 'short-uuid'

Vue.use(Vuex)

const dataVersion = '3'
const headers = {
  'X-CSRFToken': window.CSRF_TOKEN || '',
  'Content-Type': 'application/json',
}

function addFarmerFieldsToExperiment(experiment, farmer) {
  experiment.farmer_name = farmer.name
  experiment.farmer_url_slug = `${farmer.farm_name || farmer.name}--${farmer.sequence_number}` // TODO - refactor duplicate code
  experiment.postal_code = farmer.postal_code
  experiment.agriculture_types = farmer.agriculture_types
  experiment.livestock_types = farmer.livestock_types
}

export default new Vuex.Store({
  plugins: [createPersistedState({ 
    key: 'vuex-' + dataVersion,
    reducer: state => ({
      geojson: state.geojson,
      xpPaginationPage: state.xpPaginationPage,
      xpSelectionFilters: state.xpSelectionFilters,
      selectedFarmerId: state.selectedFarmerId,
    }),
  })],
  state: {
    farmers: [],
    farmerBriefs: [],
    experimentBriefs: [],
    selectedFarmerId: null,
    selectedDepartment: null,
    loggedUser: null,
    geojson: null,
    stats: null,
    themes: [],

    contactLoadingStatus: Constants.LoadingStatus.IDLE,
    farmersLoadingStatus: Constants.LoadingStatus.IDLE,
    experimentBriefsLoadingStatus: Constants.LoadingStatus.IDLE,
    experimentEditLoadingStatus: Constants.LoadingStatus.IDLE,
    farmerEditLoadingStatus: Constants.LoadingStatus.IDLE,
    loggedUserLoadingStatus: Constants.LoadingStatus.IDLE,
    geojsonLoadingStatus: Constants.LoadingStatus.IDLE,
    messagesLoadingStatus: Constants.LoadingStatus.IDLE,
    themesLoadingStatus: Constants.LoadingStatus.IDLE,

    messages: [],
    lastMessagesRequest: null,

    defaultPracticeImageUrl: "https://images.unsplash.com/photo-1502082553048-f009c37129b9?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=1350&q=80",
    xpPaginationPage: 1,
    xpSelectionFilters: {
      tags: [],
      departments: [],
      agricultureTypes: [],
      cultures: [],
      livestock: false
    },

    lastContactInfo: {},
  },
  mutations: {
    SET_CONTACT_LOADING(state, status) {
      state.contactLoadingStatus = status
    },
    SET_FARMERS_LOADING(state, status) {
      state.farmersLoadingStatus = status
    },
    SET_FARMER_BRIEFS_LOADING(state, status) {
      state.farmersLoadingStatus = status
    },
    SET_EXPERIMENT_BRIEFS_LOADING(state, status) {
      state.experimentBriefsLoadingStatus = status
    },
    SET_FARMERS(state, farmers) {
      state.farmers = farmers
    },
    SET_FARMER_BRIEFS(state, farmerBriefs) {
      state.farmerBriefs = farmerBriefs
    },
    SET_EXPERIMENT_BRIEFS(state, experimentBriefs) {
      state.experimentBriefs = experimentBriefs
    },
    RESET_CONTACT_LOADING_STATUS(state) {
      state.contactLoadingStatus = Constants.LoadingStatus.IDLE
    },
    RESET_LOADERS(state) {
      state.contactLoadingStatus = Constants.LoadingStatus.IDLE
      state.farmersLoadingStatus = Constants.LoadingStatus.IDLE
      state.experimentEditLoadingStatus = Constants.LoadingStatus.IDLE
      state.farmerEditLoadingStatus = Constants.LoadingStatus.IDLE
      state.messagesLoadingStatus = Constants.LoadingStatus.IDLE
      state.themesLoadingStatus = Constants.LoadingStatus.IDLE
      state.experimentBriefsLoadingStatus = Constants.LoadingStatus.IDLE
    },
    RESET_MESSAGES_LOADING_STATUS(state){
      state.messagesLoadingStatus = Constants.LoadingStatus.IDLE
    },
    SET_SELECTED_FARMER(state, { farmerId }) {
      state.selectedFarmerId = farmerId
    },
    SET_SELECTED_DEPARTMENT(state, { selectedDepartment }) {
      state.selectedDepartment = selectedDepartment
    },
    SET_LOGGED_USER(state, loggedUser) {
      state.loggedUser = loggedUser
    },
    SET_LOGGED_USER_LOADING_STATUS(state, status) {
      state.loggedUserLoadingStatus = status
    },
    SET_EXPERIMENT_EDIT_LOADING_STATUS(state, status) {
      state.experimentEditLoadingStatus = status
    },
    SET_FARMER_EDIT_LOADING_STATUS(state, status) {
      state.farmerEditLoadingStatus = status
    },
    UPDATE_XP(state, newExperiment) {
      for (let i = 0; i < state.farmers.length; i++) {
        const farmer = state.farmers[i]
        const experimentIndex = farmer.experiments.findIndex(x => x.id === newExperiment.id)
        if (experimentIndex > -1) {
          addFarmerFieldsToExperiment(newExperiment, farmer)
          farmer.experiments[experimentIndex] = newExperiment
          break
        }
      }
    },
    UPDATE_FARMER(state, updatedFarmer) {
      const farmerIndex = state.farmers.findIndex(x => x.id === updatedFarmer.id)
      if (farmerIndex > -1) {
        if (updatedFarmer.experiments)
          updatedFarmer.experiments.forEach(y => addFarmerFieldsToExperiment(y, updatedFarmer))
        state.farmers.splice(farmerIndex, 1, updatedFarmer)
      }
    },
    ADD_FARMER(state, newFarmer) {
      const farmerIndex = state.farmers.findIndex(x => x.id === newFarmer.id)
      if (farmerIndex === -1) {
        if (newFarmer.experiments)
          newFarmer.experiments.forEach(y => addFarmerFieldsToExperiment(y, newFarmer))
        state.farmers.push(newFarmer)
      }
    },
    ADD_XP_TO_FARMER(state, { newExperiment, farmer }) {
      farmer.experiments = farmer.experiments || []
      addFarmerFieldsToExperiment(newExperiment, farmer)
      farmer.experiments.push(newExperiment)
    },
    UPDATE_PAGINATION(state, page) {
      state.xpPaginationPage = page
    },
    UPDATE_FILTERS(state, filters) {
      Vue.set(state, 'xpSelectionFilters', filters)
    },
    SET_GEOJSON(state, geojson) {
      Vue.set(state, 'geojson', geojson)
    },
    SET_GEOJSON_LOADING_STATUS(state, status) {
      state.geojsonLoadingStatus = status
    },
    SET_LAST_CONTACT_INFO(state, contactInfo) {
      Vue.set(state, 'lastContactInfo', contactInfo)
    },
    SET_MESSAGES(state, messages) {
      Vue.set(state, 'messages', messages)
    },
    ADD_MESSAGE(state, message) {
      state.messages.push(message)
    },
    MERGE_MESSAGES(state, messages) {
      for (let i = 0; i < messages.length; i++) {
        const serverMessage = messages[i]
        const index = state.messages.findIndex(x => x.id === serverMessage.id)
        if (index > -1) {
          state.messages.splice(index, 1, serverMessage)
        } else {
          state.messages.push(serverMessage)
        }
      }
    },
    SET_MESSAGES_LOADING_STATUS(state, status) {
      state.messagesLoadingStatus = status
    },
    SET_THEMES_LOADING_STATUS(state, status) {
      state.themesLoadingStatus = status
    },
    MARK_AS_READ(state, messages) {
      for (let i = 0; i < messages.length; i++) {
        const message = state.messages.find(x => x.id === messages[i].id)
        if (message)
          message.new = false
      }
    },
    SET_LAST_MESSAGES_REQUEST(state, date) {
      state.lastMessagesRequest = date.toISOString()
    },
    SET_STATS(state, stats) {
      state.stats = stats
    },
    SET_THEMES(state, themes) {
      state.themes = themes
    }
  },
  actions: {
    fetchFarmersAndExperiments(context) {
      context.commit('SET_FARMERS_LOADING', Constants.LoadingStatus.LOADING)
      Vue.http.get('/api/v1/farmers').then(response => {
        const body = response.body
        body.forEach(x => {
          if (x.experiments)
            x.experiments.forEach(y => addFarmerFieldsToExperiment(y, x))
        })
        context.commit('SET_FARMERS', body)
        context.commit('SET_FARMERS_LOADING', Constants.LoadingStatus.SUCCESS)
      }).catch(() => {
        context.commit('SET_FARMERS_LOADING', Constants.LoadingStatus.ERROR)
      })
    },
    fetchExperimentBriefs(context) {
      context.commit('SET_EXPERIMENT_BRIEFS_LOADING', Constants.LoadingStatus.LOADING)
      Vue.http.get('/api/v1/experimentBriefs').then(response => {
        const body = response.body
        context.commit('SET_EXPERIMENT_BRIEFS', body)
        context.commit('SET_EXPERIMENT_BRIEFS_LOADING', Constants.LoadingStatus.SUCCESS)
      }).catch(() => {
        context.commit('SET_EXPERIMENT_BRIEFS_LOADING', Constants.LoadingStatus.ERROR)
      })
    },
    fetchLoggedUser(context) {
      context.commit('SET_LOGGED_USER_LOADING_STATUS', Constants.LoadingStatus.LOADING)
      Vue.http.get('/api/v1/loggedUser').then(response => {
        context.commit('SET_LOGGED_USER', response.body)
        Vue.http.get('/api/v1/farmers/' + response.body.farmer_sequence_number).then(farmer => {
          context.commit('ADD_FARMER', farmer.body)
          context.commit('SET_LOGGED_USER_LOADING_STATUS', Constants.LoadingStatus.SUCCESS)
        })
      }).catch(() => {
        context.commit('SET_LOGGED_USER', null)
        context.commit('SET_LOGGED_USER_LOADING_STATUS', Constants.LoadingStatus.ERROR)
      })
    },
    fetchThemes(context) {
      context.commit('SET_THEMES_LOADING_STATUS', Constants.LoadingStatus.LOADING)
      Vue.http.get('/api/v1/themes').then(response => {
        const body = response.body
        context.commit('SET_THEMES', body)
        context.commit('SET_THEMES_LOADING_STATUS', Constants.LoadingStatus.SUCCESS)
      }).catch(() => {
        context.commit('SET_THEMES_LOADING_STATUS', Constants.LoadingStatus.ERROR)
      })
    },
    sendContactData(context, { name, email, phoneNumber }) { // From contact page
      context.commit('SET_LAST_CONTACT_INFO', { name, email, phoneNumber })
      let reason = 'A partagé ses coordonnées pour être contacté'
      let payload = { email, name: name + ' [PARTAGE CONTACT]', phone_number: phoneNumber, reason: reason }
      context.commit('SET_CONTACT_LOADING', Constants.LoadingStatus.LOADING)
      Vue.http.post('/api/v1/sendTask', payload, { headers }).then(() => {
        context.commit('SET_CONTACT_LOADING', Constants.LoadingStatus.SUCCESS)
      }).catch(() => {
        context.commit('SET_CONTACT_LOADING', Constants.LoadingStatus.ERROR)
      })
    },
    sendShareXPDataTask(context, { experimentTitle, experimentDescription, name, email, phone }) {
      const payload = {
        email: email,
        name: name + ' [PARTAGE XP SANS CRÉATION DE COMPTE]',
        phone_number: phone,
        reason: 'Veut partager un retour d\'expérience sans créer un compte',
        problem: `Partage de l'expérience "${experimentTitle}" : ${experimentDescription}`
      }
      context.commit('SET_CONTACT_LOADING', Constants.LoadingStatus.LOADING)
      Vue.http.post('/api/v1/sendTask', payload, { headers }).then(() => {
        context.commit('SET_CONTACT_LOADING', Constants.LoadingStatus.SUCCESS)
      }).catch(() => {
        context.commit('SET_CONTACT_LOADING', Constants.LoadingStatus.ERROR)
      })
    },
    sendFarmerContactRequest(context, { farmer, name, email, phoneNumber }) { // From farmer contact prompt
      context.commit('SET_LAST_CONTACT_INFO', { name, email, phoneNumber })

      let payload = { email, name: name + ' [CONTACT AGRI]', phone_number: phoneNumber }
      payload.reason = 'Veut se mettre en contact avec ' + farmer.name + ' (' + farmer.id + ')'

      context.commit('SET_CONTACT_LOADING', Constants.LoadingStatus.LOADING)
      Vue.http.post('/api/v1/sendTask', payload, { headers }).then(() => {
        context.commit('SET_CONTACT_LOADING', Constants.LoadingStatus.SUCCESS)
      }).catch(() => {
        context.commit('SET_CONTACT_LOADING', Constants.LoadingStatus.ERROR)
      })
    },
    resetContactLoadingStatus(context) {
      context.commit('RESET_CONTACT_LOADING_STATUS')
    },
    resetLoaders(context) {
      context.commit('RESET_LOADERS')
    },
    resetMessagesLoadingStatus(context) {
      context.commit('RESET_MESSAGES_LOADING_STATUS')
    },
    setSelectedFarmer(context, { farmerId }) {
      context.commit('SET_SELECTED_FARMER', { farmerId })
    },
    setSelectedDepartment(context, { department }) {
      context.commit('SET_SELECTED_DEPARTMENT', { selectedDepartment: department })
    },
    patchExperiment(context, { experiment, changes }) {
      context.commit('SET_EXPERIMENT_EDIT_LOADING_STATUS', Constants.LoadingStatus.LOADING)
      Vue.http.patch('/api/v1/experiments/' + experiment.id, changes, { headers }).then(response => {
        context.commit('SET_EXPERIMENT_EDIT_LOADING_STATUS', Constants.LoadingStatus.SUCCESS)
        context.commit('UPDATE_XP', response.body)
      }).catch(() => {
        context.commit('SET_EXPERIMENT_EDIT_LOADING_STATUS', Constants.LoadingStatus.ERROR)
      })
    },
    createExperiment(context, { payload, farmer }) {
      context.commit('SET_EXPERIMENT_EDIT_LOADING_STATUS', Constants.LoadingStatus.LOADING)
      Vue.http.post('/api/v1/experiments/', payload, { headers }).then(response => {
        context.commit('SET_EXPERIMENT_EDIT_LOADING_STATUS', Constants.LoadingStatus.SUCCESS)
        context.commit('ADD_XP_TO_FARMER', { newExperiment: response.body, farmer: farmer })
      }).catch(() => {
        context.commit('SET_EXPERIMENT_EDIT_LOADING_STATUS', Constants.LoadingStatus.ERROR)
      })
    },
    resetExperimentEditLoadingStatus(context) {
      context.commit('SET_EXPERIMENT_EDIT_LOADING_STATUS', Constants.LoadingStatus.IDLE)
    },
    patchFarmer(context, { farmer, changes }) {
      context.commit('SET_FARMER_EDIT_LOADING_STATUS', Constants.LoadingStatus.LOADING)
      Vue.http.patch('/api/v1/farmers/' + farmer.id, changes, { headers }).then(response => {
        context.commit('SET_FARMER_EDIT_LOADING_STATUS', Constants.LoadingStatus.SUCCESS)
        context.commit('UPDATE_FARMER', response.body)
      }).catch(() => {
        context.commit('SET_FARMER_EDIT_LOADING_STATUS', Constants.LoadingStatus.ERROR)
      })
    },
    resetFarmerEditLoadingStatus(context) {
      context.commit('SET_FARMER_EDIT_LOADING_STATUS', Constants.LoadingStatus.IDLE)
    },
    updatePagination(context, { page }) {
      context.commit('UPDATE_PAGINATION', page)
    },
    updateFilters(context, { filters }) {
      context.commit('UPDATE_FILTERS', filters)
    },
    fetchGeojson(context) {
      context.commit('SET_GEOJSON_LOADING_STATUS', Constants.LoadingStatus.LOADING)
      Vue.http.get('/api/v1/geojson').then(response => {
        context.commit('SET_GEOJSON', response.body)
        context.commit('SET_GEOJSON_LOADING_STATUS', Constants.LoadingStatus.SUCCESS)
      }).catch(() => {
        context.commit('SET_GEOJSON', null)
        context.commit('SET_GEOJSON_LOADING_STATUS', Constants.LoadingStatus.ERROR)
      })
    },
    fetchMessages(context) {
      context.commit('SET_MESSAGES_LOADING_STATUS', Constants.LoadingStatus.LOADING)
      Vue.http.get('/api/v1/messages').then(response => {
        context.commit('SET_MESSAGES', response.body)
        context.commit('SET_MESSAGES_LOADING_STATUS', Constants.LoadingStatus.SUCCESS)
        context.commit('SET_LAST_MESSAGES_REQUEST', new Date())
      }).catch(() => {
        context.commit('SET_MESSAGES', [])
        context.commit('SET_MESSAGES_LOADING_STATUS', Constants.LoadingStatus.ERROR)
      })
    },
    fetchNewMessages(context) {
      let url = '/api/v1/messages'
      if (context.state.lastMessagesRequest)
        url += `?since=${context.state.lastMessagesRequest}`
      Vue.http.get(url).then(response => {
        context.commit('MERGE_MESSAGES', response.body)
        context.commit('SET_LAST_MESSAGES_REQUEST', new Date())
      }).catch(() => {
        // Fail silently
      })
    },
    createMessage(context, {body, recipient}) {
      context.commit('SET_MESSAGES_LOADING_STATUS', Constants.LoadingStatus.LOADING)
      Vue.http.post('/api/v1/messages', {body, recipient}, { headers }).then(response => {
        context.commit('ADD_MESSAGE', response.body)
        context.commit('SET_MESSAGES_LOADING_STATUS', Constants.LoadingStatus.SUCCESS)
      }).catch(() => {
        context.commit('SET_MESSAGES_LOADING_STATUS', Constants.LoadingStatus.ERROR)
      })
    },
    markAsRead(context, {messages}) {
      const messageIds = messages.map(x => x.id)
      Vue.http.post('/api/v1/messages/markAsRead', messageIds, { headers }).then(response => {
        context.commit('MARK_AS_READ', response.body)
      }).catch(() => {
      })
    },
    fetchStats(context) {
      let url = '/api/v1/stats'
      Vue.http.get(url).then(response => {
        context.commit('SET_STATS', response.body)
      }).catch(() => {})
    }
  },
  modules: {
  },
  getters: {
    farmerWithLegacyUrlComponent(state) {
      return (farmerUrlComponent => {
        let shortenedId = farmerUrlComponent.split('__')[1]
        let uuid = short().toUUID(shortenedId)
        return state.farmers.find(x => x.id === uuid)
      })
    },
    farmerWithUrlComponent(state) {
      return (farmerUrlComponent => {
        let sequenceNumber = parseInt(farmerUrlComponent.split('--')[1])
        if (!isNaN(sequenceNumber))
          return state.farmers.find(x => x.sequence_number === sequenceNumber)
      })
    },
    experimentWithLegacyUrlComponent() {
      return ((farmer, experimentUrlComponent) => {
        let shortenedId = experimentUrlComponent.split('__')[1]
        let uuid = short().toUUID(shortenedId)
        return farmer.experiments.find(x => x.id === uuid)
      })
    },
    experimentWithUrlComponent() {
      return ((farmer, experimentUrlComponent) => {
        let sequenceNumber = parseInt(experimentUrlComponent.split('--')[1])
        if (!isNaN(sequenceNumber))
          return farmer.experiments.find(x => x.sequence_number === sequenceNumber)
      })
    },
    farmerWithId(state) {
      return (farmerId => state.farmers.find(x => x.id === farmerId))
    },
    farmerUrlComponent() {
      return (farmer => `${farmer.farm_name || farmer.name}--${farmer.sequence_number}`)
    },
    experimentUrlComponent() {
      return (experiment => `${experiment.short_name || experiment.name}--${experiment.sequence_number}`)
    },
    selectedFarmer(state) {
      return state.farmerBriefs.find(x => x.id === state.selectedFarmerId)
    },
    experiments(state) {
      return state.farmers.flatMap(x => x.experiments).filter(x => !!x).sort((a, b) => {
        if (a.modification_date < b.modification_date)
          return 1
        if (a.modification_date > b.modification_date)
          return -1
        return 0
      })
    },
    experimentBriefs(state) {
      return state.experimentBriefs.sort((a, b) => {
        if (a.modification_date < b.modification_date)
          return 1
        if (a.modification_date > b.modification_date)
          return -1
        return 0
      })
    },
    hasUnreadMessages(state) {
      const loggedUser = state.loggedUser
      if (!loggedUser)
        return false
      const loggedFarmerId = loggedUser.farmer_id
      if (!loggedFarmerId)
        return false
      return state.messages.some(x => x.recipient.id === loggedFarmerId && x.new)
    },
    unreadMessageCount(state) {
      const loggedUser = state.loggedUser
      if (!loggedUser)
        return 0
      const loggedFarmerId = loggedUser.farmer_id
      if (!loggedFarmerId)
        return 0
      return state.messages.filter(x => x.recipient.id === loggedFarmerId && x.new).length
    }
  }
})
