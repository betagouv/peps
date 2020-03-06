<template>
  <v-app :class="{ 'banner-visible': !hasContributed }">
    <ContributionBanner id="contribution-banner" v-if="!hasContributed" />
    <div id="app-wrapper">
      <Header />
      <ErrorMessage
        :visible="showErrorMessage"
        ctaText="Recharger la page"
        :ctaAction="this.reload"
        :showCloseButton="false"
      />
      <v-content>
        <transition name="fade" mode="out-in">
          <router-view />
        </transition>
        <Footer />
      </v-content>
    </div>
  </v-app>
</template>

<script>
import Header from "@/components/Header.vue"
import Footer from "@/components/Footer.vue"
import Constants from "@/constants"
import ErrorMessage from "@/components/ErrorMessage.vue"
import ContributionBanner from "@/components/ContributionBanner.vue"

export default {
  name: "App",
  components: {
    Header,
    Footer,
    ErrorMessage,
    ContributionBanner
  },
  mounted() {
    this.$store.dispatch("resetLoaders")
    this.$store.dispatch("fetchFormDefinitions")
    this.$store.dispatch("fetchCategories")
    this.$store.dispatch("fetchFarmersAndExperiments")
  },
  created() {
    window.addEventListener("resize", this.onWindowResize)
  },
  destroyed() {
    window.removeEventListener("resize", this.onWindowResize)
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
    hasContributed: function() {
      return this.$store.state.hasContributed
    }
  },
  methods: {
    reload() {
      location.reload()
    },
    onWindowResize() {
      const height = this.hasContributed ? 0 : this.$el.querySelector('#contribution-banner').height
      this.$el.querySelector('#app-wrapper').style.marginTop = height
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

// #app.banner-visible #app-wrapper {
//   margin-top: 40px;
// }

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
</style>
