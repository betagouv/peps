<template>
  <div>
    <v-container
      v-if="true"
      style="padding-top: 10px; padding-bottom: 10px; border: 1px solid rgba(51, 51, 51, 0.11); border-radius: 5px; margin-top: 10px; min-width: 100%;"
    >
      <v-row class="pa-0 ma-0">
        <!-- Filter Thématique -->
        <v-col class="filter" cols="12" sm="6" md="5">
          <div class="filter-title">Thématique</div>
          <v-select
            hide-details
            chips
            deletable-chips
            small-chips
            :items="experimentTags"
            outlined
            multiple
            placeholder="Toutes les thématiques"
            class="filter-select caption"
            v-model="activeFilters.tags"
            @change="(x) => sendFilterChangeEvent('tags', x)"
          ></v-select>
        </v-col>

        <!-- Filter Department -->
        <v-col class="filter" cols="12" sm="6" md="5">
          <div class="filter-title">Département de l'exploitation</div>
          <v-select
            hide-details
            chips
            deletable-chips
            small-chips
            :items="departments"
            :item-text="departmentDisplayText"
            item-value="code"
            outlined
            multiple
            placeholder="Tous les départements"
            class="filter-select caption"
            v-model="activeFilters.departments"
            @change="(x) => sendFilterChangeEvent('departments', x)"
          ></v-select>
        </v-col>

        <!-- Filter Cultures -->
        <v-col class="filter" cols="12" sm="6" md="5">
          <div class="filter-title">Cultures</div>

          <v-select
            hide-details
            chips
            deletable-chips
            small-chips
            multiple
            outlined
            class="filter-select caption"
            :items="cultures"
            v-model="activeFilters.cultures"
            placeholder="Toutes les cultures"
            @change="(x) => sendFilterChangeEvent('cultures', x)"
          ></v-select>
        </v-col>

        <!-- Filter Agriculture type -->
        <v-col class="filter" cols="12" sm="6" md="5">
          <div class="filter-title">Type d'agriculture</div>
          <v-select
            hide-details
            chips
            deletable-chips
            small-chips
            outlined
            multiple
            placeholder="Tous les types d'agriculture"
            :items="agricultureTypes"
            class="filter-select caption"
            v-model="activeFilters.agricultureTypes"
            @change="(x) => sendFilterChangeEvent('agriculture types', x)"
          ></v-select>
        </v-col>

        <!-- Filter Livestock -->
        <v-col cols="12" sm="6" md="2">
          <div class="filter-title">Uniquement l'élevage</div>
          <v-checkbox
            hide-details
            label="Oui"
            style="margin-top: 3px;"
            v-model="activeFilters.livestock"
            @mouseup="sendFilterChangeEvent('livestock', [`${!activeFilters.livestock}`])"
          ></v-checkbox>
        </v-col>
      </v-row>
    </v-container>

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
      showFilterArea: false,
      activeFilters: {
        tags: [],
        departments: [],
        agricultureTypes: [],
        cultures: [],
        livestock: false,
      },
    }
  },
  computed: {
    filteredExperiments() {
      return this.$store.getters.experiments.filter((x) => {
        const isApproved = !!x.approved
        const tagSelected =
          this.activeFilters.tags.length === 0 ||
          (!!x.tags &&
            x.tags.some((y) => this.activeFilters.tags.indexOf(y) > -1))
        const departmentSelected =
          this.activeFilters.departments.length === 0 ||
          this.activeFilters.departments.indexOf(x.postal_code.substr(0, 2)) !==
            -1
        const agricultureTypeSelected =
          this.activeFilters.agricultureTypes.length === 0 ||
          this.activeFilters.agricultureTypes.some(
            (y) => x.agriculture_types.indexOf(y) > -1
          )
        const cultureSelected =
          this.activeFilters.cultures.length === 0 ||
          this.activeFilters.cultures.some(
            (y) => !!x.cultures && x.cultures.indexOf(y) > -1
          )
        const livestockSelected =
          !this.activeFilters.livestock ||
          (x.livestock_types && x.livestock_types.length > 0)

        return (
          isApproved &&
          tagSelected &&
          departmentSelected &&
          agricultureTypeSelected &&
          cultureSelected &&
          livestockSelected
        )
      })
    },

    experimentTags() {
      return [
        ...new Set(
          this.$store.getters.experiments
            .filter((x) => !!x.approved)
            .flatMap((x) => x.tags)
            .filter((x) => !!x)
            .sort()
        ),
      ]
    },
    cultures() {
      return [
        ...new Set(
          this.$store.getters.experiments
            .filter((x) => !!x.approved)
            .flatMap((x) => x.cultures)
            .filter((x) => !!x)
            .sort()
        ),
      ]
    },

    agricultureTypes() {
      return [
        ...new Set(
          this.$store.getters.experiments
            .filter((x) => !!x.approved)
            .flatMap((x) => x.agriculture_types)
            .filter((x) => !!x)
            .sort()
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
    departmentDisplayText(department) {
      return `${department.code} - ${department.nom}`
    },
    departmentNumberToDisplayText(departmentNumber) {
      const department = this.departments.find(
        (x) => x.code === departmentNumber
      )
      if (department) {
        return this.departmentDisplayText(department)
      }
      return ""
    },
    sendFilterChangeEvent(parameter, value) {
      const newFilter = value && value.length > 0 ? value.join(', ') : 'None'
      window.sendTrackingEvent(
        this.$route.name,
        "filter change",
        `${parameter} - ${newFilter}`
      )
    }
  },
  watch: {
    activeFilters(newFilters) {
      this.$store.dispatch("updateFilters", { filters: newFilters })
    },
  },
  beforeMount() {
    this.activeFilters = this.$store.state.xpSelectionFilters
  },
}
</script>

<style scoped>
.filter-title {
  font-size: 0.85em;
  font-weight: bold;
  margin-bottom: 10px;
}
.filter {
  padding: 5px 5px 5px 5px;
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
