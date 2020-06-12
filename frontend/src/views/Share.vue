<template>
  <div>
    <Loader v-if="loading" :loading="loading" />
    <OverlayMessage 
      :visible="showErrorMessage"
      body="Veuillez réessayer plus tard"
      title="Oups ! Une erreur est survenue"
      @done="closeErrorMessage()"
    />
    <OverlayMessage 
      :visible="showSuccessMessage"
      title="Merci !"
      body="Nous vous rappellerons dans les plus brefs délais"
      ctaText="OK"
      :ctaAction="closeSuccessMessage"
      :showCloseButton="false"
    />
    <Title :title="title" :breadcrumbs="breadcrumbs" />

    <v-container class="constrained">
      <div class="body-1">
        <p>L'équipe Peps vous accompagne dans la rédaction de votre retour d'expérience
        pour que cela vous prenne le moins de temps possible.</p>
        <p>Remplissez ces quelques informations et nous vous rappellerons dans les
        plus brefs délais.</p>
      </div>

      <v-form ref="form" v-model="formIsValid">
        <div class="field">
          <div class="field-title title">Titre de l'expérience</div>
          <div
            class="field-helper subtitle-2 grey--text"
          >Court et explicite, il doit donner l'idée générale</div>
          <v-text-field
            style="max-width: 450px;"
            :rules="[validators.notEmpty]"
            outlined
            dense
            v-model="experimentTitle"
          ></v-text-field>
        </div>

        <div class="field">
          <div class="field-title title">Pouvez-vous décrire l'expérience ?</div>
          <div
            class="field-helper subtitle-2 grey--text"
          >Dites comment cela s'est déroulé, ce que vous avez observé, les choses que vous avez apprises...</div>
          <v-textarea
            :rules="[validators.notEmpty]"
            :rows="4"
            auto-grow
            outlined
            dense
            v-model="experimentDescription"
          ></v-textarea>
        </div>

        <div class="field">
          <div class="field-title title">Prénom et nom</div>
          <v-text-field
            style="max-width: 350px;"
            :rules="[validators.notEmpty]"
            outlined
            dense
            v-model="name"
          ></v-text-field>
        </div>

        <div class="field">
          <div class="field-title title">Adresse email</div>
          <v-text-field
            style="max-width: 350px;"
            :rules="[validators.isEmail]"
            outlined
            dense
            v-model="email"
          ></v-text-field>
        </div>

        <div class="field">
          <div class="field-title title">Numéro téléphone</div>
          <v-text-field
            style="max-width: 350px;"
            :rules="[validators.notEmpty]"
            outlined
            dense
            v-model="phone"
          ></v-text-field>
        </div>
      </v-form>
      <div>
        <v-btn x-large class="text-none" color="primary" @click="sendTask">
          Valider
        </v-btn>
      </div>
    </v-container>
  </div>
</template>

<script>
import Title from "@/components/Title.vue"
import validators from "@/validators"
import Constants from "@/constants"
import Loader from "@/components/Loader.vue"
import OverlayMessage from "@/components/OverlayMessage.vue"

export default {
  name: "Share",
  components: { Title, OverlayMessage, Loader },
  data() {
    return {
      title: "Partager mon expérience",
      experimentTitle: undefined,
      experimentDescription: undefined,
      name: undefined,
      email: undefined,
      phone: undefined,
      formIsValid: true,

      breadcrumbs: [
        {
          text: "Accueil",
          disabled: false,
          href: "/"
        },
        {
          text: "Partager mon expérience",
          disabled: true
        }
      ]
    }
  },
  computed: {
    validators() {
      return validators
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
    },
    showSuccessMessage() {
      return (
        this.$store.state.contactLoadingStatus ===
        Constants.LoadingStatus.SUCCESS
      )
    }
  },
  methods: {
    sendTask() {
      this.$refs.form.validate()

      window.sendTrackingEvent("Share", "Valider", this.formIsValid ? 'form valid' : 'form invalid')

      if (!this.formIsValid) {
        window.scrollTo(0, 0)
        window.alert("Merci de vérifier les champs en rouge et réessayer")
        return
      }

      this.$store.dispatch('sendShareXPDataTask', {
        experimentTitle: this.experimentTitle,
        experimentDescription: this.experimentDescription,
        name: this.name,
        email: this.email,
        phone: this.phone,
      })
    },
    closeErrorMessage() {
      this.$store.dispatch("resetContactLoadingStatus")
    },
    closeSuccessMessage() {
      this.$store.dispatch("resetContactLoadingStatus")
      this.$router.push({ name: 'Map' })
    }
  }
}
</script>

<style scoped>
.field {
  margin-bottom: 0px;
}
.field-helper {
  margin-bottom: 5px;
}
.cropped {
  max-width: 250px;
}
</style>
