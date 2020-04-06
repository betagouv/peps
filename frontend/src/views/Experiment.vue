<template>
  <div>
    <FarmerContactOverlay
      v-if="!!farmer"
      :farmer="farmer"
      :visible="contactOverlayVisible"
      @done="contactOverlayVisible = false"
    />

    <NotFound v-if="experimentNotFound" style="padding-top: 40px; padding-bottom: 50px;" />

    <div v-else-if="experiment">
      <Title :breadcrumbs="breadcrumbs" />
      <v-container class="constrained" style="padding-top: 10px;">
        <v-card style="margin-bottom: 20px" outlined shaped>
          <!-- <v-img
            class="white--text align-end"
            height="110px"
            :src="experiment.images && experiment.images.length > 0 ? experiment.images[0].image : ''"
            style="background: #CCC;"
          />-->

          <div style="margin: 20px 20px 20px 20px;  " class="pa-0 d-flex">
            <div>
              <div class="headline" style="margin: 0px 0px 5px 0">
                <v-icon style="margin: 0px 5px 0 0">mdi-beaker-outline</v-icon>
                {{ experiment.name }}
              </div>
              <div style="margin-left: 35px;" class="body-2">
                <v-icon
                  style="margin-right: 3px;"
                  v-if="experiment.results === 'XP qui fonctionne, elle est intégrée à l\'exploitation'"
                  color="primary"
                >mdi-check-decagram</v-icon>
                {{experiment.results}}
              </div>
            </div>
          </div>
        </v-card>

        <div class="body-1">
          <v-avatar style="margin-right: 10px;" size="35" color="grey">
            <v-img :src="farmer.profile_image" v-if="farmer.profile_image"></v-img>
            <v-icon small v-else>mdi-account</v-icon>
          </v-avatar>Expérimentation faite par
          <a @click="goToFarmer(farmer)">{{farmer.name}}</a>
        </div>
        <div style="margin-bottom: 20px; margin-left: 45px; margin-top: 0px;">
          <v-btn
            class="text-none"
            @click="onContactClick"
            color="primary"
          >Contacter {{ farmer.name }}</v-btn>
        </div>

        <div v-if="experiment.xp_type" class="body-2 info-item">
          <v-icon small left>mdi-shape-outline</v-icon>
          <div>{{experiment.xp_type}}</div>
        </div>

        <div v-if="experiment.investment" class="body-2 info-item">
          <v-icon small left>mdi-cash-multiple</v-icon>
          <div>{{experiment.investment}}</div>
        </div>

        <div v-if="experiment.surface || experiment.surface_type" class="body-2 info-item">
          <v-icon small left>mdi-texture-box</v-icon>
          <div>
            Surface :
            <span
              v-if="experiment.surface && !experiment.surface_type"
            >{{experiment.surface}}</span>
            <span
              v-else-if="!experiment.surface && experiment.surface_type"
            >{{experiment.surface_type}}</span>
            <span
              v-else
              style="text-transform: lowercase;"
            >{{experiment.surface}} ({{experiment.surface_type}})</span>
          </div>
        </div>

        <div v-if="experiment.ongoing" class="body-2 info-item">
          <v-icon small left>mdi-playlist-edit</v-icon>
          <div>Expérimentation en cours</div>
        </div>

        <div v-else class="body-2 info-item">
          <v-icon small left>mdi-playlist-check</v-icon>
          <div>Expérimentation finie</div>
        </div>

        <div v-if="experiment.control_presence" class="body-2 info-item">
          <v-icon small left>mdi-eye-outline</v-icon>
          <div>Mise en place d'un témoin</div>
        </div>

        <div v-else class="body-2 info-item">
          <v-icon small left>mdi-eye-off-outline</v-icon>
          <div>Pas de témoin mis en place</div>
        </div>

        <div v-if="experiment.equipment" class="body-2 info-item">
          <v-icon small left>mdi-hammer-wrench</v-icon>
          <div>{{ experiment.equipment }}</div>
        </div>

        <div class="title" style="margin-top: 20px;">Objectifs</div>
        <div class="body-1" style="margin-top: 5px; white-space: pre-wrap;">{{ experiment.objectives }}</div>

        <p class="title" v-if="experiment.description" style="margin-top: 20px;">Description</p>
        <div
          class="body-1"
          v-if="experiment.description"
          style="margin-top: 5px; white-space: pre-wrap;"
        >{{ experiment.description }}</div>

        <div
          class="title"
          v-if="experiment.results_details"
          style="margin-top: 20px;"
        >Information sur les résultats</div>
        <div
          class="body-1"
          v-if="experiment.results_details"
          style="margin-top: 5px; white-space: pre-wrap;"
        >{{ experiment.results_details }}</div>

        <div
          class="title"
          v-if="experiment.links && experiment.links.length > 0"
          style="margin-top: 20px;"
        >Liens</div>
        <ul v-if="experiment.links && experiment.links.length > 0">
          <li
            class="body-1"
            v-for="(link, index) in experiment.links"
            :key="index"
            style="margin-top: 5px;"
          >
            <a :href="link" target="_blank">{{ link }}</a>
          </li>
        </ul>
        <div
          class="title"
          v-if="experiment.images && experiment.images.length > 0"
          style="margin-top: 20px;"
        >Images</div>
        <v-row v-if="experiment.images && experiment.images.length > 0">
          <v-col
            v-for="(photo, index) in experiment.images.map(x => x.image)"
            :key="index"
            class="d-flex child-flex"
            cols="6"
            sm="3"
          >
            <v-card flat class="d-flex">
              <v-img :src="photo" aspect-ratio="1" class="grey lighten-2"></v-img>
            </v-card>
          </v-col>
        </v-row>

        <div
          class="title"
          v-if="experiment.videos && experiment.videos.length > 0"
          style="margin-top: 20px;"
        >Vidéos</div>
        <v-row v-if="experiment.videos && experiment.videos.length > 0">
          <v-col
            v-for="(video, index) in experiment.videos.map(x => x.video)"
            :key="index"
            class="d-flex child-flex"
            cols="12"
            sm="6"
          >
            <v-card flat class="d-flex" height=250>
              <video style="height: 100%; width: 100%; background: #333;" controls>
                <source type="video/mp4" :src="video" />Votre navigateur ne peut pas afficher des vidéos.
              </video>
            </v-card>
          </v-col>
        </v-row>

        <div class="body-1" style="margin-top: 30px;">
          Pour plus d'informations sur cette expérimentation : 
          <v-btn
            class="text-none"
            @click="onContactClick"
            style="margin-top: -2px;"
            color="primary"
          >Contacter {{ farmer.name }}</v-btn>
        </div>
      </v-container>
    </div>
  </div>
</template>

<script>
import Title from "@/components/Title.vue"
import NotFound from "@/components/NotFound.vue"
import FarmerContactOverlay from "@/components/FarmerContactOverlay.vue"

export default {
  name: "Experiment",
  components: { Title, NotFound, FarmerContactOverlay },
  data() {
    return {
      testImages: [
        "https://images.unsplash.com/12/green.jpg?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=1350&q=80",
        "https://images.unsplash.com/40/yIdlmSvfSZCyGkCkLt0P_lucaslof_2.jpg?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjExMDk0fQ&auto=format&fit=crop&w=500&q=60",
        "https://images.unsplash.com/photo-1464972377689-e7674c48d806?ixlib=rb-1.2.1&auto=format&fit=crop&w=500&q=60",
        "https://images.unsplash.com/photo-1436462020942-723a9ea097c7?ixlib=rb-1.2.1&auto=format&fit=crop&w=500&q=60"
      ],
      contactOverlayVisible: false
    }
  },
  props: {
    farmerName: {
      type: String,
      required: true
    },
    experimentName: {
      type: String,
      required: true
    }
  },
  methods: {
    goToFarmer(farmer) {
      window.sendTrackingEvent(this.$route.name, "seeFarmer", this.farmer.name)
      this.$router.push({
        name: "Farmer",
        params: { farmerName: farmer.name }
      })
    },
    onContactClick() {
      window.sendTrackingEvent(this.$route.name, "contact", this.farmerName)
      this.contactOverlayVisible = true
    }
  },
  computed: {
    farmer() {
      return this.$store.getters.farmerWithName(this.farmerName)
    },
    experiment() {
      if (!this.farmer) return
      return this.farmer.experiments.find(x => x.name === this.experimentName)
    },
    experimentNotFound() {
      return this.$store.state.experiments.length > 0 && !this.experiment
    },
    icons() {
      const icons = {
        adventices: "mdi-sprout",
        insectes: "mdi-ladybug",
        maladies: "mdi-bottle-tonic-plus",
        productivite: "mdi-chart-bell-curve-cumulative",
        biodiversite: "mdi-bee",
        sol: "mdi-image-filter-hdr",
        fourrages: "mdi-cow",
        "nouvelles-cultures": "mdi-corn",
        oad: "mdi-cellphone-information"
      }
      if (!this.experiment.tags) return []
      return this.experiment.tags
        .map(x =>
          x in icons ? { icon: icons[x], text: x.replace("-", " ") } : null
        )
        .filter(x => x != null)
    },
    breadcrumbs() {
      return [
        {
          text: "Carte des expérimentations",
          disabled: false,
          href: "/#/map"
        },
        {
          text: this.farmer.name,
          disabled: false,
          href: "/#/agriculteur/" + this.farmer.name
        },
        {
          text: this.experiment.name,
          disabled: true
        }
      ]
    }
  }
}
</script>

<style scoped>
.capitalize {
  text-transform: capitalize;
}

.info-item {
  margin-top: 10px;
}

.info-item > div {
  margin-left: 30px;
}

.info-item > i {
  float: left;
  padding-top: 3px;
}
</style>
