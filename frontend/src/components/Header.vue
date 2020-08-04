<template>
  <div>
    <ContributionOverlay
      :visible="showContributionOverlay"
      @done="showContributionOverlay = false"
    />
    <div style="position: absolute; width:100%;">
      <v-app-bar app absolute color="primary" dark>
        <v-toolbar-title>
          <router-link
            :to="{ name: 'Landing' }"
            style="color:white; text-decoration:none; font-weight: bold; outline: none;"
          >Peps</router-link>
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

        <v-btn color="white" @click="onShareXPClick">
          <v-icon color="primary" class="d-flex d-sm-none">mdi-beaker-plus-outline</v-icon>
          <span
            style="font-weight:bold;"
            class="caption text-none d-none d-sm-flex primary--text"
          >Partager une expérience</span>
        </v-btn>

        <v-btn text elevation="0" v-if="!loggedUser" href="/login">
          <v-icon class="d-flex d-sm-none">mdi-account</v-icon>
          <span class="caption text-none d-none d-sm-flex">S'identifier</span>
        </v-btn>

        <v-menu v-if="loggedUser" left bottom>
          <template v-slot:activator="{ on }">
            <v-btn style="margin-left: 10px; margin-right: 0px;" icon v-on="on">

              <v-badge dot color="amber" :value="profilePending || hasUnreadMessages">
                <v-avatar size="40" v-if="profileImage">
                  <v-img :src="profileImage"></v-img>
                </v-avatar>
                <v-icon v-else>mdi-account</v-icon>
              </v-badge>

            </v-btn>
          </template>

          <AccountList />
        </v-menu>
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
    farmer() {
      if (!this.loggedUser || !this.loggedUser.farmer_id) return null
      return this.$store.getters.farmerWithId(this.loggedUser.farmer_id)
    },
    profileImage() {
      if (!this.farmer) return null
      return this.farmer.profile_image
    },
    profilePending() {
      return this.farmer && !this.farmer.approved
    },
    hasUnreadMessages() {
      return this.$store.getters.hasUnreadMessages
    }
  },
  methods: {
    onShareXPClick() {
      window.sendTrackingEvent("Header", "shareXP", "Partager une expérience")
      if (this.loggedUser && this.loggedUser.farmer_id)
        this.$router.push({ name: "ExperimentEditor" })
      else if (this.loggedUser)
        window.alert("Vous n'avez pas un profil agriculteur sur notre site")
      else this.showContributionOverlay = true
    }
  },
  watch: {
    blacklist() {
      this.blacklistDialog = false
    }
  }
}
</script>
