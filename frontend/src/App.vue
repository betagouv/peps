<template>
  <v-app>
    <Header />
    <ErrorMessage :visible="showErrorMessage" />
    <v-content>
      <transition name="fade">
        <router-view />
      </transition>
      <Footer v-show="loadingComplete" />
    </v-content>
  </v-app>
</template>

<script>
import Header from "@/components/Header.vue"
import Footer from "@/components/Footer.vue"
import Constants from "@/constants"
import ErrorMessage from "@/components/ErrorMessage.vue"

export default {
  name: "App",
  components: {
    Header,
    Footer,
    ErrorMessage
  },
  mounted() {
    this.$store.dispatch("resetLoaders")
    this.$store.dispatch("fetchFormDefinitions")
    this.$store.dispatch("fetchCategories")
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
          Constants.LoadingStatus.LOADING &&
        this.$store.state.categoriesLoadingStatus !==
          Constants.LoadingStatus.LOADING
      )
    },
    showErrorMessage() {
      const error = Constants.LoadingStatus.ERROR
      return (
        this.$store.state.formDefinitionsLoadingStatus === error ||
        this.$store.state.suggestionsLoadingStatus === error ||
        this.$store.state.categoriesLoadingStatus === error ||
        this.$store.state.implementationLoadingStatus === error
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

body {
  background: #fff;
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

.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.25s ease-out;
}
.fade-enter,
.fade-leave-to {
  opacity: 0;
}

.v-card__text,
.v-card__title {
  word-break: normal !important;
}

.theme--light.v-application {
  background: transparent !important;
}

.constrained {
  max-width: 900px;
}
</style>
