<template>
  <div>
    <NotFound v-if="themeNotFound" style="padding-top: 40px; padding-bottom: 50px;" />
    <div v-else-if="theme">
      <Title :breadcrumbs="breadcrumbs"></Title>
      <v-container class="constrained" style="padding-top: 10px;">

      <v-card
        outlined
      >
        <v-img class="white--text align-end" height="120px" v-if="theme.image" :src="theme.image" />
        <h1 class="title pa-2">
          {{theme.name}}
        </h1>
      </v-card>
      <p style="margin-top: 20px;">
        {{theme.description}}
      </p>
      <v-row v-if="theme.experiments && theme.experiments.length > 0">
          <v-col
            v-for="(experiment, index) in theme.experiments"
            :key="index"
            cols="12"
            sm="6"
            md="4"
          >
            <ExperimentCard :experiment="experiment" />
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
import ExperimentCard from "@/components/ExperimentCard"

export default {
  name: "Theme",
  components: {
    Title,
    ExperimentCard,
    NotFound,
  },
  metaInfo() {
    return {
      title: '',
      description: '',
    }
  },
  props: {
    themeUrlComponent: {
      type: String,
      required: true
    }
  },
  data() {
    return {
      themeNotFound: false,
    }
  },
  computed: {
    theme() {
      try {
        const themeId = this.themeUrlComponent.split('--')[1]
        return this.$store.state.themes.find(x => x.id === themeId)
      } catch (error) {
        return null
      }
    },
    breadcrumbs() {
      return [
        {
          text: "Accueil",
          disabled: false,
          to: { name: "Landing" }
        },
        {
          text: "Thèmes",
          disabled: false,
          to: { name: "Themes" }
        },
        {
          text: this.theme.name,
          disabled: true
        }
      ]
    },
  },
  mounted() {
    if (this.theme) {
      return
    }

    this.$store.commit('SET_THEMES_LOADING_STATUS', Constants.LoadingStatus.LOADING)
    Vue.http.get(`/api/v1/themes/`).then(response => {
      this.$store.commit('SET_THEMES_LOADING_STATUS', Constants.LoadingStatus.SUCCESS)
      this.$store.commit('SET_THEMES', response.body)

      if (!this.theme)
        this.themeNotFound = true
    }).catch(() => {
      this.$store.commit('SET_THEMES_LOADING_STATUS', Constants.LoadingStatus.IDLE)
      this.themesNotFound = true
    })
  }
}
</script>