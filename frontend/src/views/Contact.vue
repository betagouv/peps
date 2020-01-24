<template>
  <div>
    <Loader v-if="loading" :title="loadingTitle" :loading="loading" />
    <ErrorMessage 
      :visible="showErrorMessage"
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
          <v-icon size="24px" style="margin-right: 10px;">mdi-facebook-box</v-icon>@pepsagriculture
        </a>
      </div>
    </v-container>
  </div>
</template>

<script>
import Title from "@/components/Title.vue"
import Loader from "@/components/Loader.vue"
import ErrorMessage from "@/components/ErrorMessage.vue"
import Constants from "@/constants"

export default {
  name: "Contact",
  components: { Title, Loader, ErrorMessage },
  data() {
    return {
      title: "Nous contacter",
      breadcrumbs: [
        {
          text: "Accueil",
          disabled: false,
          href: "/#/"
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
    name: {
      get() {
        if (this.$store.state.contactFormData && this.$store.state.contactFormData.name)
          return this.$store.state.contactFormData.name
        return undefined
      },
      set(value) {
        this.$store.dispatch('addContactFormData', { fieldId: 'name', fieldValue: value })
      }
    },
    email: {
      get() {
        if (this.$store.state.contactFormData && this.$store.state.contactFormData.email)
          return this.$store.state.contactFormData.email
        return undefined
      },
      set(value) {
        this.$store.dispatch('addContactFormData', { fieldId: 'email', fieldValue: value })
      }
    },
    phoneNumber: {
      get() {
        if (this.$store.state.contactFormData && this.$store.state.contactFormData.phone)
          return this.$store.state.contactFormData.phone
        return undefined
      },
      set(value) {
        this.$store.dispatch('addContactFormData', { fieldId: 'phone', fieldValue: value })
      }
    },
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
    }
  },
  methods: {
    sendContactData() {
      this.$store.dispatch("sendContactData")
    },
    closeErrorMessage() {
      this.$store.dispatch("resetContactLoadingStatus")
    }
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
