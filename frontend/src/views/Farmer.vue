<template>
  <div>
    <Title :title="farmer.name" :breadcrumbs="breadcrumbs" />
    <v-container class="constrained" style="padding-top: 0px;">
      <v-img
        class="white--text align-end"
        height="110px"
        :src="farmer.backgroundPhoto"
        style="background: #CCC;"
      />
      <FarmerListItem :farmer="farmer" />
      <v-divider style="margin-top: 10px;" />
      <div class="subtitle-2" style="margin-top: 20px;">Son exploitation</div>
      <div class="body-2 practice-description" style="margin-top: 5px;">{{ farmer.description }}</div>

      <div class="subtitle-2" style="margin-top: 20px;">Ses expérimentations</div>
      <v-row>
        <v-col v-for="(experiment, index) in farmer.experiments" :key="index" cols="12" sm="6" md="4">
          <ExperimentCard :experiment="experiment" />
        </v-col>
      </v-row>
    </v-container>
  </div>
</template>

<script>
import ExperimentCard from "@/components/ExperimentCard"
import FarmerListItem from "@/components/FarmerListItem"
import Title from "@/components/Title.vue"

export default {
  name: "Farmer",
  components: { Title, ExperimentCard, FarmerListItem },
  props: {
    farmer: {
      type: Object,
      required: true
    }
  },
  computed: {
    breadcrumbs() {
      return [
        {
          text: "Carte des expérimentations",
          disabled: false,
          href: "/#/map"
        }
      ]
    }
  }
}
</script>

<style scoped>
.subtitle-2,
.body-2 {
  line-height: 1.375rem;
}
</style>
