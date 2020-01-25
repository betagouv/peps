<template>
  <div>
    <Title :title="title" :breadcrumbs="breadcrumbs" />
    <v-container class="constrained">
      <Loader v-if="loading" :title="loadingTitle" :loading="loading" />
      <div v-else-if="canRenderForms">
        <v-card
          class="form-info"
          color="#fafafa"
          elevation="0"
          style="margin-bottom: 15px; margin-top: 5px;"
        >
          <v-card-text>Peps est en étape d'expérimentation et ne cible pour le moment que les pratiques en grandes cultures et élevage 🌱 🐄</v-card-text>
        </v-card>
        <Form
          style="margin-bottom: 10px;"
          :schema="miaFormDefinition.schema"
          :options="miaFormDefinition.options"
          updateActionName="addMiaFormData"
          storeDataName="miaFormData"
        />
        <Form
          style="margin-bottom: 10px;"
          v-if="$options.shouldShowStatsForm"
          :schema="statsFormDefinition.schema"
          :options="statsFormDefinition.options"
          updateActionName="addStatsFormData"
          storeDataName="statsFormData"
        />
        <Form
          style="margin-bottom: 10px;"
          v-if="$options.shouldShowContactForm"
          :schema="contactFormDefinition.schema"
          :options="contactFormDefinition.options"
          updateActionName="addContactFormData"
          storeDataName="contactFormData"
        />
        <div style="margin-top: 30px; text-align: right">
          <v-btn
            large
            rounded
            :disabled="disabled"
            color="primary"
            @click="submitForm()"
          >Trouver des pratiques alternatives</v-btn>
          <p
            :style="{visibility: disabled ? 'visible' : 'hidden'}"
            class="caption"
            style="margin-top: 10px;"
          >
            <v-icon small>mdi-alert-circle</v-icon>Répondez à toutes les questions ci-dessus pour continuer
          </p>
        </div>
      </div>
    </v-container>
  </div>
</template>

<script>
import Loader from "@/components/Loader.vue"
import Form from "@/components/forms/Form.vue"
import Constants from "@/constants"
import Title from "@/components/Title.vue"

export default {
  name: "FormsContainer",
  components: { Loader, Title, Form },
  created() {
    const statsFormData = this.$store.state.statsFormData
    const contactFormData = this.$store.state.contactFormData
    this.$options.shouldShowStatsForm =
      !statsFormData || Object.keys(statsFormData).length === 0
    this.$options.shouldShowContactForm =
      !contactFormData || Object.keys(contactFormData).length === 0
  },
  data() {
    return {
      loadingTitle: "Juste un instant...",
      title: "Obtenir des suggestions",
      breadcrumbs: [
        {
          text: "Accueil",
          disabled: false,
          href: "/#/"
        },
        {
          text: "Simulateur",
          disabled: true
        }
      ]
    }
  },
  computed: {
    loading() {
      return (
        this.$store.state.formDefinitionsLoadingStatus ===
        Constants.LoadingStatus.LOADING
      )
    },
    miaFormDefinition() {
      return this.$store.state.miaFormDefinition
    },
    statsFormDefinition() {
      return this.$store.state.statsFormDefinition
    },
    contactFormDefinition() {
      return this.$store.state.contactFormDefinition
    },
    canRenderForms() {
      return (
        Object.keys(this.miaFormDefinition).length > 0 &&
        Object.keys(this.statsFormDefinition).length > 0 &&
        Object.keys(this.contactFormDefinition).length > 0
      )
    },
    disabled() {
      return !this.$store.getters.formsAreComplete
    }
  },
  methods: {
    submitForm() {
      this.$router.push({ name: "Results" })
      if (this.$options.shouldShowStatsForm) {
        this.$store.dispatch("sendStatsData")
      }
      if (this.$options.shouldShowContactForm) {
        this.$store.dispatch("sendContactData", 'A répondu depuis l\'application Web')
      }
      this.$store.dispatch("fetchSuggestions")
    }
  }
}
</script>
