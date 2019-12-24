<template>
  <div>
    <v-card class="pa-5">
      <div
        class="display-1 primary--text"
      >Les pratiques économes en produits phytosanitaires à portée de clic</div>
      <v-divider class="ma-5" />

      <div class="title">Des suggestions de pratiques pour mon exploitation</div>
      <v-card-text>
        3 minutes pour décrire votre exploitation
        <br />
        3 pratiques qui me correspondent
      </v-card-text>
      <v-btn
        class="text-none body-1"
        @click="goToForm()"
        rounded
        color="primary"
        style="margin-top: 10px;"
      >{{formButtonText}}</v-btn>
    <v-divider class="ma-5" />
      <div class="title">Découvrez les pratiques par vous même</div>
      <CategoriesCards />
    </v-card>

    <v-card class="pa-5" style="margin-top: 10px;">
      <div class="title">Le service Peps, qu'est-ce que c'est ?</div>
      <DescriptionCards />
    </v-card>

    <v-card class="pa-5" style="margin-top: 10px;">
      <div class="title">Nous avons besoin de vous pour faire évoluer ce service !</div>
      <v-card-text class="pa-0">Notre volonté est de construire ce service et de l'améliorer avec ces utilisateurs. Nous vous laisson le choix sur la forme, tout retour nous est très utile !</v-card-text>
      <FeedbackCards />
    </v-card>
  </div>
</template>

<script>
import CategoriesCards from "@/components/grids/CategoriesCards.vue"
import DescriptionCards from "@/components/grids/DescriptionCards.vue"
import FeedbackCards from "@/components/grids/FeedbackCards.vue"

export default {
  name: "Landing",
  components: { CategoriesCards, DescriptionCards, FeedbackCards },
  data () {
    return {
      formButtonText: 'Obtenir des suggestions'
    }
  },
  methods: {
    goToForm() {
      window.sendTrackingEvent('Landing', 'simulator', this.formButtonText)
      this.$router.push({ name: "FormsContainer" })
    }
  }
}
</script>
