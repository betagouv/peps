import Vue from 'vue'
import App from '@/App.vue'
import vuetify from '@/plugins/vuetify'
import store from '@/store'
import router from '@/router'
import VueResource from 'vue-resource'
import VueBrowserUpdate from 'vue-browserupdate'
import "leaflet/dist/leaflet.css"

import { Icon } from 'leaflet';

delete Icon.Default.prototype._getIconUrl;
Icon.Default.mergeOptions({
  iconRetinaUrl: require('leaflet/dist/images/marker-icon-2x.png'),
  iconUrl: require('leaflet/dist/images/marker-icon.png'),
  shadowUrl: require('leaflet/dist/images/marker-shadow.png'),
});


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

Vue.filter('truncate', function (text, length, clamp) {
  clamp = clamp || '...';
  var node = document.createElement('div');
  node.innerHTML = text;
  var content = node.textContent;
  return content.length > length ? content.slice(0, length) + clamp : content;
});

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
