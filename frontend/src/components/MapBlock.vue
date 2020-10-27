<template>
  <div>
    <div class="d-flex" style="margin-top: 30px; margin-bottom: 30px;">
      <router-link :to="{ name: 'Map' }">
        <v-img contain src="/static/images/france-regions.jpg" max-width="300"></v-img>
      </router-link>

      <v-card
        class="d-none d-sm-flex flex-container"
        style="overflow: hidden; margin-left: 90px;"
        :max-width="$vuetify.breakpoint.name === 'sm' ? 300 : 400"
        max-height="300"
        v-if="featuredFarmer"
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
              v-if="featuredFarmer.production"
            >
              <span
                class="caption"
                style="margin-right: 4px;"
              >{{ featuredFarmer.production }}</span>
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
  data: () => ({
    featuredFarmer: {
      profile_image: "https://cellar-c2.services.clever-cloud.com/peps-prod/media/attjuMglgRBPmfdIX.jpg",
      name: "Eric Bonnefoy",
      production: "Grandes cultures",
      description: " Je me suis installé en GAEC avec mes parents sur l'exploitation familiale de polyculture élevage laitier montbéliardes. Nous avons toujours fait des céréales, en particulier du blé panifiable, on travaillait avec un meunier. Au départ à la retraite de mes parents, je me suis mis en GAEC avec mon frère, ma belle soeur et mon épouse. Il y a 7 ans, on a séparé l'exploitation en 2, mon frère a gardé le troupeau laitier et un peu de céréales et moi uniquement des céréales. Je suis aujourd'hui en SARL avec mon épouse (SARL Bonnefoy). Je travaille pour Lu, avec une biscuiterie à côté de Besançon. Je suis la charte Lu Harmony, j'ai 7ha de plantes mellifères, je travaille avec un apiculteur, j'ai un stockage à la ferme sans insecticide. Pour moi ces démarches de vente en local et de biodiversité sont importantes. Je suis engagé dans plusieurs réseaux : Arvalis CRC, le groupe des producteurs Lu de la région et je suis ambassadeur Passion Céréales en région.",
      url_slug: "SARL Bonnefoy--19",
    }
  }),
  methods: {
    goToFarmer(farmer) {
      window.sendTrackingEvent("FarmerMapBlock", "seeProfile", farmer.name)
      this.$router.push({
        name: "Farmer",
        params: {
          farmerUrlComponent: this.featuredFarmer.url_slug,
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
