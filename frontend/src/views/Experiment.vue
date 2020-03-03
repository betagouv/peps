<template>
  <div>
    <Title :title="experiment.title" :breadcrumbs="breadcrumbs" />
    <v-container class="constrained" style="padding-top: 0px;">
      <v-img
        class="white--text align-end"
        height="110px"
        :src="farmer.backgroundPhoto || defaultImageUrl"
      />

      <div class="display-1" style="margin-top: 20px;">{{ experiment.title }}</div>

      <v-list-item style="margin: 10px 0 0 0;">
        <v-list-item-avatar color="grey">
          <v-img :src="farmer.profilePhoto"></v-img>
        </v-list-item-avatar>
        <v-list-item-content>
          <v-list-item-title>{{ farmer.name }}</v-list-item-title>
          <v-list-item-subtitle>GAEC Les Champs</v-list-item-subtitle>
        </v-list-item-content>
      </v-list-item>

      <div class="subtitle-2" style="margin-top: 20px;">Description</div>
      <div class="body-2" style="margin-top: 5px;">{{ experiment.description }}</div>
      <div class="subtitle-2" style="margin-top: 20px;">Étapes</div>
      <div class="body-2 practice-description" style="margin-top: 5px;">
        <v-card class="pa-0 fill-height" style="margin-bottom: 5px;" outlined v-for="(step, index) in experiment.stages" :key="index">
          <v-card-title>{{ step.title }} ({{ step.schedule }})</v-card-title>
          <v-card-text>{{ step.description }}</v-card-text>
        </v-card>
      </div>
    </v-container>
  </div>
</template>

<script>
import Title from "@/components/Title.vue"

export default {
  name: "Experiment",
  components: { Title },
  props: {
    farmer: {
      type: Object,
      required: true
    },
    experiment: {
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
        },
        {
          text: this.farmer.name,
          disabled: false,
          href: "/#/agriculteur/" + this.farmer.name
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
