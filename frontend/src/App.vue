<template>
  <v-app>
    <Header />
    <v-content style="background: #EEE;">
      <v-container style="max-width: 900px;">
        <router-view />
      </v-container>
      <Footer v-show="loadingComplete" />
    </v-content>
  </v-app>
</template>

<script>
import Header from "@/components/Header.vue"
import Footer from "@/components/Footer.vue"
import Constants from "@/constants"

export default {
  name: "App",
  components: {
    Header,
    Footer
  },
  mounted() {
    this.$store.dispatch("fetchFormDefinitions")
    this.$store.dispatch("resetLoaders")
  },
  computed: {
    loadingComplete() {
      return (
        this.$store.state.formDefinitionsLoadingStatus !==
          Constants.LoadingStatus.LOADING &&
        this.$store.state.suggestionsLoadingStatus !==
          Constants.LoadingStatus.LOADING &&
        this.$store.state.statsLoadingStatus !==
          Constants.LoadingStatus.LOADING &&
        this.$store.state.contactLoadingStatus !==
          Constants.LoadingStatus.LOADING
      )
    }
  }
}
</script>

<style lang="scss">
#app {
  font-family: "Roboto", sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  color: #2c3e50;
}

body .buorg {
  border-bottom: 1px solid #008763;
  background-color: #008763;
  font-family: "Roboto", sans-serif;
  color: white;
}

body .buorg .buorg-buttons {
  margin-top: 15px;
  margin-bottom: 15px;
}
</style>
