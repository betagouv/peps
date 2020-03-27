<template>
  <div>
    <!-- <v-row style="padding: 0 16px 0 16px;">
      <v-text-field prepend-icon="mdi-file-search" />
      <v-btn outlined color="primary" style="margin: 10px 0 0 10px;">
        <v-icon small style="margin: 0 5px 0 0;">mdi-magnify</v-icon>Chercher
      </v-btn>
      <v-spacer class="hidden-sm-and-down" />
    </v-row>-->
    <v-row style="padding: 0 16px 0 16px;">
      <v-chip
        @click="toggleFilter(filter)"
        class="ma-2"
        v-for="(filter, index) in filters"
        :key="index"
        :outlined="selectedFilters.indexOf(filter) === -1"
        :dark="selectedFilters.indexOf(filter) > -1"
        :color="selectedFilters.indexOf(filter) > -1 ? 'primary' : '#999'"
      >{{filter}}</v-chip>
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
      selectedFilters: []
    }
  },
  computed: {
    filteredExperiments() {
      if (this.selectedFilters.length === 0)
        return this.$store.state.experiments
      return this.$store.state.experiments.filter(
        x => !!x.tags && x.tags.some(y => this.selectedFilters.indexOf(y) > -1)
      )
    },
    filters() {
      return [...new Set(this.$store.state.experiments.flatMap(x => x.tags).filter(x => !!x))]
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