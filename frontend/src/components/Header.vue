<template>
  <div>
    <ContributionOverlay :visible="showContributionOverlay" @done="showContributionOverlay = false"/>
    <div style="position: absolute; width:100%;">
      <v-app-bar app absolute color="primary" dark>
        <v-toolbar-title>
          <div style="color:white; text-decoration:none; font-weight: bold; outline: none;">Peps</div>
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

        <v-btn text elevation="0" v-if="isXPPage && !loggedUser" href="/login">
          <v-icon class="d-flex d-sm-none">mdi-account</v-icon>
          <span class="caption text-none d-none d-sm-flex">S'identifier</span>
        </v-btn>

        <v-menu v-if="isXPPage && loggedUser" left bottom>
          <template v-slot:activator="{ on }">
            <v-btn style="margin-left: 0px; margin-right: 10px;" icon v-on="on">
              <v-avatar size="40" v-if="profileImage"><v-img :src="profileImage" ></v-img></v-avatar>
              <v-icon v-else>mdi-account</v-icon>
            </v-btn>
          </template>

          <AccountList />

        </v-menu>

        <v-btn v-if="isXPPage" color="white" @click="onShareXPClick">
          <v-icon color="primary" class="d-flex d-sm-none">mdi-beaker-plus-outline</v-icon>
          <span
            style="font-weight:bold;"
            class="caption text-none d-none d-sm-flex primary--text"
          >Proposer une expérimentation</span>
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
  </div>
</template>

<script>
import Blacklist from "@/components/Blacklist.vue"
import AccountList from "@/components/AccountList.vue"
import ContributionOverlay from "@/components/ContributionOverlay.vue"

export default {
  name: "Header",
  components: { Blacklist, AccountList, ContributionOverlay },
  data: () => {
    return {
      blacklistDialog: false,
      showContributionOverlay: false
    }
  },
  computed: {
    blacklist() {
      return this.$store.state.blacklist
    },
    loggedUser() {
      return this.$store.state.loggedUser
    },
    isXPPage() {
      const xpPages = ["Contribution", "Farmer", "Experiment", "Map", "Profile" , "ExperimentEditor"]
      return xpPages.indexOf(this.$route.name) > -1
    },
    farmer() {
      if (!this.loggedUser || !this.loggedUser.farmer_id) return null
      return this.$store.getters.farmerWithId(
        this.loggedUser.farmer_id
      )
    },
    profileImage() {
      if (!this.farmer)
        return null
      return this.farmer.profile_image
    }
  },
  methods: {
    onShareXPClick() {
      window.sendTrackingEvent(
        "Header",
        "shareXP",
        "Proposer une expérimentation"
      )
      if (this.loggedUser && this.loggedUser.farmer_id)
        this.$router.push({ name: "ExperimentEditor" })
      else if (this.loggedUser)
        window.alert('Vous n\'avez pas un profil agriculteur sur notre site')
      else
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

<style scoped>
.v-overlay {
  z-index: 99999 !important;
}
.close-overlay {
  position: absolute;
  right: -10px;
  top: -20px;
  z-index: 99999;
}
</style>