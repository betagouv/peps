<template>
  <v-app>
    <Header />
    <v-content>
      <v-container>
        <router-view />
      </v-container>
    </v-content>
  </v-app>
</template>

<script>
import Header from "@/components/Header.vue";
import store from "@/store/index";

export default {
  name: "App",
  components: {
    Header
  },
  mounted() {
    store.dispatch("fetchFormDefinitions");
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
