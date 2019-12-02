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
import Header from "@/components/Header.vue";
import Footer from "@/components/Footer.vue";
import Constants from "@/constants"

export default {
  name: "App",
  components: {
    Header,
    Footer,
  },
  mounted() {
    this.$store.dispatch("fetchFormDefinitions");
  },
  computed: {
    loadingComplete() {
      return (
        this.$store.state.formDefinitionsLoadingStatus !==
          Constants.LoadingStatus.LOADING &&
        this.$store.state.suggestionsLoadingStatus !==
          Constants.LoadingStatus.LOADING
      )
    }
  }
};
</script>

<style lang="scss">
#app {
  font-family: "Roboto", sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  color: #2c3e50;
}
</style>
