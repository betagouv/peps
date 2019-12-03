<template>
  <div>
    <Loader v-if="!!loading" :title="loadingTitle" :text="loadingSubtitle" />
    <div v-else-if="suggestions && suggestions.length > 0">
      <InfoWell :description="infoWellText" style="margin-bottom:15px;" />
      <div v-for="suggestion in suggestions" :key="suggestion.id">
        <Practice
          :practice="suggestion.practice"
          style="margin-bottom: 15px;"
          @implement="tryPractice(suggestion.practice)"
          @blacklist="blacklistPractice(suggestion.practice)"
        />
      </div>
    </div>
    <ImplementationOverlay
      :practice="implementationPractice"
      @done="implementationPractice = null"
    />
    <DiscardOverlay
      :practice="discardPractice"
      @done="discardPractice = null"
    />
    <v-card v-if="!loading && suggestions.length === 0">
      <v-card-title>Vous cherchez des pratiques alternatives ?</v-card-title>
      <v-card-text>Pour vous proposer des pratiques alternatives nous avons besoin de quelques informations. C'est par ici pour répondre aux questions :</v-card-text>
      <div style="padding-right: 10px; padding-bottom: 10px; text-align: right">
        <v-btn class="text-none body-1 practice-buttons" @click="goToForm()" rounded>🖊️ Répondre au formulaire</v-btn>
      </div>
    </v-card>
  </div>
</template>

<script>
import Loader from "@/components/Loader.vue"
import Constants from "@/constants"
import Practice from "@/components/Practice.vue"
import InfoWell from "@/components/InfoWell.vue"
import ImplementationOverlay from "@/components/ImplementationOverlay"
import DiscardOverlay from "@/components/DiscardOverlay"

export default {
  name: "results",
  components: { Loader, Practice, InfoWell, ImplementationOverlay, DiscardOverlay },
  data: () => ({
    loadingTitle: "⌛️ Nous cherchons des pratiques alternatives",
    loadingSubtitle:
      "Nous vous proposerons 3 pratiques alternatives de gestion des adventices, des maladies et des ravageurs qui sont adaptées à votre exploitation",
    infoWellText:
      "🌱 Vous trouverez ci-dessous les trois pratiques que nous avons sélectionnées pour votre problématique.",
    implementationPractice: null,
    discardPractice: null,
  }),
  computed: {
    loading() {
      return (
        this.$store.state.suggestionsLoadingStatus ===
          Constants.LoadingStatus.LOADING ||
        this.$store.state.statsLoadingStatus ===
          Constants.LoadingStatus.LOADING ||
        this.$store.state.contactLoadingStatus ===
          Constants.LoadingStatus.LOADING
      )
    },
    suggestions() {
      return this.$store.state.suggestions
    },
    blacklist() {
      return this.$store.state.blacklist
    }
  },
  methods: {
    tryPractice(practice) {
      this.implementationPractice = practice
    },
    blacklistPractice(practice) {
      this.discardPractice = practice
    },
    goToForm() {
      this.$router.push({ name: "FormContainer" })
      location.reload()
    }
  },
  watch: {
    blacklist() {
      this.$store.dispatch('fetchSuggestions')
    }
  }
}
</script>
