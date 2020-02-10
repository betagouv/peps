<template>
  <div>
    <div id="landing-image">
      <v-container class="constrained">
        <v-alert
          border="top"
          colored-border
          color="primary"
          type="info"
          elevation="2"
          v-if="!hasContributed"
        >
          Nous avons besoin de vous !
          <span
            style="text-decoration: underline; cursor: pointer;"
            @click="contribute()"
          >Contribuez au projet</span> lors d'un entretien, des tests de nouvelles interfaces, un tour de plaine...
        </v-alert>
        <v-card id="landing-main" class="pa-5" style="margin-top: 10px; max-width: 650px;">
          <div class="display-1">
            Les pratiques économes en produits phytosanitaires
            <span
              class="cursive"
              style="font-size: 38px; letter-spacing: 0em;"
            >à portée de clic</span>
          </div>
          <v-card-text style="padding: 16px 16px 16px 0;">
            3 minutes pour décrire votre exploitation
            <br />3 pratiques qui me correspondent
          </v-card-text>
          <v-btn
            class="text-none body-1"
            @click="goToForm()"
            rounded
            color="primary"
            style="margin-top: 10px;"
          >{{formButtonText}}</v-btn>
        </v-card>
      </v-container>
    </div>

    <v-container class="constrained">
      <div class="title" style="margin-top: 20px;">Découvrez les pratiques par vous même</div>
      <CategoriesCards />

      <div style="margin-top: 20px;">
        <div class="title">Le service Peps, qu'est-ce que c'est ?</div>
        <DescriptionCards />
      </div>

      <div style="margin-top: 20px;">
        <div class="title">Nous avons besoin de vous pour faire évoluer ce service !</div>
        <v-card-text
          class="pa-0"
        >Notre volonté est de construire ce service et de l'améliorer avec ces utilisateurs. Nous vous laisson le choix sur la forme, tout retour nous est très utile !</v-card-text>
        <FeedbackCards :contributionCallback="contribute" />
      </div>
    </v-container>
    <ContributionOverlay :visible="showContributionOverlay" @done="showContributionOverlay = false"/>
  </div>
</template>

<script>
import CategoriesCards from "@/components/grids/CategoriesCards.vue"
import DescriptionCards from "@/components/grids/DescriptionCards.vue"
import FeedbackCards from "@/components/grids/FeedbackCards.vue"
import ContributionOverlay from "@/components/ContributionOverlay.vue"

export default {
  name: "Landing",
  components: {
    CategoriesCards,
    DescriptionCards,
    FeedbackCards,
    ContributionOverlay
  },
  data() {
    return {
      formButtonText: "Proposez-moi des pratiques",
      backgroundImageHeight: 0,
      showContributionOverlay: false
    }
  },
  computed: {
    hasContributed: function() {
      return this.$store.state.hasContributed
    }
  },
  methods: {
    goToForm() {
      window.sendTrackingEvent("Landing", "simulator", this.formButtonText)
      this.$router.push({ name: "FormsContainer" })
    },
    contribute() {
      window.sendTrackingEvent("Landing", "contribute", this.formButtonText)
      this.showContributionOverlay = true
    }
  }
}
</script>

<style scoped>
#landing-image {
  background: #ddba8e;
  background-image: url("/static/images/sunflowers-optimized.jpg");
  background-repeat: no-repeat;
  background-position: center;
  background-size: cover;
  padding-bottom: 10px;
}
</style>
