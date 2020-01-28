<template>
  <div>
    <Title :title="practice.title" :breadcrumbs="breadcrumbs" />
    <v-container class="constrained" style="padding-top: 0px;">
      <v-img
        class="white--text align-end"
        height="110px"
        :src="practice.image || defaultImageUrl"
      />
      <InfoBox v-if="infoBoxItems.length > 0" :infoItems="infoBoxItems" style="margin-top: 10px; margin-bottom: 10px;" />
      <div>
        <v-btn
          class="text-none body-1 practice-buttons"
          color="primary"
          @click="tryPractice()"
          style="margin-bottom: 10px;"
          rounded
        >Cette pratique m'interesse</v-btn>
        <v-btn
          class="text-none body-1 practice-buttons"
          href="mailto:peps@beta.gouv.fr"
          target="_blank"
          rounded
          style="margin-bottom: 10px;"
        >Faire un retour</v-btn>
      </div>
      <v-divider />
      <div class="subtitle-2" style="margin-top: 20px;">Marge de manœuvre</div>
      <div class="body-2" style="margin-top: 20px;">{{ practice.mechanism.description }}</div>
      <div class="subtitle-2" style="margin-top: 20px;">Description de la pratique</div>
      <div class="body-2" style="margin-top: 20px;">{{ practice.description }}</div>
      <div class="subtitle-2" style="margin-top: 20px;">Ressources</div>
      <Resource
        v-for="resource in resources"
        :key="resource.id"
        :resource="resource"
      />
      <ImplementationOverlay
        :practice="implementationPractice"
        @done="implementationPractice = null"
      />
    </v-container>
  </div>
</template>

<script>
import InfoBox from "@/components/InfoBox.vue"
import Resource from "@/components/Resource.vue"
import ImplementationOverlay from "@/components/ImplementationOverlay"
import Title from "@/components/Title.vue"

export default {
  name: "PracticeView",
  components: { InfoBox, Resource, ImplementationOverlay, Title },
  data: () => {
    return {
      implementationPractice: null,
    }
  },
  props: {
    practice: {
      type: Object,
      required: true
    }
  },
  computed: {
    defaultImageUrl() {
      return this.$store.state.defaultPracticeImageUrl
    },
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
    },
    breadcrumbs() {
      const provenance = this.$router.previousRoute
      let breadcrumbs = [
        {
          text: "Accueil",
          disabled: false,
          href: "/#/"
        }
      ]
      if (provenance && provenance.name === 'Category') {
        breadcrumbs.push({
          text: provenance.params.categoryTitle,
          disabled: false,
          href: "/#" + provenance.path
        })
      } else if (provenance && provenance.name === 'Results') {
        breadcrumbs.push({
          text: 'Simulateur',
          disabled: false,
          href: "/#/formulaire"
        })
        breadcrumbs.push({
          text: 'Résultats',
          disabled: false,
          href: "/#/resultats"
        })
      }
      breadcrumbs.push({
        text: this.practice.title,
        disabled: true
      })
      return breadcrumbs
    }
  },
  methods: {
    tryPractice() {
      window.sendTrackingEvent("Practice", "try", this.practice.title)
      this.implementationPractice = this.practice
    }
  }
}
</script>

<style scoped>
.subtitle-2, .body-2 {
  line-height: 1.375rem;
}
</style>
