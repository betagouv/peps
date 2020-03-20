<template>
  <v-card class="flex-container">
    <!-- <v-img
      class="flex-fix-item"
      :src="farmer.backgroundPhoto"
      height="100px"
      style="background: #CCC;"
    ></v-img>-->
    <v-list-item class="flex-fix-item" style="margin: 10px 0 0 0;">
      <v-list-item-avatar color="grey">
        <v-img :src="farmer.profile_image" v-if="farmer.profile_image"></v-img>
        <v-icon v-else>mdi-account</v-icon>
      </v-list-item-avatar>
      <v-list-item-content>
        <v-list-item-title>
          <img
            src="/static/images/marker-icon-2x-red.png"
            height="18px"
            style="display:inline-block; margin-bottom: -3px; margin-right: 2px;"
          />
          {{ farmer.name }}
        </v-list-item-title>
        <v-list-item-subtitle>
          <span v-for="(title, index) in (farmer.profession || [])" :key="index">
            {{ title }}
            <span
              v-if="farmer.profession.length > 1 && index < farmer.profession.length - 1"
            >,</span>
          </span>
        </v-list-item-subtitle>
      </v-list-item-content>
    </v-list-item>
    <v-card-text class="flex-fix-item">
      <v-btn
        block
        class="text-none"
        color="primary"
        max-width="50"
        @click="goToFarmer(farmer)"
      >Voir le profil</v-btn>
    </v-card-text>
    <v-card-subtitle
      v-if="farmer.experiments && farmer.experiments.length > 0"
      class="subtitle-2 flex-fix-item"
      style="padding: 4px 16px 0px 16px;"
    >Expérimentations</v-card-subtitle>
    <v-card-text class="flex-fix-item" v-if="farmer.experiments && farmer.experiments.length > 0">
      <ul>
        <li v-for="(item, index) in farmer.experiments" :key="index">
          <a @click="goToExperiment(farmer, item)">{{ item.name }}</a>
        </li>
      </ul>
    </v-card-text>
    <v-card-subtitle
      class="subtitle-2 flex-fix-item"
      style="padding: 0px 16px 0px 16px;"
    >Son exploitation</v-card-subtitle>
    <v-card-text class="description flex-shrink-item" style="margin-bottom: 20px;">
      {{ farmer.description }}
      <div class="gradient" v-if="showDescriptionGradient"></div>
    </v-card-text>
  </v-card>
</template>

<script>
export default {
  name: "FarmerCard",
  props: {
    farmer: {
      type: Object,
      required: true
    }
  },
  data() {
    return {
      showDescriptionGradient: false
    }
  },
  methods: {
    goToFarmer(farmer) {
      this.$router.push({
        name: "Farmer",
        params: { farmerName: farmer.name }
      })
    },
    goToExperiment(farmer, experiment) {
      this.$router.push({
        name: "Experiment",
        params: {
          farmerName: farmer.name,
          expName: experiment.name
        }
      })
    },
    adjustHeight() {
      if (this.$el) {
        const domElement = this.$el.querySelector(".description")
        this.showDescriptionGradient =
          domElement.scrollHeight > domElement.offsetHeight
      }
    }
  },
  updated() {
    this.adjustHeight()
  },
  mounted() {
    this.adjustHeight()
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