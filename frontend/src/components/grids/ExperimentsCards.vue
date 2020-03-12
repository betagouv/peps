<template>
  <v-container :class="{'constrained': true, 'transition-backwards': lastTransitionBackwards}">
    <v-pagination v-model="page" :length="pages" color="#333"></v-pagination>
    <transition-group name="list" tag="div" class="row" mode="out-in">
      <v-col v-for="experiment in paginatedExperiments" :key="experiment.id" cols="12" sm="6" md="4">
        <ExperimentCard :experiment="experiment" />
      </v-col>
    </transition-group>
    <v-pagination v-model="page" :length="pages" color="#333"></v-pagination>
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
      cardsPerPage: 6,
      lastTransitionBackwards: false,
    }
  },
  props: {
    experiments: {
      type: Array,
      required: true
    }
  },
  computed: {
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
    },
    experiments() {
      this.page = 1
    }
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
