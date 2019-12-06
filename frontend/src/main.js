import Vue from 'vue'
import App from '@/App.vue'
import vuetify from '@/plugins/vuetify'
import store from '@/store'
import router from '@/router'
import VueResource from 'vue-resource'
import VueBrowserUpdate from 'vue-browserupdate'
import VueAnalytics from 'vue-analytics'

Vue.config.productionTip = false

Vue.use(VueResource)
Vue.use(VueBrowserUpdate, {
  options: {
    required: {i: 11},
    noclose: true,
  }
})

Vue.use(VueAnalytics, {
  id: 'UA-154028243-1',
  router
})

Vue.http.interceptors.push((request) => {
  request.headers['X-CSRFToken'] = window.CSRF_TOKEN
})

new Vue({
  vuetify,
  store,
  router,
  render: h => h(App)
}).$mount('#app')
