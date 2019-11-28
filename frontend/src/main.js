import Vue from 'vue'
import App from '@/App.vue'
import vuetify from '@/plugins/vuetify'
import store from '@/store'
import router from '@/router'
import VueResource from 'vue-resource'

Vue.config.productionTip = false

Vue.use(VueResource)

Vue.http.interceptors.push((request) => {
  request.headers['X-CSRFToken'] = window.CSRF_TOKEN
})

new Vue({
  vuetify,
  store,
  router,
  render: h => h(App)
}).$mount('#app')
