<template>
  <div>
    <div class="d-flex" style="margin-top: 30px; margin-bottom: 30px;">
      <router-link :to="{ name: 'Map' }">
        <v-img contain src="/static/images/france-regions.jpg" max-width="300"></v-img>
      </router-link>
      <div
        class="d-none d-sm-block"
        style="margin: 100px -10px 0 -70px; height: 3px; width: 250px; background-color: #CCC; transform: rotate(-20deg);"
      ></div>
      <v-card
        class="d-none d-sm-flex flex-container"
        style="overflow: hidden;"
        :max-width="$vuetify.breakpoint.name === 'sm' ? 300 : 400"
        max-height="300"
      >
        <v-list-item class="flex-fix-item" style="margin: 5px 0 0px 0;">
          <v-list-item-avatar size="40" color="grey" style="margin-right: 8px;">
            <v-img :src="featuredFarmer.profile_image" v-if="featuredFarmer.profile_image"></v-img>
            <v-icon v-else>mdi-account</v-icon>
          </v-list-item-avatar>
          <v-list-item-content>
            <v-list-item-title class="title" style="padding-left: 3px;">{{ featuredFarmer.name }}</v-list-item-title>

            <v-list-item-subtitle
              style="padding-left: 4px;"
              v-if="featuredFarmer.production && featuredFarmer.production.length > 0"
            >
              <span
                class="caption"
                style="margin-right: 4px;"
                v-for="(title, index) in (featuredFarmer.production || [])"
                :key="index"
              >{{ title }}</span>
            </v-list-item-subtitle>
          </v-list-item-content>
        </v-list-item>

        <v-card-text style="padding-top: 5px;" class="flex-shrink-item">
          {{featuredFarmer.description}}
          <div class="gradient"></div>
        </v-card-text>

        <v-card-actions class="flex-fix-item">
          <v-btn
            text
            small
            class="text-none text-decoration-underline"
            color="primary"
            @click="goToFarmer(featuredFarmer)"
          >Voir son profil</v-btn>
        </v-card-actions>
      </v-card>
    </div>
    <v-btn
      small
      outlined
      color="primary"
      :to="{name: 'Map'}"
      class="text-none"
    >Voir tous les agriculteurs sur une carte</v-btn>
  </div>
</template>

<script>
export default {
  name: "MapBlock",
  computed: {
    featuredFarmer() {
      const featured = this.$store.state.farmers.find(
        (x) => x.name === "Eric Bonnefoy"
      )
      if (featured) return featured
      return this.$store.state.farmers[
        Math.floor(Math.random() * this.$store.state.farmers.length)
      ]
    },
  },
  methods: {
    goToFarmer(farmer) {
      window.sendTrackingEvent("FarmerMapBlock", "seeProfile", farmer.name)
      this.$router.push({
        name: "Farmer",
        params: {
          farmerUrlComponent: this.$store.getters.farmerUrlComponent(farmer),
        },
      })
    },
  },
}
</script>

<style scoped>
.flex-container {
  display: flex;
  flex-direction: column;
  flex-wrap: nowrap;
}
.flex-shrink-item {
  flex: 0 1 auto;
  overflow: hidden;
  position: relative;
}
.flex-fix-item {
  flex: 0 0 auto;
}
.flex-shrink-item .gradient {
  position: absolute;
  background-image: linear-gradient(transparent, white);
  height: 40px;
  bottom: 0;
  left: 0;
  right: 0;
}
</style>
