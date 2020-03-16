<template>
  <div>
    <v-row style="padding: 0 16px 0 16px;">
      <v-text-field prepend-icon="mdi-file-search" />
      <v-btn outlined color="primary" style="margin: 10px 0 0 10px;">
        <v-icon small style="margin: 0 5px 0 0;">mdi-magnify</v-icon>Chercher
      </v-btn>
      <v-spacer class="hidden-sm-and-down" />
    </v-row>
    <v-row style="padding: 0 16px 0 16px;">
      <v-chip
        @click="toggleFilter(filter)"
        class="ma-2"
        v-for="(filter, index) in filters"
        :key="index"
        :outlined="selectedFilters.indexOf(filter) === -1"
        :dark="selectedFilters.indexOf(filter) > -1"
        :color="selectedFilters.indexOf(filter) > -1 ? 'primary' : '#999'"
      >
        <v-icon left>{{filter.icon}}</v-icon>
        {{filter.text}}
      </v-chip>
    </v-row>
    <ExperimentsCards :experiments="filteredExperiments" />
  </div>
</template>

<script>
import ExperimentsCards from "@/components/grids/ExperimentsCards"

export default {
  name: "ExperimentFilter",
  components: { ExperimentsCards },
  data() {
    return {
      filters: [
        {
          icon: "mdi-sprout",
          filter: "adventices",
          text: "Adventices"
        },
        {
          icon: "mdi-ladybug",
          filter: "insectes",
          text: "Insectes"
        },
        {
          icon: "mdi-bottle-tonic-plus",
          filter: "maladies",
          text: "Maladies"
        },
        {
          icon: "mdi-chart-bell-curve-cumulative",
          filter: "productivite",
          text: "Productivité"
        },
        {
          icon: "mdi-bee",
          filter: "biodiversite",
          text: "Biodiversité"
        },
        {
          icon: "mdi-image-filter-hdr",
          filter: "sol",
          text: "Sol"
        },
        {
          icon: "mdi-cow",
          filter: "Fourrages",
          text: "Fourrages"
        },
        {
          icon: "mdi-corn",
          filter: "nouvelles-cultures",
          text: "Nouvelles cultures"
        },
        {
          icon: "mdi-cellphone-information",
          filter: "oad",
          text: "OAD"
        }
      ],
      selectedFilters: []
    }
  },
  computed: {
    filteredExperiments() {
      if (this.selectedFilters.length === 0)
        return this.$store.state.experiments
      const filterValues = this.selectedFilters.map(x => x.filter)
      return this.$store.state.experiments.filter(x =>
        !!x.tags && x.tags.some(y => filterValues.indexOf(y) > -1)
      )
    }
  },
  methods: {
    toggleFilter(filter) {
      const index = this.selectedFilters.indexOf(filter)
      const itemIsSelected = index > -1
      if (itemIsSelected) {
        this.selectedFilters.splice(index, 1)
      } else {
        this.selectedFilters.push(filter)
      }
    }
  }
}
</script>