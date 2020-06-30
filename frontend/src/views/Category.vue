<template>
  <div>
    <Title :title="category.title" :breadcrumbs="breadcrumbs" />

    <v-container class="constrained">
      <div class="subtitle-2" v-if="category.description" style="margin-top: 10px; margin-bottom: 10px;">Fonctionnement</div>
      <div class="body-2" v-if="category.description" style="margin-top: 10px; margin-bottom: 20px;">{{ category.description }}</div>

      <PracticeCards :practices="category.practices" />
    </v-container>
  </div>
</template>

<script>
import PracticeCards from "@/components/grids/PracticeCards.vue"
import Title from "@/components/Title.vue"

export default {
  name: "Category",
  components: { PracticeCards, Title },
  props: {
    category: {
      type: Object,
      required: true
    }
  },
  computed: {
    breadcrumbs() {
      return [
        {
          text: "Accueil",
          disabled: false,
          to: { name: "Map" }
        },
        {
          text: this.category.title,
          disabled: true
        }
      ]
    }
  }
}
</script>
