<template>
  <v-list>

    <v-list-item v-if="loggedUser">
      <v-list-item-avatar color="grey">
        <v-img :src="profileImage" v-if="profileImage"></v-img>
        <v-icon v-else>mdi-account</v-icon>
      </v-list-item-avatar>
      <v-list-item-content>
        <v-list-item-title class="title" style="padding-left: 3px;">{{ displayName }}</v-list-item-title>
      </v-list-item-content>
    </v-list-item>

    <v-list-item v-else>
      <v-list-item-content @click="login">
        <v-list-item-title class="title" style="padding-left: 3px;">Session fermée</v-list-item-title>
      </v-list-item-content>
    </v-list-item>

    <v-divider v-if="loggedUser"></v-divider>

    <v-list-item v-if="loggedUser" @click="goToProfile">
      <v-list-item-title class="body-2" style="padding-left: 3px;">Mon compte</v-list-item-title>
    </v-list-item>

    <v-list-item v-if="loggedUser" @click="logout">
      <v-list-item-title class="body-2" style="padding-left: 3px;">Fermer ma session</v-list-item-title>
    </v-list-item>

    <v-list-item v-if="!loggedUser" @click="login">
      <v-list-item-title class="body-2" style="padding-left: 3px;">M'identifier</v-list-item-title>
    </v-list-item>

  </v-list>
  
</template>

<script>

export default {
  name: "AccountList",
  computed: {
    loggedUser() {
      return this.$store.state.loggedUser
    },
    farmer() {
      if (!this.loggedUser || !this.loggedUser.farmer_external_id) return null
      return this.$store.getters.farmerWithExternalId(
        this.loggedUser.farmer_external_id
      )
    },
    displayName() {
      if (!this.loggedUser) return ""
      if (this.farmer) return this.farmer.name
      if (this.loggedUser.first_name && this.loggedUser.first_name !== "")
        return this.loggedUser.first_name + " " + this.loggedUser.last_name
      if (this.loggedUser.username && this.loggedUser.username !== "")
        return this.loggedUser.username

      return this.loggedUser.email
    },
    profileImage() {
      if (!this.farmer) return null
      return this.farmer.profile_image
    }
  },
  methods: {
    goToProfile() {
      if (this.$route.name === 'Profile')
        return
      window.sendTrackingEvent("Header", "Profile", this.loggedUser.email)
      this.$router.push({
        name: "Profile"
      })
    },
    login() {
      window.sendTrackingEvent("Header", "Login", 'login')
      window.location.href = "/login"
    },
    logout() {
      if (window.confirm('Êtes-vous sur de vouloir fermer votre session ?')) {
        window.sendTrackingEvent("Header", "Logout", 'logout')
        window.location.href = "/logout"
      }
    },
  }
}
</script>
