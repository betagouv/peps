<template>
  <v-container class="ma-0 pa-0">
    <v-row>
      <v-col v-for="(category, index) in categories" :key="index" cols="12" sm="6" md="4">
        <v-hover>
          <v-card
            class="pa-0 fill-height"
            outlined
            @click="goToCategory(category)"
            slot-scope="{ hover }"
            :elevation="hover ? 4 : 0"
          >
            <v-img class="white--text align-end" height="100px" :src="category.image" />
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
      const categoryId = category.id
      window.sendTrackingEvent("Landing", "category", category.title)
      this.$router.push({
        name: "Category",
        params: { categoryId: categoryId }
      })
    }
  }
}
</script>
