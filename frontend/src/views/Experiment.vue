<template>
  <div>
    <div>
      <Title :title="experiment.name" :breadcrumbs="breadcrumbs" />
      <v-container class="constrained" style="padding-top: 10px;">
        <v-card style="margin-bottom: 20px" outlined shaped>
          <!-- <v-img
            class="white--text align-end"
            height="110px"
            :src="experiment.images && experiment.images.length > 0 ? experiment.images[0].image : ''"
            style="background: #CCC;"
          /> -->

          <div style="margin: 20px 20px 20px 20px;  " class="pa-0 d-flex">
            <div>
              <div class="title">
                <v-icon style="margin: -3px 5px 0 0">mdi-beaker-outline</v-icon>
                {{ experiment.name }}
              </div>
              <div style="margin-left: 35px;" class="caption">
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

        <div class="body-2" style="margin-bottom: 20px;">
          <v-avatar style="margin-right: 5px;" size="25" color="grey">
            <v-img :src="farmer.profile_image" v-if="farmer.profile_image"></v-img>
            <v-icon small v-else>mdi-account</v-icon>
          </v-avatar>Expérimentation faite par
          <a @click="goToFarmer(farmer)">{{farmer.name}}</a>
        </div>

        <div v-if="experiment.xp_type" class="caption info-item">
          <v-icon small left style="padding-bottom: 3px;">mdi-shape-outline</v-icon>
          {{experiment.xp_type}}
        </div>

        <div v-if="experiment.investment" class="caption info-item">
          <v-icon small left style="padding-bottom: 3px;">mdi-cash-multiple</v-icon>
          {{experiment.investment}}
        </div>

        <div v-if="experiment.surface || experiment.surface_type" class="caption info-item">
          <v-icon small left style="padding-bottom: 3px;">mdi-texture-box</v-icon>Surface :
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

        <div v-if="experiment.ongoing" class="caption info-item">
          <v-icon small left style="padding-bottom: 3px;">mdi-playlist-edit</v-icon>Expérimentation en cours
        </div>

        <div v-else class="caption info-item">
          <v-icon small left style="padding-bottom: 3px;">mdi-playlist-check</v-icon>Expérimentation finie
        </div>

        <div v-if="experiment.control_presence" class="caption info-item">
          <v-icon small left style="padding-bottom: 3px;">mdi-eye-outline</v-icon>Mise en place d'un témoin
        </div>

        <div v-else class="caption info-item">
          <v-icon small left style="padding-bottom: 3px;">mdi-eye-off-outline</v-icon>Pas de témoin mis en place
        </div>

        <div v-if="experiment.equipment" class="caption info-item">
          <v-icon small left style="padding-bottom: 3px;">mdi-hammer-wrench</v-icon>{{ experiment.equipment }} 
        </div>

        <div class="subtitle-2" style="margin-top: 20px;">Objectifs</div>
        <div class="body-2" style="margin-top: 5px;">{{ experiment.objectives }}</div>

        <div class="subtitle-2" v-if="experiment.description" style="margin-top: 20px;">Description</div>
        <div
          class="body-2"
          v-if="experiment.description"
          style="margin-top: 5px;"
        >{{ experiment.description }}</div>

        <div class="subtitle-2" v-if="experiment.results_details" style="margin-top: 20px;">Information sur les résultats</div>
        <div
          class="body-2"
          v-if="experiment.results_details"
          style="margin-top: 5px;"
        >{{ experiment.results_details }}</div>

        <div class="subtitle-2" v-if="experiment.links && experiment.links.length > 0" style="margin-top: 20px;">Links</div>
        <ul v-if="experiment.links && experiment.links.length > 0">
          <li
            class="body-2"
            
            v-for="(link, index) in experiment.links"
            :key="index"
            style="margin-top: 5px;"
          ><a href="link">{{ link }}</a></li>
        </ul>
        <div
          class="subtitle-2"
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
      </v-container>
    </div>
  </div>
</template>

<script>
import Title from "@/components/Title.vue"

export default {
  name: "Experiment",
  components: { Title },
  data() {
    return {
      testImages: [
        "https://images.unsplash.com/12/green.jpg?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=1350&q=80",
        "https://images.unsplash.com/40/yIdlmSvfSZCyGkCkLt0P_lucaslof_2.jpg?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjExMDk0fQ&auto=format&fit=crop&w=500&q=60",
        "https://images.unsplash.com/photo-1464972377689-e7674c48d806?ixlib=rb-1.2.1&auto=format&fit=crop&w=500&q=60",
        "https://images.unsplash.com/photo-1436462020942-723a9ea097c7?ixlib=rb-1.2.1&auto=format&fit=crop&w=500&q=60"
      ]
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
      this.$router.push({
        name: "Farmer",
        params: { farmerName: farmer.name }
      })
    },
  },
  computed: {
    farmer() {
      return this.$store.getters.farmerWithName(this.farmerName)
    },
    experiment() {
      if (!this.farmer)
        return
      return this.farmer.experiments.find(x => x.name === this.experimentName)
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
        }
      ]
    }
  }
}
</script>

<style scoped>
.subtitle-2,
.body-2 {
  line-height: 1.375rem;
}

.capitalize {
  text-transform: capitalize;
}

.info-item {
  margin-top: 5px;
}
</style>
