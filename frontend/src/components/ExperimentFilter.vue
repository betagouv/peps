<template>
  <div>
    <v-row style="padding: 0 16px 0 16px;">
      <v-col cols="12" sm="10">
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
      <v-col cols="12" sm="2">
        <v-chip
          style="height: 48px; border-radius: 24px;"
          :outlined="!showFilterArea"
          :color="showFilterArea ? 'rgb(224, 244, 238)' : '#999'"
          @click="showFilterArea = !showFilterArea"
        >
          <v-badge dot color="amber" offset-y="5" offset-x="3" :value="!!filteredDepartment">
            <v-icon>mdi-filter-variant</v-icon>Filtrer
          </v-badge>
        </v-chip>
      </v-col>
    </v-row>
    <v-row v-if="showFilterArea" style="padding-left: 20px; padding-right: 20px;">
      <!-- Filter Department -->
      <v-col cols="12" sm="6" md="3">
        <v-badge dot color="amber" :value="!!filteredDepartment">
          <div class="filter-title">Département de l'exploitation</div>
        </v-badge>
        <v-select
          hide-details
          :items="departments"
          :item-text="departmentDisplayText"
          item-value="code"
          outlined
          clearable
          dense
          placeholder="Tous les départements"
          class="filter-select caption"
          v-model="filteredDepartment"
        ></v-select>
      </v-col>

      <!-- Filter Cultures -->
      <v-col cols="12" sm="6" md="3">
        <v-badge dot color="amber" :value="false">
          <div class="filter-title">Cultures</div>
        </v-badge>
        <v-select hide-details outlined dense class="filter-select"></v-select>
      </v-col>

      <!-- Filter Agriculture type -->
      <v-col cols="12" sm="6" md="3">
        <v-badge dot color="amber" :value="false">
          <div class="filter-title">Type d'agriculture</div>
        </v-badge>
        <v-select hide-details outlined dense class="filter-select"></v-select>
      </v-col>

      <!-- Filter Livestock -->
      <v-col cols="12" sm="6" md="3">
        <v-badge dot color="amber" :value="false">
          <div class="filter-title">Uniquement l'élevage</div>
        </v-badge>
        <v-checkbox hide-details label="Oui" style="margin-top: 3px;"></v-checkbox>
      </v-col>
    </v-row>

    <ExperimentsCards v-if="filteredExperiments.length > 0" :experiments="filteredExperiments" />
    <div
      v-else
      class="d-flex flex-column align-center pa-5 ma-5"
      style="background: #eee; border-radius: 5px;"
    >
      <v-icon class="pa-3" color="#999">mdi-beaker-remove-outline</v-icon>
      <p
        class="pa-3 caption"
        style="color: #999;"
      >Nous n'avons pas trouvé des retours d'expérience avec les filtres indiqués</p>
    </div>
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
      filteredDepartment: null,
    }
  },
  computed: {
    filteredExperiments() {
      return this.$store.getters.experiments.filter((x) => {
        const isApproved = !!x.approved
        const tagSelected =
          this.selectedFilters.length === 0 ||
          (!!x.tags && x.tags.some((y) => this.selectedFilters.indexOf(y) > -1))
        const departmentSelected =
          !this.filteredDepartment ||
          x.postal_code.substr(0, 2) === this.filteredDepartment

        return isApproved && tagSelected && departmentSelected
      })
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
    departments() {
      return this.$store.state.geojson
        ? this.$store.state.geojson.features.map((x) => x.properties)
        : []
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
    departmentDisplayText(department) {
      return `${department.code} - ${department.nom}`
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
  margin-bottom: 10px;
}
</style>
<style>
.v-slide-group__next {
  box-shadow: -8px 0px 5px -6px #3e3e3e6b;
  background: rgb(224, 244, 238);
  border-top-left-radius: 0%;
  border-top-right-radius: 50%;
  border-bottom-right-radius: 50%;
  border-bottom-left-radius: 0%;
}
.v-slide-group__next.v-slide-group__next--disabled {
  box-shadow: none;
  background: #eee;
}
.v-slide-group__prev {
  box-shadow: 8px 0px 5px -6px #3e3e3e6b;
  background: rgb(224, 244, 238);
  border-top-left-radius: 50%;
  border-top-right-radius: 0%;
  border-bottom-right-radius: 0%;
  border-bottom-left-radius: 50%;
}
.v-slide-group__prev.v-slide-group__prev--disabled {
  box-shadow: none;
  background: #eee;
}
</style>
