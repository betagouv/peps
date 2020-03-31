<template>
  <div>
    <Title :title="title" :breadcrumbs="breadcrumbs" />
    <ContributionOverlay
      :visible="showContributionOverlay"
      @done="showContributionOverlay = false"
    />
    <v-container class="constrained">
      <div style="margin-top: 20px;">
        <p class="body-1">
          Si vous faites déjà parti des testeurs et vous êtes déjà en contact avec l'équipe Peps,
          veuillez remplir le questionnaire ci-dessous.
        </p>

        <p class="body-1">
          Sinon,
          <a @click="joinTest">contactez-nous</a> pour faire partie du groupe et partager vos expérimentations.
        </p>

        <v-divider class="ma-5"></v-divider>
        <iframe
          class="airtable-embed"
          src="https://airtable.com/embed/shrsGaijZWpwEvByf?backgroundColor=green"
          frameborder="0"
          onmousewheel
          width="100%"
          height="533"
          style="background: transparent; border: 1px solid #ccc; box-shadow: 2px 2px 9px -5px #333;"
        ></iframe>
      </div>
    </v-container>
  </div>
</template>

<script>
import Title from "@/components/Title.vue"
import ContributionOverlay from "@/components/ContributionOverlay.vue"

export default {
  name: "Contribution",
  components: { Title, ContributionOverlay },
  data() {
    return {
      showContributionOverlay: false,
      title: "Proposez une expérimentation",
      breadcrumbs: [
        {
          text: "Carte des expérimentations",
          disabled: false,
          href: "/#/map"
        },
        {
          text: "Proposez une expérimentation",
          disabled: true
        }
      ]
    }
  },
  methods: {
    joinTest() {
      window.sendTrackingEvent(this.$route.name, "joinTest", "contactez-nous")
      this.showContributionOverlay = true
    }
  }
}
</script>

<style scoped>
.theme--light.v-card > .v-card__subtitle,
.theme--light.v-card > .v-card__text {
  color: rgba(0, 0, 0, 0.87);
}
.display-1 {
  margin-top: 25px;
  margin-bottom: 10px;
}
.title {
  margin-top: 10px;
  margin-bottom: 5px;
}
.body-2 {
  line-height: 1.375rem;
}
</style>
