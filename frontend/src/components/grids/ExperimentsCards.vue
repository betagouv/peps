<template>
  <v-container :class="{'constrained': true, 'transition-backwards': lastTransitionBackwards}">
    <v-pagination
      @input="onPaginationInput"
      v-if="pages > 1"
      v-model="page"
      :length="pages"
      color="#333"
      class="mb-3 mt-5"
    ></v-pagination>
    <transition-group name="list" tag="div" class="row" mode="out-in" style="margin-left: -24px; margin-right: -24px;">
      <v-col
        v-for="experiment in paginatedExperiments"
        :key="experiment.id"
        cols="12"
        sm="6"
        md="4"
      >
        <ExperimentCard :experiment="experiment" />
      </v-col>
    </transition-group>
    <v-pagination
      @input="onPaginationInput"
      color="#333"
      v-if="pages > 1"
      v-model="page"
      :length="pages"
      class="mb-0 mt-3"
    ></v-pagination>
  </v-container>
</template>

<script>
import ExperimentCard from "@/components/ExperimentCard"

export default {
  name: "ExperimentsCards",
  components: { ExperimentCard },
  data() {
    return {
      page: 1,
      lastTransitionBackwards: false
    }
  },
  props: {
    experiments: {
      type: Array,
      required: true
    }
  },
  methods: {
    onPaginationInput() {
      window.sendTrackingEvent(this.$route.name, "pagination", "page-" + this.page)
    }
  },
  computed: {
    cardsPerPage() {
      if (this.$vuetify.breakpoint.name === 'xs')
        return 6
      if (this.$vuetify.breakpoint.name === 'sm')
        return 8
      return 15
    },
    paginatedExperiments() {
      const startingIndex = (this.page - 1) * this.cardsPerPage
      return this.experiments.slice(
        startingIndex,
        startingIndex + this.cardsPerPage
      )
    },
    pages() {
      return Math.ceil(this.experiments.length / this.cardsPerPage)
    }
  },
  watch: {
    page(newPage, oldPage) {
      this.lastTransitionBackwards = newPage < oldPage
      this.$store.dispatch('updatePagination', { page: newPage })
    },
    experiments() {
      this.page = 1
    }
  },
  mounted() {
    this.page = this.$store.state.xpPaginationPage
  }
}
</script>

<style scoped>
.list-item {
  display: inline-block;
  margin-right: 10px;
}
.list-enter-active,
.list-leave-active {
  transition: all 0.5s;
}
.list-enter,
.list-leave-to {
  opacity: 0;
  transform: translateX(50px);
}
.transition-backwards .list-enter,
.transition-backwards .list-leave-to {
  transform: translateX(-50px);
}
.list-leave-active {
  display: none;
}
</style>
