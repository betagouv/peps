<template>
  <div>
    <Title :title="title" :breadcrumbs="breadcrumbs" />
    <v-container class="constrained">
      <Loader v-if="loading" :title="loadingTitle" :text="loadingSubtitle" :loading="loading" />
      <div v-else-if="suggestions && suggestions.length > 0">
        <v-card
          class="form-info"
          color="#fafafa"
          elevation="0"
          style="margin-bottom: 15px; margin-top: 5px;"
        >
          <v-card-text>
            {{ description }}
            <span
              style="text-decoration: underline; cursor: pointer;"
              @click="goToForm()"
            >Revenir au formulaire</span>.
          </v-card-text>
        </v-card>

        <PracticeCards
          v-if="suggestions"
          :displayDiscardButton="true"
          :practices="suggestions.map(x => x.practice)"
          @blacklist="(practice) => blacklistPractice(practice)"
        />
      </div>
      <ImplementationOverlay
        :practice="implementationPractice"
        @done="implementationPractice = null"
      />
      <DiscardOverlay :practice="discardPractice" @done="discardPractice = null" />
      <v-card v-if="!loading && suggestions.length === 0">
        <v-card-title>Vous cherchez des pratiques alternatives ?</v-card-title>
        <v-card-text>Pour vous proposer des pratiques alternatives nous avons besoin de quelques informations. C'est par ici pour répondre aux questions :</v-card-text>
        <div style="padding-right: 10px; padding-bottom: 10px; text-align: right">
          <v-btn
            class="text-none body-1 practice-buttons"
            @click="goToForm(); reloadLocation()"
            rounded
          >🖊️ Répondre au formulaire</v-btn>
        </div>
      </v-card>
    </v-container>
  </div>
</template>

<script>
import Loader from "@/components/Loader.vue"
import Constants from "@/constants"
import ImplementationOverlay from "@/components/ImplementationOverlay"
import DiscardOverlay from "@/components/DiscardOverlay"
import Title from "@/components/Title.vue"
import PracticeCards from "@/components/grids/PracticeCards.vue"

export default {
  name: "results",
  components: {
    Loader,
    ImplementationOverlay,
    DiscardOverlay,
    Title,
    PracticeCards
  },
  data: () => ({
    title: "Résultats",
    breadcrumbs: [
      {
        text: "Accueil",
        disabled: false,
        href: "/#/"
      },
      {
        text: "Simulateur",
        disabled: false,
        href: "/#/formulaire"
      },
      {
        text: "Résultats",
        disabled: true
      }
    ],
    loadingTitle: "⌛️ Nous cherchons des pratiques alternatives",
    loadingSubtitle:
      "Nous vous proposerons 3 pratiques alternatives de gestion des adventices, des maladies et des ravageurs qui sont adaptées à votre exploitation",
    description:
      "🌱 Vous trouverez ci-dessous les pratiques que nous avons sélectionnées pour votre problématique.",
    implementationPractice: null,
    discardPractice: null
  }),
  computed: {
    loading() {
      return (
        this.$store.state.suggestionsLoadingStatus ===
          Constants.LoadingStatus.LOADING ||
        this.$store.state.statsLoadingStatus ===
          Constants.LoadingStatus.LOADING ||
        this.$store.state.contactLoadingStatus ===
          Constants.LoadingStatus.LOADING ||
        this.$store.state.farmersLoadingStatus ===
          Constants.LoadingStatus.LOADING
      )
    },
    suggestions() {
      return this.$store.state.suggestions.slice().reverse()
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
      this.$router.push({ name: "FormsContainer" })
    },
    reloadLocation() {
      window.location.reload()
    }
  },
  watch: {
    blacklist() {
      this.$store.dispatch("fetchSuggestions")
    }
  }
}
</script>
