<template>
  <div>
    <ContributionOverlay
      :visible="showContributionOverlay"
      @done="showContributionOverlay = false"
    />
    <v-container class="constrained">
      <!-- Intro top -->
      <v-row>
        <v-col cols="12">
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
      </v-row>

      <!-- Newsletter -->
      <div
        style="background-color: rgb(224, 244, 238); margin: 10px -16px 30px -16px;padding: 16px;border-radius: 5px;"
      >
      <p
        class="body-1 pa-0"
        style="margin: 5px 0px;"
      >Les retours d'expérience de ceux et celles qui font l'agriculture de demain, directement dans votre boite email.</p>
      <MailChimpForm />
      </div>


      <!-- Experiment filters -->
      <h2
        class="title pa-0"
        id="explore-xp"
        style="margin: 30px 0px 10px 0px;"
      >Explorez les retours d'expérience</h2>
      <ExperimentFilter v-if="experimentsFetched" />

      <!-- Experiments by location -->
      <h2
        class="title pa-0"
        style="margin: 16px 0px 5px 0px;"
        id="location"
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
          style="margin: 0px 0px 5px 0px;"
          id="stats"
        >Le service Peps en chiffres</h2>
        <p
          class="body-1 pa-0"
          style="margin: 5px 0px;"
        >De la transparence sur les données de la communauté d'agriculteurs qui font confiance à Peps</p>
        <StatsCards />
      </div>

      <!-- Reviews cards -->
      <div>
        <h2 class="title pa-0" id="reviews" style="margin: 16px 0px 5px 0px;">Paroles de convaincus</h2>
        <p
          class="body-1 pa-0"
          style="margin: 5px 0px;"
        >Ces agriculteurs ont trouvé des réponses à leurs questions, pourquoi pas vous ?</p>
        <ReviewsBlock />
      </div>

      <!-- About us cards -->
      <h2
        class="title pa-0"
        style="margin: 20px 0px 5px 0px;"
        id="about"
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
import Vue from "vue"
import Constants from "@/constants"
import ExperimentFilter from "@/components/ExperimentFilter.vue"
import ContributionOverlay from "@/components/ContributionOverlay.vue"
import AboutUsCards from "@/components/AboutUsCards.vue"
import StatsCards from "@/components/StatsCards.vue"
import MapBlock from "@/components/MapBlock.vue"
import ReviewsBlock from "@/components/ReviewsBlock.vue"
import MailChimpForm from "@/components/MailChimpForm.vue"

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
    MailChimpForm
  },
  data() {
    return {
      showContributionOverlay: false,
      experimentsFetched: false
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
  mounted() {
    const experimentBriefs = this.$store.state.experimentBriefs
    if (experimentBriefs && experimentBriefs.length > 0) {
      this.experimentsFetched = true
      return
    }

    this.$store.commit('SET_EXPERIMENT_BRIEFS_LOADING', Constants.LoadingStatus.LOADING)
    Vue.http.get('/api/v1/experimentBriefs').then(response => {
      const body = response.body
      this.$store.commit('SET_EXPERIMENT_BRIEFS', body)
      this.$store.commit('SET_EXPERIMENT_BRIEFS_LOADING', Constants.LoadingStatus.SUCCESS)
      this.experimentsFetched = true
    }).catch(() => {
      this.$store.commit('SET_EXPERIMENT_BRIEFS_LOADING', Constants.LoadingStatus.ERROR)
      this.experimentsFetched = false
    })
  }
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
