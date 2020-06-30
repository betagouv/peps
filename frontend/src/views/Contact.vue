<template>
  <div>
    <Loader v-if="loading" :title="loadingTitle" :loading="loading" />
    <OverlayMessage 
      :visible="showErrorMessage"
      ctaText="Recharger la page"
      title="Oups ! Une erreur est survenue"
      @done="closeErrorMessage()"
    />
    <Title :title="title" :breadcrumbs="breadcrumbs" />
    <v-container class="constrained">
      <div class="title">Si vous souhaitez en savoir plus</div>
      <div class="body-2">Laissez nous vos coordonnées, nous vous recontacterons sous peu.</div>

      <div style="max-width: 500px; margin: 15px 0 15px 0;">
        <v-text-field prepend-icon="mdi-account" v-model="name" label="Nom et prenom"></v-text-field>
        <v-text-field prepend-icon="mdi-email" v-model="email" label="Adresse email"></v-text-field>
        <v-text-field
          prepend-icon="mdi-cellphone-android"
          v-model="phoneNumber"
          label="Numéro téléphone"
        ></v-text-field>
      </div>
      <v-btn
        class="text-none"
        style="margin-bottom: 15px;"
        @click="sendContactData()"
        color="primary"
        dark
        rounded
      >Contactez-moi !</v-btn>

      <v-divider />
      <div class="title">Contactez-nous directement</div>
      <div class="body-2">Nous répondrons dès que nous serons disponibles.</div>
      <v-btn
        class="text-none"
        style="margin-top: 15px; margin-bottom: 15px;"
        color="primary"
        href="mailto:peps@beta.gouv.fr"
        target="_blank"
        dark
        rounded
      >J'envoie un email</v-btn>

      <v-divider />
      <div class="title">Pour nous suivre sur les réseaux sociaux</div>
      <div class="body-2" style="margin-bottom: 10px;">
        <a href="https://twitter.com/pepsagriculture" target="_blank">
          <v-icon size="24px" style="margin-right: 10px;">mdi-twitter</v-icon>@pepsagriculture
        </a>
      </div>
      <div class="body-2">
        <a href="https://www.facebook.com/pepsagriculture/" target="_blank">
          <v-icon size="24px" style="margin-right: 10px;">mdi-facebook</v-icon>@pepsagriculture
        </a>
      </div>
    </v-container>
  </div>
</template>

<script>
import Title from "@/components/Title.vue"
import Loader from "@/components/Loader.vue"
import OverlayMessage from "@/components/OverlayMessage.vue"
import Constants from "@/constants"

export default {
  name: "Contact",
  components: { Title, Loader, OverlayMessage },
  metaInfo() {
    return {
      title: "Peps - Questions ou suggestions, contactez nous",
      meta: [{ description: 'Si vous souhaitez en savoir plus sur la démarche ou le produit, laissez nous vos coordonnées, nous vous contacterons dans les plus bref délais' }]
    }
  },
  data() {
    return {
      title: "Nous contacter",
      name: '',
      email: '',
      phoneNumber: '',
      breadcrumbs: [
        {
          text: "Accueil",
          disabled: false,
          to: { name: "Map" }
        },
        {
          text: "Contact",
          disabled: true
        }
      ],
      loadingTitle: "Nous envoyons votre information...",
    }
  },
  computed: {
    loading() {
      return (
        this.$store.state.contactLoadingStatus ===
        Constants.LoadingStatus.LOADING
      )
    },
    showErrorMessage() {
      return (
        this.$store.state.contactLoadingStatus ===
        Constants.LoadingStatus.ERROR
      )
    },
    loggedUser() {
      return this.$store.state.loggedUser
    }
  },
  methods: {
    sendContactData() {
      this.$store.dispatch("sendContactData", {
        name: this.name,
        email: this.email,
        phoneNumber: this.phoneNumber
      })
    },
    closeErrorMessage() {
      this.$store.dispatch("resetContactLoadingStatus")
    },
    getInitialName() {
      if (this.loggedUser && this.loggedUser.farmer_id)
        return this.$store.getters.farmerWithId(this.loggedUser.farmer_id).name
      if (this.$store.state.lastContactInfo && this.$store.state.lastContactInfo.name)
        return this.$store.state.lastContactInfo.name
      return null
    },
    getInitialEmail() {
      if (this.loggedUser)
        return this.loggedUser.email
      if (this.$store.state.lastContactInfo && this.$store.state.lastContactInfo.email)
        return this.$store.state.lastContactInfo.email
      return null
    },
    getInitialPhoneNumber() {
      if (this.loggedUser && this.loggedUser.farmer_id)
        return this.$store.getters.farmerWithId(this.loggedUser.farmer_id).phone_number
      if (this.$store.state.lastContactInfo && this.$store.state.lastContactInfo.phoneNumber)
        return this.$store.state.lastContactInfo.phoneNumber
      return null
    }
  },
  mounted() {
    this.name = this.getInitialName()
    this.email = this.getInitialEmail()
    this.phoneNumber = this.getInitialPhoneNumber()
  }
}
</script>

<style scoped>
.title {
  margin-top: 20px;
  margin-bottom: 5px;
}
.body-2 {
  line-height: 1.375rem;
}
</style>
