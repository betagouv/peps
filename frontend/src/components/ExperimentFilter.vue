<template>
  <div>
    <v-row style="padding: 0 16px 0 16px;">
      <v-col cols="12" md="10">
        <v-chip-group show-arrows>
          <v-chip
            small
            @click="toggleFilter(filter)"
            class="ma-2"
            v-for="(filter, index) in filters"
            :key="index"
            :outlined="selectedFilters.indexOf(filter) === -1"
            :dark="selectedFilters.indexOf(filter) > -1"
            :color="selectedFilters.indexOf(filter) > -1 ? 'primary' : '#999'"
          >{{filter}}</v-chip>
        </v-chip-group>
      </v-col>
      <v-col cols="12" md="2">
        <v-chip
          style="height: 48px; border-radius: 24px;"
          :outlined="!showFilterArea"
          :color="showFilterArea ? 'rgb(224, 244, 238)' : '#999'"
          @click="showFilterArea = !showFilterArea"
        >
          <v-icon>mdi-filter-variant</v-icon>Filtrer
        </v-chip>
      </v-col>
    </v-row>
    <v-row v-if="showFilterArea" style="padding-left: 20px; padding-right: 20px;">
      <!-- Filter Department -->
      <v-col cols="12" sm="6" md="3">
        <div class="filter-title">Département de l'exploitation</div>
        <v-select outlined dense class="filter-select"></v-select>
      </v-col>

      <!-- Filter Cultures -->
      <v-col cols="12" sm="6" md="3">
        <div class="filter-title">Cultures</div>
        <v-select outlined dense class="filter-select"></v-select>
      </v-col>

      <!-- Filter Agriculture type -->
      <v-col cols="12" sm="6" md="3">
        <div class="filter-title">Type d'agriculture</div>
        <v-select outlined dense class="filter-select"></v-select>
      </v-col>

      <!-- Filter Livestock -->
      <v-col cols="12" sm="6" md="3">
        <div class="filter-title">Uniquement l'élevage</div>
        <v-checkbox label="Oui" style="margin-top: 3px;"></v-checkbox>
      </v-col>
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
      selectedFilters: [],
      showFilterArea: false,
    }
  },
  computed: {
    filteredExperiments() {
      let approvedXps = this.$store.getters.experiments.filter(
        (x) => !!x.approved
      )
      if (this.selectedFilters.length === 0) return approvedXps
      return approvedXps.filter(
        (x) =>
          !!x.tags && x.tags.some((y) => this.selectedFilters.indexOf(y) > -1)
      )
    },
    filters() {
      return [
        ...new Set(
          this.$store.getters.experiments
            .filter((x) => !!x.approved)
            .flatMap((x) => x.tags)
            .filter((x) => !!x)
        ),
      ]
    },
  },
  methods: {
    toggleFilter(filter) {
      const index = this.selectedFilters.indexOf(filter)
      const itemIsSelected = index > -1
      if (itemIsSelected) {
        this.selectedFilters.splice(index, 1)
        window.sendTrackingEvent(
          this.$route.name,
          "filter",
          "deselected-" + filter
        )
      } else {
        this.selectedFilters.push(filter)
        window.sendTrackingEvent(
          this.$route.name,
          "filter",
          "selected-" + filter
        )
      }
    },
  },
  watch: {
    selectedFilters(newFilters) {
      this.$store.dispatch("updateFilters", { filters: newFilters })
    },
  },
  beforeMount() {
    this.selectedFilters = this.$store.state.xpSelectionFilters
  },
}
</script>

<style scoped>
.filter-title {
  font-size: 0.85em;
  font-weight: bold;
  margin-bottom: 5px;
}
</style>
<style>

.v-slide-group__next {
  box-shadow: -8px 0px 5px -6px #3E3E3E6B;
  background: rgb(224, 244, 238);
  border-top-left-radius: 0%;
  border-top-right-radius: 50%;
  border-bottom-right-radius: 50%;
  border-bottom-left-radius: 0%;
}
.v-slide-group__next.v-slide-group__next--disabled {
  box-shadow: none;
  background: #EEE;
}
.v-slide-group__prev {
  box-shadow: 8px 0px 5px -6px #3E3E3E6B;
  background: rgb(224, 244, 238);
  border-top-left-radius: 50%;
  border-top-right-radius: 0%;
  border-bottom-right-radius: 0%;
  border-bottom-left-radius: 50%;
}
.v-slide-group__prev.v-slide-group__prev--disabled {
  box-shadow: none;
  background: #EEE;
}
</style>
