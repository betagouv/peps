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
        <v-row>
          <v-col cols="12" md="9">
            <v-card style="margin-bottom: 20px" outlined shaped>
              <div style="margin: 20px 15px 20px 15px;" class="pa-0 d-flex">
                <div>
                  <div style="float: left; margin-top: 3px;">
                    <v-icon>mdi-beaker-outline</v-icon>
                  </div>
                  <div style="margin-left: 35px;" class="body-2">
                    <div class="headline" style="margin-bottom: 10px;">{{ experiment.name }}</div>
                    <v-icon
                      style="margin-right: 3px;"
                      v-if="experiment.results === 'XP qui fonctionne, elle est intégrée à l\'exploitation'"
                      color="primary"
                    >mdi-check-decagram</v-icon>
                    {{experiment.results}}
                  </div>
                  <div style="margin-left: 35px; margin-top: 10px;">
                    <v-btn
                      class="text-none d-none d-md-flex"
                      @click="onContactClick"
                      color="primary"
                      :small="isMobile"
                    >Contacter {{ farmer.name }}</v-btn>
                  </div>
                </div>
              </div>
            </v-card>

            <div
              class="d-flex d-md-none"
              style="margin-bottom: 20px; margin-left: 15px; margin-top: 0px;"
            >
              <MiniMap
                style="padding-top: 15px; width: 120px; margin-right: 20px;"
                :size="100"
                class="d-none d-sm-flex"
                :lat="farmer.lat"
                :lon="farmer.lon"
              />

              <v-avatar
                style="margin-right: 10px; float: left; margin-top: 0px;"
                size="35"
                color="grey"
              >
                <v-img :src="farmer.profile_image" v-if="farmer.profile_image"></v-img>
                <v-icon small v-else>mdi-account</v-icon>
              </v-avatar>

              <div class="subtitle-1" style="margin-bottom: 0px;">
                Retour d'expérience par {{ farmer.name }}
                <span
                  v-if="farmer.postal_code"
                  style="margin-top: 5px;"
                  class="body-2"
                >
                  (
                  <v-icon small style="padding-bottom: 3px;">mdi-map-marker</v-icon>
                  {{ farmer.postal_code }})
                </span>
                <v-btn
                  block
                  class="text-none"
                  style="margin-bottom: 10px; margin-top: 5px;"
                  @click="onContactClick"
                  color="primary"
                >Contacter {{ farmer.name }}</v-btn>

                <v-btn
                  block
                  class="text-none"
                  color="primary"
                  outlined
                  @click="goToFarmer()"
                >Voir son profil</v-btn>
              </div>
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
                >{{experiment.surface_type.join ? experiment.surface_type.join(', ') : experiment.surface_type}}</span>
                <span
                  v-else
                  style="text-transform: lowercase;"
                >{{experiment.surface}} ({{experiment.surface_type.join ? experiment.surface_type.join(', ') : experiment.surface_type}})</span>
              </div>
            </div>

            <div v-if="experiment.ongoing" class="body-2 info-item">
              <v-icon small left>mdi-playlist-edit</v-icon>
              <div>Expérience en cours</div>
            </div>

            <div v-else class="body-2 info-item">
              <v-icon small left>mdi-playlist-check</v-icon>
              <div>Expérience finie</div>
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
            <div
              class="body-1"
              style="margin-top: 5px; white-space: pre-wrap;"
            >{{ experiment.objectives }}</div>

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
            <ImageGallery
              v-if="experiment.images && experiment.images.length > 0"
              :images="experiment.images"
            />

            <div
              class="title"
              v-if="experiment.videos && experiment.videos.length > 0"
              style="margin-top: 20px;"
            >Vidéos</div>
            <VideoGallery
              v-if="experiment.videos && experiment.videos.length > 0"
              :videos="experiment.videos"
            />

            <div class="body-1" style="margin-top: 30px;">
              Pour plus d'informations sur cette expérience :
              <v-btn
                class="text-none"
                @click="onContactClick"
                style="margin-top: -2px;"
                color="primary"
              >Contacter {{ farmer.name }}</v-btn>
            </div>
          </v-col>
          <v-col style="padding-left: 0; padding-right: 0;" cols="12" md="3">
            <FarmerCard
              class="d-none d-sm-none d-md-flex"
              :showMiniMap="true"
              :ctaSecondary="true"
              :avatarSize="30"
              :compact="true"
              :farmer="farmer"
            />
          </v-col>
        </v-row>
      </v-container>
    </div>
  </div>
</template>

<script>
import Title from "@/components/Title.vue"
import NotFound from "@/components/NotFound.vue"
import FarmerContactOverlay from "@/components/FarmerContactOverlay.vue"
import FarmerCard from "@/components/FarmerCard.vue"
import ImageGallery from "@/components/ImageGallery.vue"
import VideoGallery from "@/components/VideoGallery.vue"
import MiniMap from "@/components/MiniMap.vue"

export default {
  name: "Experiment",
  metaInfo() {
    const titleMaxLength = 70
    const descriptionMaxLength = 150
    let title = this.experiment ? this.experiment.name : "Retour d'expérience"
    if (title.length >= titleMaxLength) {
      title = title.substring(0, titleMaxLength - 1) + "…"
    }
    let tags =
      this.experiment && this.experiment.tags
        ? "Thèmes : " + this.experiment.tags.join(", ") + ". "
        : ""
    let descriptionLength = descriptionMaxLength - tags.length
    let description =
      this.experiment && this.experiment.description
        ? this.experiment.description.substring(0, descriptionLength - 1) + "…"
        : ""
    return {
      title: title,
      meta: [{ description: `${tags} ${description}` }]
    }
  },
  components: {
    Title,
    NotFound,
    FarmerContactOverlay,
    FarmerCard,
    ImageGallery,
    VideoGallery,
    MiniMap
  },
  data() {
    return {
      contactOverlayVisible: false
    }
  },
  props: {
    farmerUrlComponent: {
      type: String,
      required: true
    },
    experimentUrlComponent: {
      type: String,
      required: true
    }
  },
  methods: {
    goToFarmer() {
      window.sendTrackingEvent(this.$route.name, "seeFarmer", this.farmer.name)
      this.$router.push({
        name: "Farmer",
        params: { farmerUrlComponent: this.farmerUrlComponent }
      })
    },
    onContactClick() {
      if (this.$store.state.loggedUser && this.$store.state.loggedUser.farmer_id) {
        this.$router.push({
          name: "Messages",
          params: {
            farmerUrlComponent: this.farmerUrlComponent
          }
        })
        
      } else {
        window.sendTrackingEvent(
          this.$route.name,
          "contact",
          this.farmerUrlComponent
        )
        this.contactOverlayVisible = true
      }
    }
  },
  computed: {
    farmer() {
      return this.$store.getters.farmerWithUrlComponent(this.farmerUrlComponent)
    },
    isMobile() {
      return this.$vuetify.breakpoint.name === "xs"
    },
    experiment() {
      if (!this.farmer) return
      return this.$store.getters.experimentWithUrlComponent(
        this.farmer,
        this.experimentUrlComponent
      )
    },
    experimentNotFound() {
      return this.$store.getters.experiments.length > 0 && !this.experiment
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
          text: "Accueil",
          disabled: false,
          to: { name: "Map" }
        },
        {
          text: this.farmer.name,
          disabled: false,
          to: {
            name: "Farmer",
            params: {
              farmerUrlComponent: this.$store.getters.farmerUrlComponent(
                this.farmer
              )
            }
          }
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
