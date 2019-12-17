<template>
  <v-card>
    <v-img
      class="white--text align-end"
      height="110px"
      :src="practice.image_url || defaultImageUrl"
    />
    <v-card-title class="subtitle-2" style="margin-left: 3px;">{{ practice.mechanism.name }}</v-card-title>
    <v-card-subtitle class="display-1 primary--text">{{ practice.title }}</v-card-subtitle>
    <div style="margin-left: 10px;">
      <v-btn class="text-none body-1 practice-buttons" color="primary" @click="tryPractice()" style="margin-bottom: 10px;" rounded>Cette pratique m'interesse</v-btn>
      <v-btn class="text-none body-1 practice-buttons" href="mailto:peps@beta.gouv.fr" target="_blank" rounded style="margin-bottom: 10px;">Faire un retour</v-btn>
    </div>
    <v-divider class="ma-5" />
    <InfoBox v-if="infoBoxItems.length > 0" :infoItems="infoBoxItems" class="ma-5" />
    <div class="body-2 ma-5">{{ practice.description }}</div>
    <div class="subtitle-2" style="margin-left: 20px;">Ressources</div>
    <Resource
      v-for="resource in resources"
      :key="resource.id"
      :resource="resource"
      style="margin-left: 10px; margin-right: 10px;"
    />
    <ImplementationOverlay
      :practice="implementationPractice"
      @done="implementationPractice = null"
    />
  </v-card>
</template>

<script>
import InfoBox from "@/components/InfoBox.vue"
import Resource from "@/components/Resource.vue"
import ImplementationOverlay from "@/components/ImplementationOverlay"

export default {
  name: "PracticeView",
  components: { InfoBox, Resource, ImplementationOverlay },
  data: () => {
    return {
      implementationPractice: null,
      defaultImageUrl:
        "https://images.unsplash.com/photo-1502082553048-f009c37129b9?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=1350&q=80"
    }
  },
  props: {
    practice: {
      type: Object,
      required: true
    }
  },
  computed: {
    infoBoxItems() {
      let boxItems = []
      const boxItemsDescriptors = [
        {
          property: "equipment",
          title: "Matériel"
        },
        {
          property: "schedule",
          title: "Période de travail"
        },
        {
          property: "impact",
          title: "Impact"
        },
        {
          property: "additional_benefits",
          title: "Bénéfices supplémentaires"
        },
        {
          property: "success_factors",
          title: "Facteur clé de succès"
        }
      ]
      for (let i = 0; i < boxItemsDescriptors.length; i++) {
        if (this.practice[boxItemsDescriptors[i].property]) {
          boxItems.push({
            title: boxItemsDescriptors[i].title,
            text: this.practice[boxItemsDescriptors[i].property]
          })
        }
      }
      return boxItems
    },
    resources() {
      let resources = []
      if (this.practice.main_resource)
        resources.push(this.practice.main_resource)
      if (this.practice.secondary_resources)
        resources = resources.concat(this.practice.secondary_resources)
      return resources
    }
  },
  methods: {
    tryPractice() {
      window.sendTrackingEvent('Practice', 'try', this.practice.title)
      this.implementationPractice = this.practice
    }
  }
}
</script>
