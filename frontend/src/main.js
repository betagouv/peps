import Vue from 'vue'
import App from '@/App.vue'
import vuetify from '@/plugins/vuetify'
import store from '@/store'
import router from '@/router'
import VueResource from 'vue-resource'
import VueBrowserUpdate from 'vue-browserupdate'

Vue.config.productionTip = false

Vue.use(VueResource)
Vue.use(VueBrowserUpdate, {
  options: {
    required: { i: 11 },
    noclose: true,
  }
})

Vue.http.interceptors.push((request) => {
  request.headers['X-CSRFToken'] = window.CSRF_TOKEN
})

// router and IE 11 workaround. see: https://github.com/vuejs/vue-router/issues/1911
const IE11RouterFix = {
  methods: {
    hashChangeHandler: function () {
      this.$router.push(window.location.hash.substring(1, window.location.hash.length))
    },
    isIE11: function () {
      return !!window.MSInputMethodContext && !!document.documentMode
    }
  },
  mounted: function () { if (this.isIE11()) { window.addEventListener('hashchange', this.hashChangeHandler); } },
  destroyed: function () { if (this.isIE11()) { window.removeEventListener('hashchange', this.hashChangeHandler); } }
};

new Vue({
  vuetify,
  store,
  router,
  mixins: [IE11RouterFix],
  render: h => h(App)
}).$mount('#app')
