<template>
  <v-card class="pa-5">
    <div
      class="display-1 primary--text"
    >{{ category.title }}</div>
    <v-divider class="ma-5" />

    <div class="title">Fonctionnement</div>
    <v-card-text>
      {{ category.description }}
    </v-card-text>
    <PracticeCards :practices="category.practices" />
  </v-card>
</template>

<script>
import PracticeCards from '@/components/grids/PracticeCards.vue'

export default {
  name: "Category",
  components: { PracticeCards },
  props: {
    category: {
      type: Object,
      required: true
    }
  }
}
</script>
