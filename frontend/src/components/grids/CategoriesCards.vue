<template>
  <v-container class="constrained ma-0 pa-0">
    <v-row>
      <v-col v-for="(category, index) in categories" :key="index" cols="12" sm="6" md="4">
        <v-hover>
          <v-card
            class="pa-0 fill-height"
            outlined
            @click="goToCategory(category)"
            slot-scope="{ hover }"
            :elevation="hover ? 4 : 1"
          >
            <v-img class="white--text align-end" height="120px" :src="category.image" />
            <v-card-text>{{ category.title }}</v-card-text>
          </v-card>
        </v-hover>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
export default {
  name: "CategoriesCards",
  components: {},
  computed: {
    categories() {
      return this.$store.state.categories
    }
  },
  methods: {
    goToCategory(category) {
      window.sendTrackingEvent(this.$route.name, "category", category.title)
      this.$router.push({
        name: "Category",
        params: { categoryTitle: category.title }
      })
    }
  }
}
</script>
