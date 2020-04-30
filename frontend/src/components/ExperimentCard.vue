<template>
  <v-hover>
    <v-card
      class="pa-0 fill-height"
      style="max-height: 150px; overflow: hidden;"
      outlined
      slot-scope="{ hover }"
      :elevation="!disabled && hover ? 3 : elevation"
      :disabled="disabled"
      @click="goToExperiment()"
    >
      <div class="d-flex" style="height: 100%;">
        <v-img
          class="white--text align-end flex-fix-item"
          height="100%"
          width="80px"
          style="background: #DDD;"
          :src="experiment.images && experiment.images.length > 0 ? experiment.images[0].image : ''"
        />
        <div class="flex-container">
          <v-card-title
            class="flex-fix-item subtitle-2"
            style="padding-top: 10px; padding-bottom: 5px;"
          >{{experiment.name}}</v-card-title>
          <v-card-text class="caption flex-fix-item" style="padding-bottom: 0; padding-top: 0px;">
            <v-icon small left style="padding-bottom: 2px;">mdi-account</v-icon>
            {{experiment.farmer}}
          </v-card-text>
          <v-card-text class="description flex-shrink-item">
            {{experiment.objectives}}
            <div class="gradient" v-if="showDescriptionGradient"></div>
          </v-card-text>
        </div>
      </div>
    </v-card>
  </v-hover>
</template>

<script>
export default {
  name: "ExperimentCard",
  components: {},
  props: {
    experiment: {
      type: Object,
      required: true
    },
    disabled: {
      type: Boolean,
      default: false
    },
    elevation: {
      type: Number,
      default: 1
    }
  },
  data() {
    return {
      showDescriptionGradient: false
    }
  },
  methods: {
    goToExperiment() {
      window.sendTrackingEvent("ExperimentCard", "seeXP", this.experiment.name)
      this.$router.push({
        name: "Experiment",
        params: {
          farmerName: this.experiment.farmer,
          expName: this.experiment.name
        }
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
.description {
  padding-top: 5px;
  color: #999;
}
</style>
