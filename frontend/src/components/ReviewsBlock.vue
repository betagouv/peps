<template>
  <div>
    <v-row>
      <v-col v-for="item in items" :key="item.title" cols="12" sm="6">
        <v-card elevation="0" class="d-flex secondary--text">
          <div class="pa-2" style="text-align: center; min-width: 30%;">
            <v-avatar :size="$vuetify.breakpoint.name != 'md' ? 60 : 90">
              <v-img :src="item.farmer.profile_image" v-if="item.farmer.profile_image"></v-img>
              <v-icon v-else>mdi-account</v-icon>
            </v-avatar>
            <div class="body-2 font-weight-bold" style="margin-top: 10px;">{{ item.farmer.name }}</div>
            <div
              v-if="item.farmer.production"
              class="caption grey--text"
            >{{ item.farmer.production }}</div>
            <v-btn
              text
              small
              class="text-none text-decoration-underline"
              color="primary"
              @click="goToFarmer(item.farmer)"
            >Voir son profil</v-btn>
          </div>

          <div class="pa-2 body-1">
            <span>«</span>
            {{item.review}}
            <span>»</span>
          </div>
        </v-card>
      </v-col>
    </v-row>
    <v-btn
      outlined
      color="primary"
      href="/register"
      class="text-none"
      v-if="!loggedUser"
    >Créer mon compte</v-btn>
  </div>
</template>

<script>
export default {
  name: "ReviewsBlock",
  data: () => {
    return {
      items: [{
        farmer: {
          profile_image: 'https://cellar-c2.services.clever-cloud.com/peps-prod/media/attZe1vXrlvrHX0sl.jpg',
          name: 'Thierry Desvaux',
          production: 'Grandes cultures',
          urlSlug: 'sep de bord--83'
        },
        review: "Génial, enfin un site pour partager nos expériences et surtout échanger avec des agriculteurs qui innovent.",
      }]
    }
  },
  computed: {
    loggedUser() {
      return this.$store.state.loggedUser
    }
  },
  methods: {
    farmerWithName(name) {
      const farmers = this.$store.state.farmers
      return farmers.find((x) => x.name === name)
    },
    goToFarmer(farmer) {
      window.sendTrackingEvent("FarmerMapBlock", "seeProfile", farmer.name)
      this.$router.push({
        name: "Farmer",
        params: {
          farmerUrlComponent: farmer.urlSlug,
        },
      })
    },
  },
}
</script>
