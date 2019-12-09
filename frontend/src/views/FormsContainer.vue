<template>
  <div>
    <Loader v-if="loading" :title="loadingTitle" :loading="loading" />
    <div v-else-if="canRenderForms">
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
  </div>
</template>

<script>
import Loader from "@/components/Loader.vue"
import Form from "@/components/forms/Form.vue"
import Constants from "@/constants"

export default {
  name: "FormsContainer",
  components: { Loader, Form },
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
      loadingTitle: "Juste un instant..."
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
        this.$store.dispatch("sendContactData")
      }
      this.$store.dispatch("fetchSuggestions")
    }
  }
}
</script>
