<template>
  <div>
    <Title :title="farmer.name" :breadcrumbs="breadcrumbs" />
    <v-container class="constrained" style="padding-top: 0px;">
      <v-img
        class="white--text align-end"
        height="110px"
        :src="farmer.backgroundPhoto || defaultImageUrl"
      />

      <v-list-item style="margin: 10px 0 0 0;">
        <v-list-item-avatar color="grey">
          <v-img :src="farmer.profilePhoto"></v-img>
        </v-list-item-avatar>
        <v-list-item-content>
          <v-list-item-title>{{ farmer.name }}</v-list-item-title>
          <v-list-item-subtitle>GAEC Les Champs</v-list-item-subtitle>
        </v-list-item-content>
      </v-list-item>

      <div class="subtitle-2" style="margin-top: 20px;">Son histoire</div>
      <div class="body-2" style="margin-top: 5px;">{{ farmer.background }}</div>
      <div class="subtitle-2" style="margin-top: 20px;">Son exploitation</div>
      <div class="body-2 practice-description" style="margin-top: 5px;">{{ farmer.description }}</div>

      <div class="subtitle-2" style="margin-top: 20px;">Ses expérimentations</div>
      <v-row>
        <v-col v-for="(experiment, index) in farmer.tests" :key="index" cols="12" sm="6" md="4">
          <ExperimentCard :experiment="experiment" />
        </v-col>
      </v-row>
    </v-container>
  </div>
</template>

<script>
import ExperimentCard from "@/components/ExperimentCard"
import Title from "@/components/Title.vue"

export default {
  name: "Farmer",
  components: { Title, ExperimentCard },
  props: {
    farmer: {
      type: Object,
      required: true
    }
  },
  computed: {
    defaultImageUrl() {
      return this.$store.state.defaultPracticeImageUrl
    },
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
