<template>
  <v-card>
    <div class="primary white--text practice-header">
        <div
          class="caption"
          v-if="practice.mechanism && practice.mechanism.name"
        >{{ practice.mechanism.name }}</div>
        <div class="subtitle-1 practice-title ma-0 font-weight-bold">{{ practice.title }}</div>
      </div>
    <v-container>
      
      <InfoBox v-if="infoBoxItems.length > 0" :infoItems="infoBoxItems" />
      <div class="body-2 practice-description">{{ practice.description }}</div>
      <div v-if="resources.length > 0">
        <div class="subtitle-2">Ressources</div>
        <Resource
          v-for="resource in resources"
          :key="resource.id"
          :resource="resource"
          style="margin-top: 10px; margin-bottom: 10px;"
        />
      </div>
      <div style="padding-right: 10px; text-align: right">
        <v-btn class="text-none body-1 practice-buttons" @click="blacklistPractice()" rounded>🚫 Recalculer sans cette pratique</v-btn>
        <v-btn class="text-none body-1 practice-buttons" @click="tryPractice()" rounded>👍 Cette pratique m'interesse</v-btn>
      </div>
    </v-container>
  </v-card>
</template>

<script>
import Resource from "@/components/Resource.vue"
import InfoBox from "@/components/InfoBox.vue"

export default {
  name: "Practice",
  components: { Resource, InfoBox },
  props: {
    practice: {
      type: Object,
      required: true
    },
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
    blacklistPractice() {
      window.sendTrackingEvent('Practice', 'blacklist', this.practice.title)
      this.$emit('blacklist', this.practice)
    },
    tryPractice() {
      window.sendTrackingEvent('Practice', 'try', this.practice.title)
      this.$emit('implement', this.practice)
    }
  }
}
</script>

<style>
.practice-header {
  padding: 10px 15px 10px 15px;
}
.practice-description {
  margin-top: 15px;
  margin-bottom: 15px;
}
.practice-buttons {
  margin-left: 10px;
  margin-top: 10px;
  margin-bottom: 10px;
}
</style>
