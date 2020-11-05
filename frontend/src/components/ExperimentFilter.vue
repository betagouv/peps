<template>
  <div>
    <ContributionOverlay
      :visible="showContributionOverlay"
      @done="showContributionOverlay = false"
    />
    <!-- Recherche -->
    <v-row class="align-center" style="padding:12px;">
      <v-text-field
        prepend-inner-icon="mdi-magnify"
        placeholder="Cherchez des mots clé"
        @input="searchTermChanged"
        ref="search"
        outlined
        hide-details="auto"
        clearable
      >
      </v-text-field>
      <div class="d-none d-sm-flex" style="width: 10px;margin-left: 10px;border-left: solid 1px #c4bfbf;height: 50px;"></div>
      <v-badge
            class="d-none d-sm-flex"
            color="primary"
            :content="hiddenFilters"
            :value="hiddenFilters"
            overlap
          >
            <v-btn
              outlined
              :color="showFilterArea || hiddenFilters > 0 ? 'primary' : '#999'"
              class="text-none"
              @click="showFilterArea = !showFilterArea"
            >
              <v-icon>mdi-filter-variant</v-icon>Filtrer
            </v-btn>
          </v-badge>
    </v-row>
    
    <v-container
      :class="{'d-none': removeFilterArea}"
      style="
        padding-top: 10px;
        padding-bottom: 10px;
        border: 1px solid rgba(51, 51, 51, 0.11);
        border-radius: 5px;
        margin-top: 10px;
        min-width: 100%;
      "
    >
      <v-row class="pa-0 ma-0">
        <v-col cols="12">
          <v-badge
            class="d-sm-none"
            color="primary"
            :content="hiddenFilters"
            :value="hiddenFilters"
            overlap
          >
            <v-btn
              outlined
              :color="showFilterArea || hiddenFilters > 0 ? 'primary' : '#999'"
              class="text-none"
              @click="showFilterArea = !showFilterArea"
            >
              <v-icon>mdi-filter-variant</v-icon>Filtrer
            </v-btn>
          </v-badge>
        </v-col>

        <!-- Filter Thématique mobile and tablet -->
        <v-col
          :class="{
            filter: true,
            'd-none': !showFilterArea,
          }"
          cols="12"
          sm="6"
        >
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
            class="filter-select"
            v-model="activeFilters.tags"
            @change="(x) => sendFilterChangeEvent('tags', x)"
          ></v-select>
        </v-col>

        <!-- Filter Department -->
        <v-col
          :class="{ filter: true, 'd-none': !showFilterArea }"
          cols="12"
          sm="6"
        >
          <div class="filter-title">Département de l'exploitation</div>
          <v-select
            hide-details
            chips
            deletable-chips
            small-chips
            :items="departmentsSelectItems"
            :item-text="departmentDisplayText"
            item-value="code"
            outlined
            multiple
            placeholder="Tous les départements"
            class="filter-select"
            v-model="activeFilters.departments"
            @change="(x) => sendFilterChangeEvent('departments', x)"
          ></v-select>
        </v-col>

        <!-- Filter Cultures -->
        <v-col
          :class="{ filter: true, 'd-none': !showFilterArea }"
          cols="12"
          sm="6"
        >
          <div class="filter-title">Cultures</div>

          <v-select
            hide-details
            chips
            deletable-chips
            small-chips
            multiple
            outlined
            class="filter-select"
            :items="cultures"
            v-model="activeFilters.cultures"
            placeholder="Toutes les cultures"
            @change="(x) => sendFilterChangeEvent('cultures', x)"
          ></v-select>
        </v-col>

        <!-- Filter Agriculture type -->
        <v-col
          :class="{ filter: true, 'd-none': !showFilterArea }"
          cols="12"
          sm="6"
        >
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
            class="filter-select"
            v-model="activeFilters.agricultureTypes"
            @change="(x) => sendFilterChangeEvent('agriculture types', x)"
          ></v-select>
        </v-col>

        <!-- Filter Livestock -->
        <v-col cols="12" sm="6" :class="{ 'd-none': !showFilterArea }">
          <div class="filter-title">Uniquement l'élevage</div>
          <v-checkbox
            hide-details
            label="Oui"
            style="margin-top: 3px"
            v-model="activeFilters.livestock"
            @change="
              sendFilterChangeEvent('livestock', [`${activeFilters.livestock}`])
            "
          ></v-checkbox>
        </v-col>
      </v-row>
    </v-container>

    <ExperimentsCards
      v-if="filteredExperiments.length > 0"
      :experiments="filteredExperiments"
    />
    <div
      v-else
      class="d-flex flex-column align-center pa-5"
      style="background: #eee; border-radius: 5px; margin-top: 10px"
    >
      <v-icon class="pa-3" color="#999">mdi-beaker-remove-outline</v-icon>
      <p class="pa-3 caption" style="color: #999; margin-bottom: 10px">
        Il n'y a pas encore de retours d'expérience qui correspondent à vos
        critères, à vous d'en ajouter une !
      </p>
      <v-btn
        color="primary"
        outlined
        style="margin-bottom: 20px"
        @click="onShareXPClick"
      >
        <v-icon color="primary" small style="margin-right: 5px"
          >mdi-beaker-plus-outline</v-icon
        >
        <span style="font-weight: bold" class="caption text-none"
          >Proposer une expérience</span
        >
      </v-btn>
    </div>
  </div>
</template>

<script>
import ExperimentsCards from "@/components/grids/ExperimentsCards"
import ContributionOverlay from "@/components/ContributionOverlay.vue"
import Fuse from "fuse.js"
import { normalizeSync } from 'normalize-diacritics'

export default {
  name: "ExperimentFilter",
  components: { ExperimentsCards, ContributionOverlay },
  data() {
    return {
      menu: false,
      showContributionOverlay: false,
      showFilterArea: false,
      activeFilters: {
        tags: [],
        agricultureTypes: [],
        cultures: [],
        livestock: false,
      },
      searchTerm: "",
      searchDebounceTimer: null,
      searchDebounceMs: 300
    }
  },
  computed: {

    fuse() {
      return new Fuse(this.$store.getters.experimentBriefs, {
        threshold: 0.4,
        ignoreLocation: true,
        getFn() {
          const fn = Fuse.config.getFn.apply(this, arguments)
          if (typeof(fn) === 'string')
            return normalizeSync(fn).replace(/_/g, " ")
          if (fn && fn.constructor === Array)
            return fn.map(normalizeSync)
          return fn
        },
        keys: [
          {
            name: "name",
            weight: 4
          },
          {
            name: "short_name",
            weight: 5
          },
          {
            name: "cultures",
            weight: 2
          },
          {
            name: "objectives",
            weight: 1
          }
        ]
      })
    },
    searchResults() {
      return this.searchTerm ? this.fuse.search(this.searchTerm).map(x => x.item) : this.$store.getters.experimentBriefs
    },
    filteredExperiments() {
      return this.searchResults.filter((x) => {
        const tagSelected =
          this.activeFilters.tags.length === 0 ||
          (!!x.tags &&
            x.tags.some((y) => this.activeFilters.tags.indexOf(y) > -1))

        const departmentSelected =
          this.activeFilters.departments.length === 0 ||
          this.activeFilters.departments.find(code => x.postal_code.startsWith(code))

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
          tagSelected &&
          departmentSelected &&
          agricultureTypeSelected &&
          cultureSelected &&
          livestockSelected
        )
      })
    },

    activeDepartmentNumbers() {
      return [
        ...new Set(
          this.$store.getters.experimentBriefs
            .filter(
              (x) => !!x.postal_code && x.postal_code.length > 2
            )
            .flatMap((x) => x.postal_code.startsWith('97') ?
              x.postal_code.substr(0, 3) :
              x.postal_code.substr(0, 2))
            .filter((x) => !!x)
        ),
      ]
    },

    experimentTags() {
      return [
        ...new Set(
          this.$store.getters.experimentBriefs
            .flatMap((x) => x.tags)
            .filter((x) => !!x && x !== "Autre")
            .sort()
        ),
      ]
    },

    cultures() {
      return [
        ...new Set(
          this.$store.getters.experimentBriefs
            .flatMap((x) => x.cultures)
            .filter((x) => !!x)
            .sort()
        ),
      ]
    },

    agricultureTypes() {
      return [
        ...new Set(
          this.$store.getters.experimentBriefs
            .flatMap((x) => x.agriculture_types)
            .filter((x) => !!x && x !== "Autre")
            .sort()
        ),
      ]
    },

    departmentsSelectItems() {
      const activeDepartments = this.departments
        .filter((x) => this.activeDepartmentNumbers.indexOf(x.code) !== -1)
        .map((x) => {
          x.disabled = false
          return x
        })
      const inactiveDepartments = this.departments
        .filter((x) => this.activeDepartmentNumbers.indexOf(x.code) === -1)
        .map((x) => {
          x.disabled = true
          return x
        })

      return [
        ...activeDepartments,
        {
          header: "Pas encore de données sur ces départements :",
        },
        ...inactiveDepartments,
      ]
    },

    departments() {
      const mapDepartments = this.$store.state.geojson
        ? this.$store.state.geojson.features.map((x) => x.properties)
        : []
      const domToms = [{
        "code": "971",
        "nom": "Guadeloupe"
      },{
        "code": "972",
        "nom": "Martinique"
      }, {
        "code": "973",
        "nom": "Guyane"
      }, {
        "code": "974",
        "nom": "La Réunion"
      }, {
        "code": "976",
        "nom": "Mayotte"
      }]
      return mapDepartments.concat(domToms)
    },
    hiddenTagFilters() {
      // On desktop mode, how many tag filters under the "+plus" chip are active ?
      return this.experimentTags
        .slice(5)
        .filter((x) => this.activeFilters.tags.indexOf(x) > -1).length
    },
    hiddenFilters() {
      // How many filters are active and under the collapsable drawer ?
      let count = 0
      if (this.activeFilters.tags.length > 0) count++
      if (this.activeFilters.departments.length > 0) count++
      if (this.activeFilters.cultures.length > 0) count++
      if (this.activeFilters.agricultureTypes.length > 0) count++
      if (this.activeFilters.livestock) count++
      return count
    },
    removeFilterArea() {
      const isMobile = this.$vuetify.breakpoint.name === "xs"
      return !isMobile && !this.showFilterArea
    }
  },
  methods: {
    toggleTagFilter(filter) {
      const index = this.activeFilters.tags.indexOf(filter)
      const itemIsSelected = index > -1
      if (itemIsSelected) this.activeFilters.tags.splice(index, 1)
      else this.activeFilters.tags.push(filter)
      this.sendFilterChangeEvent("tags", this.activeFilters.tags)
    },
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
      const newFilter = value && value.length > 0 ? value.join(", ") : "None"
      window.sendTrackingEvent(
        this.$route.name,
        "filter change",
        `${parameter} - ${newFilter}`
      )
    },
    onShareXPClick() {
      const loggedUser = this.$store.state.loggedUser
      window.sendTrackingEvent(
        this.$route.name,
        "filter empty view",
        "Partager une expérience"
      )
      if (loggedUser && loggedUser.farmer_id)
        this.$router.push({ name: "ExperimentEditor" })
      else if (loggedUser)
        window.alert("Vous n'avez pas un profil agriculteur sur notre site")
      else this.showContributionOverlay = true
    },
    searchTermChanged(searchTerm) {
      clearTimeout(this.searchDebounceTimer)
      this.searchDebounceTimer = setTimeout(() => {
        this.searchTerm = searchTerm ? normalizeSync(searchTerm) : searchTerm
        window.sendTrackingEvent(this.$route.name, "search term", this.searchTerm)
      }, this.searchDebounceMs)
    }
  },
  watch: {
    "activeFilters.tags": function () {
      this.$store.dispatch("updateFilters", { filters: this.activeFilters })
    },
    "activeFilters.departments": function () {
      this.$store.dispatch("updateFilters", { filters: this.activeFilters })
    },
    "activeFilters.agricultureTypes": function () {
      this.$store.dispatch("updateFilters", { filters: this.activeFilters })
    },
    "activeFilters.cultures": function () {
      this.$store.dispatch("updateFilters", { filters: this.activeFilters })
    },
    "activeFilters.livestock": function () {
      this.$store.dispatch("updateFilters", { filters: this.activeFilters })
    }
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
