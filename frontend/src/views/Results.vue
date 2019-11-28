<template>
  <div>
    <Loader v-if="!!loading" :title="loadingTitle" :text="loadingSubtitle" />
    <div v-else-if="suggestions && suggestions.length > 0">
      <InfoWell :description="infoWellText" style="margin-bottom:20px;"/>
      <div v-for="suggestion in suggestions" :key="suggestion.id">
        <Practice :practice="suggestion.practice" style="margin-bottom: 10px;" />
      </div>
    </div>
  </div>
</template>

<script>
import Loader from "@/components/Loader.vue"
import Constants from '@/constants'
import Practice from '@/components/Practice.vue'
import InfoWell from '@/components/InfoWell.vue'

export default {
  name: "results",
  components: { Loader, Practice, InfoWell },
  data() {
    return {
      loadingTitle: "⌛️ Nous cherchons des pratiques alternatives",
      loadingSubtitle:
        "Nous vous proposerons 3 pratiques alternatives de gestion des adventices, des maladies et des ravageurs qui sont adaptées à votre exploitation",
      infoWellText: "🌱 Vous trouverez ci-dessous les trois pratiques que nous avons sélectionnées pour votre problématique.",
    }
  },
  computed: {
    loading() {
      return (
        this.$store.state.suggestionsLoadingStatus ===
        Constants.LoadingStatus.LOADING
      )
    },
    suggestions() {
      return this.$store.state.suggestions
    }
  }
}
</script>
