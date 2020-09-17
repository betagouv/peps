<template>
  <div>
    <ContributionOverlay
      :visible="showContributionOverlay"
      @done="showContributionOverlay = false"
    />
    <v-container class="constrained">
      <!-- Intro top -->
      <v-row>
        <v-col cols="12" md="10">
          <div class="display-1">
            Le savoir partagé
            <span
              class="cursive"
              style="font-size: 38px; letter-spacing: 0em;"
            >entre agriculteurs</span>
          </div>
          <v-card-text
            class="body-1"
            style="padding: 16px 16px 0px 0;"
          >Un service public qui soutient une agriculture plus durable, pour ceux et celles qui produisent ainsi que pour l'environnement</v-card-text>
        </v-col>

        <v-col cols="2" class="d-none d-md-flex">
          <v-img src="/static/images/agriculteurs-discussion-salade.jpg"></v-img>
        </v-col>
      </v-row>

      <v-row>
        <v-col cols="12" sm="4">
          <v-card flat>
            <v-card-title
              v-if="$vuetify.breakpoint.name !== 'xs'"
              style="color: #2c3e50; margin-bottom: 5px; padding: 0 0 5px 0;"
            >Découvrez</v-card-title>
            <v-card-text class="pa-0" style="color: #2c3e50;">
              <span class="font-weight-bold" v-if="$vuetify.breakpoint.name === 'xs'">Découvrez</span>
               les retours d'expériences d'autres agriculteurs
            </v-card-text>
          </v-card>
        </v-col>
        <v-col cols="12" sm="4">
          <v-card flat>
            <v-card-title
              v-if="$vuetify.breakpoint.name !== 'xs'"
              style="color: #2c3e50; margin-bottom: 5px; padding: 0 0 5px 0;"
            >Échangez</v-card-title>
            <v-card-text class="pa-0" style="color: #2c3e50;">
              <span class="font-weight-bold" v-if="$vuetify.breakpoint.name === 'xs'">Échangez</span>
              avec les agriculteurs qui ont testé des pratiques qui vous intéressent
            </v-card-text>
          </v-card>
        </v-col>
        <v-col cols="12" sm="4">
          <v-card flat>
            <v-card-title
              v-if="$vuetify.breakpoint.name !== 'xs'"
              style="color: #2c3e50; margin-bottom: 5px; padding: 0 0 5px 0;"
            >Partagez</v-card-title>
            <v-card-text class="pa-0" style="color: #2c3e50;">
              <span class="font-weight-bold" v-if="$vuetify.breakpoint.name === 'xs'">Partagez</span>
              ce que vous mettez en place sur votre exploitation
            </v-card-text>
          </v-card>
        </v-col>
      </v-row>

      <v-btn color="primary" style="margin: 20px 0;" href="#explore-xp">
        <span class="text-none">J'explore les pratiques</span>
        <v-icon small style="margin-right: 5px;">mdi-arrow-right</v-icon>
      </v-btn>

      <!-- Experiment filters -->
      <h2
        class="title pa-0"
        id="explore-xp"
        style="margin: 16px 0px 10px 0px;"
      >Explorez les retours d'expérience</h2>
      <ExperimentFilter />

      <!-- Experiments by location -->
      <h2
        class="title pa-0"
        style="margin: 16px 0px 5px 0px;"
      >Des exploitations sur tout le territoire</h2>
      <p
        class="body-1 pa-0"
        style="margin: 5px 0px;"
      >Ces exploitantes et exploitants partagent leurs retours d'expériences sur des pratiques agricoles et leurs évolutions</p>
      <MapBlock />

      <!-- Stats -->
      <div
        style="background-color: rgb(224, 244, 238); margin: 30px -16px 0 -16px;padding: 16px;border-radius: 5px;"
      >
        <h2
          class="title pa-0"
          id="explore-xp"
          style="margin: 0px 0px 5px 0px;"
        >Le service Peps en chiffres</h2>
        <p
          class="body-1 pa-0"
          style="margin: 5px 0px;"
        >De la transparence sur les données de la communauté d'agriculteurs qui font confiance à Peps</p>
        <StatsCards />
      </div>

      <!-- Reviews cards -->
      <div>
        <h2 class="title pa-0" style="margin: 16px 0px 5px 0px;">Paroles de convaincus</h2>
        <p
          class="body-1 pa-0"
          style="margin: 5px 0px;"
        >Ces agriculteurs ont trouvé des réponses à leurs questions, pourquoi pas vous ?</p>
        <ReviewsBlock />
      </div>

      <!-- About us cards -->
      <h2
        class="title pa-0"
        id="explore-xp"
        style="margin: 20px 0px 5px 0px;"
      >Le projet Peps, qu'est-ce que c'est ?</h2>
      <p
        class="body-1 pa-0"
        style="margin: 5px 0px;"
      >Une philosophie, des personnes et une envie de travailler pour vous</p>
      <AboutUsCards />

      <!-- Contribution proposal -->
      <div style="margin: 20px 0 0px 15px;">
        Vous souhaitez partager votre expérience ?
        <v-btn
          @click="onShareXPClick"
          outlined
          color="primary"
          class="text-none primary--text"
          style="margin-left: 10px; margin-top: -2px;"
        >Partager une expérience</v-btn>
      </div>
    </v-container>
  </div>
</template>

<script>
import ExperimentFilter from "@/components/ExperimentFilter.vue"
import ContributionOverlay from "@/components/ContributionOverlay.vue"
import AboutUsCards from "@/components/AboutUsCards.vue"
import StatsCards from "@/components/StatsCards.vue"
import MapBlock from "@/components/MapBlock.vue"
import ReviewsBlock from "@/components/ReviewsBlock.vue"

export default {
  name: "Landing",
  metaInfo() {
    return {
      title:
        "Peps, les expériences d'agriculteurs - adventices ravageurs maladies",
      meta: [
        {
          description:
            "Grâce aux essais d’agriculteurs, trouvez des réponses à vos questions sur de nombreux thèmes (réduction des charges, autonomie, maladies…)",
        },
      ],
    }
  },
  components: {
    ExperimentFilter,
    ContributionOverlay,
    AboutUsCards,
    StatsCards,
    MapBlock,
    ReviewsBlock,
  },
  data() {
    return {
      showContributionOverlay: false,
    }
  },
  computed: {
    loggedUser() {
      return this.$store.state.loggedUser
    },
  },
  methods: {
    onShareXPClick() {
      window.sendTrackingEvent("Header", "shareXP", "Partager une expérience")
      if (this.loggedUser && this.loggedUser.farmer_id)
        this.$router.push({ name: "ExperimentEditor" })
      else if (this.loggedUser)
        window.alert("Vous n'avez pas un profil agriculteur sur notre site")
      else this.showContributionOverlay = true
    },
  },
}
</script>

<style scoped>
.leaflet-container {
  background: #f5f5f5;
  border-radius: 5px;
}
#landing-image {
  background: #fff;
  background-repeat: no-repeat;
  background-position: center;
  background-size: cover;
  padding-bottom: 10px;
}
</style>
