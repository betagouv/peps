<template>
  <v-row>
    <v-col v-for="item in items" :key="item.title" cols="12" sm="6">
      <v-card elevation="0" class="d-flex">

        <div class="pa-2" style="text-align: center; min-width: 30%;">
          <v-avatar :size="$vuetify.breakpoint.name != 'md' ? 60 : 90">
            <v-img :src="item.farmer.profile_image" v-if="item.farmer.profile_image"></v-img>
            <v-icon v-else>mdi-account</v-icon>
          </v-avatar>
          <div class="body-2 font-weight-bold" style="margin-top: 10px;">
            {{ item.farmer.name }}
          </div>
          <div v-if="item.farmer.production && item.farmer.production.length > 0" class="caption grey--text">
            {{ item.farmer.production[0] }}
          </div>
          <v-btn
            text
            small
            class="text-none text-decoration-underline"
            color="primary"
            @click="goToFarmer(item.farmer)"
          >Voir son profil</v-btn>
        </div>

        <div class="pa-2">
          <span>« </span>{{item.review}}<span> »</span>
        </div>

      </v-card>
    </v-col>
     <v-btn
      small
      outlined
      color="primary"
      href="/register"
      class="text-none"
      style="margin-left: 20px;"
    >Créer mon compte</v-btn>
  </v-row>
</template>

<script>
export default {
  name: "ReviewsBlock",
  computed: {
    items() {
      const items = [
        {
          farmer: this.farmerWithName('Alejandro Guillén'),
          review: "Ça faisait plusieurs fois que je pensais à mettre en place du traitement bas volumes, les retours des agriculteurs et le contact avec Eric m'ont décidé"
        },
        {
          farmer: this.farmerWithName('Eric Bonnefoy'),
          review: "Ça faisait plusieurs fois que je pensais à mettre en place du traitement bas volumes, les retours des agriculteurs et le contact avec Eric m'ont décidé"
        },
      ]
      return items.filter(x => !!x.farmer)
    },
  },
  methods: {
    farmerWithName(name) {
      const farmers = this.$store.state.farmers
      return farmers.find(x => x.name === name)
    },
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
