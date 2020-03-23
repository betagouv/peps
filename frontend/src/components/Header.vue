<template>
  <div style="position: absolute; width:100%;">
    <ContributionOverlay
        :visible="showContributionOverlay"
        @done="showContributionOverlay = false"
      />
    <v-app-bar app absolute color="primary" dark>
      <v-toolbar-title>
        <div
          style="color:white; text-decoration:none; font-weight: bold; outline: none;"
        >Peps</div>
      </v-toolbar-title>
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

      <v-btn text elevation="0" href="/#/qui-sommes-nous">
        <v-icon class="d-flex d-sm-none">mdi-information</v-icon>
        <span class="caption text-none d-none d-sm-flex">En savoir plus</span>
      </v-btn>

      <v-btn text elevation="0" href="/#/contact">
        <v-icon class="d-flex d-sm-none">mdi-email</v-icon>
        <span class="caption text-none d-none d-sm-flex">Contact</span>
      </v-btn>

      <v-btn color="#00744C" dark @click="onShareXPClick">
        <v-icon class="d-flex d-sm-none">mdi-beaker-outline</v-icon>
        <span class="caption text-none d-none d-sm-flex">Proposer une expérimentation</span>
      </v-btn>
    </v-app-bar>
    <v-overlay :value="blacklistDialog" :dark="false">
      <v-btn
        @click="blacklistDialog = false"
        class="close-overlay"
        fab
        dark
        small
        color="grey lighten-5"
      >
        <v-icon color="red darken-3">mdi-close</v-icon>
      </v-btn>
      <Blacklist style="max-height: 80vh;" class="overflow-y-auto"></Blacklist>
    </v-overlay>
  </div>
</template>

<script>
import Blacklist from "@/components/Blacklist.vue"
import ContributionOverlay from "@/components/ContributionOverlay.vue"

export default {
  name: "z",
  components: { Blacklist, ContributionOverlay },
  data: () => {
    return { 
      blacklistDialog: false,
      showContributionOverlay: false,
    }
  },
  computed: {
    blacklist() {
      return this.$store.state.blacklist
    }
  },
  methods: {
    onShareXPClick() {
      window.sendTrackingEvent("Header", "shareXP", "Proposer une expérimentation")
      this.showContributionOverlay = true
    }
  },
  watch: {
    blacklist() {
      this.blacklistDialog = false
    }
  }
}
</script>
