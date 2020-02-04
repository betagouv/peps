<template>
  <div>
    <div id="landing-image">
      <v-container class="constrained">
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
        <FeedbackCards />
      </div>
    </v-container>
  </div>
</template>

<script>
import CategoriesCards from "@/components/grids/CategoriesCards.vue"
import DescriptionCards from "@/components/grids/DescriptionCards.vue"
import FeedbackCards from "@/components/grids/FeedbackCards.vue"

export default {
  name: "Landing",
  components: { CategoriesCards, DescriptionCards, FeedbackCards },
  data() {
    return {
      formButtonText: "Proposez-moi des pratiques",
      backgroundImageHeight: 0
    }
  },
  methods: {
    goToForm() {
      window.sendTrackingEvent("Landing", "simulator", this.formButtonText)
      this.$router.push({ name: "FormsContainer" })
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
