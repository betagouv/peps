<template>
  <div>
    <v-row>
      <v-col v-for="stat in stats" :key="stat.label" cols="12" sm="6" md="4">
        <v-card tile elevation="0" color="transparent" class="secondary--text">
          <v-card-title
            style="font-size: 4em; line-height: normal;"
            class="primary--text justify-center justify-sm-start"
          >{{stat.value}}</v-card-title>
          <v-card-subtitle
            class="text-center text-sm-left justify-center justify-sm-start"
          >{{stat.label}}</v-card-subtitle>
        </v-card>
      </v-col>
    </v-row>
    <v-btn
      outlined
      color="primary"
      :to="{ name: 'Stats' }"
      class="text-none"
    >Voir les statistiques complètes</v-btn>
  </div>
</template>

<script>
export default {
  name: "StatsCards",
  computed: {
    stats() {
      const backendStats = this.$store.state.stats
      let stats = []
      if (backendStats && backendStats.approvedExperimentCount) {
        stats.push({
          value: backendStats.approvedExperimentCount,
          label: "Retours d'expérience d'agriculteurs",
        })
      }
      if (backendStats && backendStats.approvedFarmerCount) {
        stats.push({
          value: backendStats.approvedFarmerCount,
          label: "Profils d'exploitations",
        })
      }
      if (backendStats && backendStats.contactCount) {
        stats.push({
          value: backendStats.contactCount,
          label: "Mises en relation entre agriculteurs",
        })
      }
      return stats
    },
  },
}
</script>