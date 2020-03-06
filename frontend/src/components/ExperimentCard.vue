<template>
  <v-card class="pa-0 fill-height flex-container" style="max-height: 450px;" outlined>
    <v-img
      class="white--text align-end flex-fix-item"
      height="120px"
      style="background: #DDD;"
      :src="experiment.image"
    />
    <v-card-text style="padding-bottom: 0; padding-top: 10px;">
      <v-icon left small v-for="(iconName, index) in icons" :key="index">{{ iconName }}</v-icon>
    </v-card-text>
    <v-card-title class="flex-fix-item" style="padding-top: 5px; padding-bottom: 5px;">{{experiment.title}}</v-card-title>
    <v-card-text class="description flex-shrink-item">
      {{experiment.description}}
      <div class="gradient" v-if="showDescriptionGradient"></div>
    </v-card-text>
    <div class="pa-5 flex-fix-item">
      <v-btn
        block
        class="text-none"
        color="primary"
        max-width="50"
        @click="goToExperiment(experiment)"
      >En savoir plus</v-btn>
    </div>
  </v-card>
</template>

<script>
export default {
  name: "ExperimentCard",
  components: {},
  props: {
    experiment: {
      type: Object,
      required: true,
    }
  },
  data() {
    return {
      showDescriptionGradient: false
    }
  },
  computed: {
    icons() {
      const icons = {
        "adventices": "mdi-sprout",
        "insectes": "mdi-ladybug",
        "maladies": "mdi-bottle-tonic-plus",
        "productivite": "mdi-chart-bell-curve-cumulative",
        "biodiversite": "mdi-bee",
        "sol": "mdi-image-filter-hdr",
        "fourrages": "mdi-cow",
        "nouvelles-cultures": "mdi-corn",
        "oad": "mdi-cellphone-information"
      }
      return this.experiment.tags.map(x => x in icons ? icons[x] : null).filter(x => x != null)
    }
  },
  methods: {
    goToExperiment(experiment) {
      this.$router.push({
        name: "Experiment",
        params: { expName: experiment.title }
      })
    }
  },
  mounted() {
    if (this.$el) {
      const domElement = this.$el.querySelector(".description")
      this.showDescriptionGradient =
        domElement.scrollHeight > domElement.offsetHeight
    }
  }
}
</script>

<style scoped>
.flex-container {
  display: flex;
  flex-direction: column;
  flex-wrap: nowrap;
}
.flex-shrink-item {
  flex: 0 1 auto;
  overflow: hidden;
  position: relative;
}
.flex-fix-item {
  flex: 0 0 auto;
}
.flex-shrink-item .gradient {
  position: absolute;
  background-image: linear-gradient(transparent, white);
  height: 40px;
  bottom: 0;
  left: 0;
  right: 0;
}
</style>
