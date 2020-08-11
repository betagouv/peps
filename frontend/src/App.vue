<template>
  <v-app>
    <div id="app-wrapper">
      <Header />
      <Loader v-if="initialCallsLoading" :loading="true" />
      <OverlayMessage
        :visible="showErrorMessage"
        ctaText="Recharger la page"
        title="Oups ! Une erreur est survenue"
        body="Veuillez réessayer plus tard"
        :ctaAction="this.reload"
        :showCloseButton="false"
      />
      <v-main style="margin-bottom: 20px;">
        <transition name="fade" mode="out-in">
          <router-view />
        </transition>
      </v-main>
      <Footer v-if="!removeFooter" />
    </div>
  </v-app>
</template>

<script>
import Header from "@/components/Header.vue"
import Footer from "@/components/Footer.vue"
import Constants from "@/constants"
import OverlayMessage from "@/components/OverlayMessage.vue"
import Loader from "@/components/Loader.vue"

export default {
  name: "App",
  components: {
    Header,
    Footer,
    OverlayMessage,
    Loader
  },
  data() {
    return {
      messageRequestInterval: null
    }
  },
  mounted() {
    this.$store.dispatch("resetLoaders")
    this.$store.dispatch("fetchLoggedUser")
    this.$store.dispatch("fetchFarmersAndExperiments")
    this.$store.dispatch("fetchMessages")
    this.$store.dispatch("fetchStats")
  },
  computed: {
    showErrorMessage() {
      const error = Constants.LoadingStatus.ERROR
      return (
        this.$store.state.formDefinitionsLoadingStatus === error ||
        this.$store.state.suggestionsLoadingStatus === error ||
        this.$store.state.categoriesLoadingStatus === error ||
        this.$store.state.farmersLoadingStatus === error ||
        this.$store.state.implementationLoadingStatus === error
      )
    },
    initialCallsLoading() {
      const loading = Constants.LoadingStatus.LOADING
      return (
        this.$store.state.loggedUserLoadingStatus === loading ||
        this.$store.state.farmersLoadingStatus === loading
      )
    },
    removeFooter() {
      return this.$route.name === "Messages"
    },
    loggedUser() {
      return this.$store.state.loggedUser
    }
  },
  methods: {
    reload() {
      location.reload()
    },
    createMessageInterval() {
      this.clearMessageInterval()
      this.messageRequestInterval = setInterval(() => this.$store.dispatch('fetchNewMessages'), 30000)
    },
    clearMessageInterval() {
      if (!this.messageRequestInterval)
        return
      clearInterval(this.messageRequestInterval)
      this.messageRequestInterval = null
    },
  },
  watch: {
    loggedUser(value) {
      if (value && value.farmer_id) {
        this.createMessageInterval()
      } else {
        this.clearMessageInterval()
      }
    }
  }
}
</script>

<style lang="scss">
$source-sans-pro: "Source Sans Pro", "Roboto", sans-serif;
$cursive: "Caveat", cursive;

#app.v-application {
  font-family: "Roboto", sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  color: #2c3e50;

  .display-1,
  .display-2,
  .display-3,
  .display-4,
  .headline,
  .subtitle-1,
  .subtitle-2,
  .title {
    font-family: $source-sans-pro !important;
  }

  .cursive {
    font-family: $cursive !important;
  }

  .display-1,
  .subtitle-2,
  .title {
    font-weight: bold !important;
  }

  .subtitle-2 {
    font-size: 16px !important;
  }
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
  max-width: 1000px;
}

// https://github.com/Leaflet/Leaflet/issues/4686
.leaflet-fade-anim .leaflet-tile,
.leaflet-zoom-anim .leaflet-zoom-animated {
  will-change: auto !important;
}

.v-overlay {
  z-index: 99999 !important;
}

.close-overlay {
  position: absolute;
  right: -10px;
  top: -20px;
  z-index: 99999;
}

.field {
  margin-bottom: 30px;
}
.field-helper {
  margin-bottom: 5px;
  font-family: "Roboto", sans-serif;
  font-weight: normal;
  font-size: 0.9em;
  color: #888;
}
.parent-field {
  margin-bottom: 10px;
}
.child-field {
  padding-left: 30px;
  margin-bottom: 10px;
}
.child-field:last-of-type {
  margin-bottom: 30px;
}
.field .mandatory {
  color: #d74c4c;
  text-transform: uppercase;
  font-size: 0.6em;
  letter-spacing: 2px;
}
</style>
