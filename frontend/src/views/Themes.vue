<template>
  <div>

    <NotFound v-if="themesNotFound" style="padding-top: 40px; padding-bottom: 50px;" />

    <div v-else-if="themes">
      <Title :breadcrumbs="breadcrumbs" />
      <v-container class="constrained" style="padding-top: 10px;">

      <v-row v-if="themes && themes.length > 0">
        <v-col
          v-for="(theme, index) in themes"
          :key="index"
          cols="12"
          sm="6"
          md="4"
        >
          <v-hover>
        <v-card
            class="pa-0 fill-height"
            outlined
            slot-scope="{ hover }"
            :elevation="hover ? 3 : 1"
            @click="goToTheme(theme)"
          >
            <v-img class="white--text align-end" height="120px" v-if="theme.image" :src="theme.image" />
            <v-card-title class="title">{{ theme.name }}</v-card-title>
            <v-card-subtitle>{{ theme.experiments.length }} retours d'expérience</v-card-subtitle>
        </v-card>
        </v-hover>
        </v-col>
      </v-row>

      </v-container>
    </div>
  </div>
</template>

<script>
import Vue from 'vue'
import Title from "@/components/Title.vue"
import NotFound from "@/components/NotFound.vue"
import Constants from "@/constants"

export default {
  name: "Themes",
  components: {
    Title,
    NotFound,
  },
  metaInfo() {
    if (!this.theme) return {}
    return {
      title: 'Thèmes',
    }
  },
  data() {
    return {
      themesNotFound: false,
    }
  },
  computed: {
    themes() {
      return this.$store.state.themes
    },
    breadcrumbs() {
      return [
        {
          text: "Accueil",
          disabled: false,
          to: { name: "Landing" }
        },
        {
          text: 'Thèmes',
          disabled: true
        }
      ]
    }
  },
  methods: {
    goToTheme(theme) {
      let themeUrlComponent = `${theme.name}--${theme.id}`
      window.sendTrackingEvent("Themes", "seeTheme", themeUrlComponent)
      this.$router.push({
        name: "Theme",
        params: {
          themeUrlComponent: themeUrlComponent
        }
      })
    }
  },
  mounted() {
    if (this.theme) {
      return
    }

    this.$store.commit('SET_THEMES_LOADING_STATUS', Constants.LoadingStatus.LOADING)
    Vue.http.get(`/api/v1/themes/`).then(response => {
      this.$store.commit('SET_THEMES_LOADING_STATUS', Constants.LoadingStatus.SUCCESS)
      this.$store.commit('SET_THEMES', response.body)
    }).catch(() => {
      this.$store.commit('SET_THEMES_LOADING_STATUS', Constants.LoadingStatus.IDLE)
      this.themesNotFound = true
    })
  }
}
</script>
