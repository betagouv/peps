import Vue from 'vue'
import App from '@/App.vue'
import vuetify from '@/plugins/vuetify'
import store from '@/store'
import router from '@/router'
import VueResource from 'vue-resource'
import VueBrowserUpdate from 'vue-browserupdate'
import "leaflet/dist/leaflet.css"
import L from 'leaflet'

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
}).$mount('#app');

  // We manually include https://github.com/hayeswise/Leaflet.PointInPolygon/tree/v1.0.0
  // to determine whether of not a point is in a polygon.
  (function (L) {
    "use strict"
    L.Polyline.prototype.contains = function (p) {
      var rectangularBounds = this.getBounds()
      var wn
      if (rectangularBounds.contains(p)) {
        wn = this.getWindingNumber(p)
        return wn !== 0
      } else {
        return false
      }
    }
    L.LatLng.prototype.isLeft = function (p1, p2) {
      return (
        (p1.lng - this.lng) * (p2.lat - this.lat) -
        (p2.lng - this.lng) * (p1.lat - this.lat)
      )
    }
    L.Polyline.prototype.getWindingNumber = function (p) {
      var i, isLeftTest, n, vertices, wn
      function flatten(a) {
        var flat
        flat = (Array.isArray
          ? Array.isArray(a)
          : L.Util.isArray(a))
          ? a.reduce(function (accumulator, v) {
            return accumulator.concat(Array.isArray(v) ? flatten(v) : v)
          }, [])
          : a
        return flat
      }

      vertices = this.getLatLngs()
      vertices = flatten(vertices)
      vertices = vertices.filter(function (v, i, array) {
        if (
          i > 0 &&
          v.lat === array[i - 1].lat &&
          v.lng === array[i - 1].lng
        ) {
          return false
        } else {
          return true
        }
      })
      n = vertices.length
      if (
        n > 0 &&
        !(
          vertices[n - 1].lat === vertices[0].lat &&
          vertices[n - 1].lng === vertices[0].lng
        )
      ) {
        vertices.push(vertices[0])
      }
      n = vertices.length - 1
      wn = 0
      for (i = 0; i < n; i++) {
        isLeftTest = vertices[i].isLeft(vertices[i + 1], p)
        if (isLeftTest === 0) {
          wn = 1
          break
        } else {
          if (isLeftTest !== 0) {
            if (vertices[i].lat <= p.lat) {
              if (vertices[i + 1].lat > p.lat) {
                if (isLeftTest > 0) {
                  wn++
                }
              }
            } else {
              if (vertices[i + 1].lat <= p.lat) {
                if (isLeftTest < 0) {
                  wn--
                }
              }
            }
          } else {
            wn++
          }
        }
      }
      return wn
    }
  })(L)
