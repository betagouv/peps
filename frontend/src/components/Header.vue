<template>
  <div>
    <v-app-bar app color="primary" dark>
      <v-toolbar-title><a href="/#/" style="color:white; text-decoration:none; font-weight: bold; outline: none;">Peps</a></v-toolbar-title>
      <v-spacer></v-spacer>

      <v-badge
        bottom
        left
        v-if="blacklist && blacklist.length > 0"
        color="accent"
        :overlap="true"
        class="align-self-center"
      >
        <template v-slot:badge>
          <span>{{ blacklist.length }}</span>
        </template>
        <v-btn icon outlined @click="blacklistDialog = true">
          <v-icon>mdi-cancel</v-icon>
        </v-btn>
      </v-badge>

      <v-btn icon href="mailto:peps@beta.gouv.fr" target="_blank">
        <v-icon>mdi-email</v-icon>
      </v-btn>

      <v-btn icon href="/#/qui-sommes-nous">
        <v-icon>mdi-information</v-icon>
      </v-btn>
    </v-app-bar>
    <v-overlay :value="blacklistDialog" :dark="false">
      <v-btn @click="blacklistDialog = false" class="close-overlay" fab dark small color="grey lighten-5">
        <v-icon color="red darken-3">mdi-close</v-icon>
      </v-btn>
      <Blacklist></Blacklist>
    </v-overlay>
  </div>
</template>

<script>
import Blacklist from "@/components/Blacklist.vue"

export default {
  name: "Header",
  components: { Blacklist },
  data() {
    return { blacklistDialog: false }
  },
  computed: {
    blacklist() {
      return this.$store.state.blacklist
    }
  },
  watch: {
    blacklist() {
      this.blacklistDialog = false
    }
  }
}
</script>