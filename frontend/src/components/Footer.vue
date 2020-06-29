<template>
  <div style="background: #EEE;">

    <div style="text-align:center;">
      <v-container class="constrained">
        <v-row align="start">
          <v-col cols="6" sm="1" :style="'padding:' + minAgriPadding + ';'">
            <v-img
              class="white--text align-start"
              position="top"
              contain
              :max-height="imageMaxHeight"
              src="/static/images/minagri.png"
            />
          </v-col>

          <v-col cols="6" sm="2" :style="'padding:' + minEcoPadding + ';'">
            <v-img
              class="white--text align-start"
              position="top"
              contain
              :max-height="imageMaxHeight"
              src="/static/images/mineco.png"
            />
          </v-col>

          <v-col cols="12" sm="4">
            <p class="text-left caption" style="padding-right: 10px;">
              Peps est un service proposé par le Ministère de l’Agriculture et de l’Alimentation
              et le Ministère de la Transiton Écologique et Solidaire dans le cadre du plan Ecophyto
            </p>
          </v-col>

          <v-col cols="12" sm="2" :style="'padding: ' + listPadding + ';'">
            <ul class="text-left caption">
              <li class="font-weight-bold">Peps</li>
              <li>
                <a target="_blank" href="https://stats.data.gouv.fr/index.php?idSite=107">Statistiques</a>
              </li>
              <li>
                <a href="/qui-sommes-nous">En savoir plus</a>
              </li>
              <li>
                <a href="/contact">Contact</a>
              </li>
              <li>
                <a href="/conditions-generales-d-utilisation">CGU</a>
              </li>
            </ul>
          </v-col>

          <v-col cols="12" sm="2" :style="'padding: ' + listPadding + ';'">
            <ul class="text-left caption">
              <li class="font-weight-bold">Reseaux sociaux</li>
              <li>
                <a target="_blank" href="https://www.facebook.com/pepsagriculture/">Facebook</a>
              </li>
              <li>
                <a target="_blank" href="https://twitter.com/pepsagriculture">Twitter</a>
              </li>
            </ul>
          </v-col>
        </v-row>
      </v-container>

      <div style="padding-top:20px;">
        <a href="https://www.beta.gouv.fr/apropos/" target="_blank" style="text-align: center;">
          <img src="/static/images/betagouv.png" style="height:35px; opacity:0.5;" />
        </a>
      </div>

      <div
        class="caption ma-2"
        style="color: #777; text-align: center; padding-bottom: 20px;"
      >{{ new Date().getFullYear() }} — Peps</div>
    </div>
  </div>
</template>

<script>
export default {
  name: "Footer",
  computed: {
    listPadding() {
      if (this.$vuetify.breakpoint.name === 'xs') {
        return '10px'
      }
      return '10px 0 0 0'
    },
    imageMaxHeight() {
      if (this.$vuetify.breakpoint.name === 'xs') {
        return '120px'
      }
      return undefined
    },
    minAgriPadding() {
      if (this.$vuetify.breakpoint.name === 'xs') {
        return '12px'
      }
      return '12px 0px 12px 12px'
    },
    minEcoPadding() {
      if (this.$vuetify.breakpoint.name === 'xs') {
        return '12px 12px 12px 0'
      }
      return '12px'
    },
  }
}
</script> 

<style scoped>
.v-application ul {
  list-style: outside none none;
  padding-left: 0;
}
.v-application .caption {
  font-size: 0.65rem !important;
}
li a {
  color: #2c3e50;
  text-decoration: none;
}

li a:hover {
  text-decoration: underline;
}
</style>