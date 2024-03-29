<template>
  <div>
    <FarmerContactOverlay
      v-if="!!farmer && farmer"
      :farmer="farmer"
      :visible="contactOverlayVisible"
      @done="contactOverlayVisible = false"
    />

    <NotFound v-if="farmerNotFound" style="padding-top: 40px; padding-bottom: 50px;" />

    <div v-else-if="farmer">
      <Title :breadcrumbs="breadcrumbs" />
      <v-container class="constrained" style="padding-top: 10px;">
        <v-card style="margin-bottom: 20px" outlined shaped>
          <div style="margin: 20px 15px 20px 15px;  " class="pa-0 d-flex">
            <v-avatar :size="isMobile ? 35 : 100" color="grey">
              <v-img :src="farmer.profile_image" v-if="farmer.profile_image"></v-img>
              <v-icon v-else :large="!isMobile" :small="isMobile">mdi-account</v-icon>
            </v-avatar>
            <div style="padding-left: 15px;">
              <div class="headline">
                {{ farmer.name }}
                <span class="d-block d-sm-inline">
                  <v-chip
                    small
                    class
                    style="margin-top:-4px; margin-right: 10px;"
                    v-for="(title, index) in (farmer.production || [])"
                    :key="index"
                  >{{ title }}</v-chip>
                </span>
              </div>
              <div v-if="farmer.postal_code" style="margin-top: 5px;" class="body-2">
                <v-icon small style="padding-bottom: 3px;">mdi-map-marker</v-icon>
                {{ farmer.postal_code }}
              </div>
              <div>
                <v-btn
                  v-if="farmer.contact_possible"
                  class="text-none"
                  style="margin-top: 10px"
                  outlined
                  :small="isMobile"
                  color="primary"
                  @click="onContactClick"
                >
                  Discuter avec {{ farmer.name }}
                  <v-icon small style="margin-left: 5px;">mdi-message</v-icon>
                </v-btn>
              </div>
              <div v-if="farmer.links && farmer.links.length > 0" style="margin-top: 10px">
                <v-btn
                  v-for="(link, index) in farmer.links"
                  :key="index"
                  class="text-none"
                  style="margin-right: 10px"
                  icon
                  outlined
                  :color="getLinkColor(link)"
                  :href="link"
                  target="_blank"
                >
                  <v-icon>{{ getLinkIcon(link) }}</v-icon>
                </v-btn>
              </div>
            </div>
          </div>
        </v-card>

        <div
          class="title"
          style="margin-top: 20px;"
          v-if="approvedExperiments && approvedExperiments.length === 1"
        >Son retour d'expérience</div>
        <div
          class="title"
          style="margin-top: 20px;"
          v-if="approvedExperiments && approvedExperiments.length > 1"
        >Ses retours d'expérience</div>
        <v-row v-if="approvedExperiments && approvedExperiments.length > 0">
          <v-col
            v-for="(experiment, index) in approvedExperiments"
            :key="index"
            cols="12"
            sm="6"
            md="4"
          >
            <ExperimentCard :experiment="experiment" />
          </v-col>
        </v-row>

        <div class="title" style="margin-top: 20px;">Son exploitation</div>

        <FarmerInfoBox v-if="farmer" :farmer="farmer" />

        <div
          class="body-1"
          style="margin-top: 20px; white-space: pre-wrap;"
        >{{ farmer.description }}</div>

        <div class="title" style="margin-top: 20px;" v-if="farmer.specificities">Spécifités</div>
        <div
          class="body-1"
          style="margin-top: 5px; white-space: pre-wrap;"
          v-if="farmer.specificities"
        >{{ farmer.specificities }}</div>

        <div class="title" style="margin-top: 20px;" v-if="farmer.text_links">Liens</div>
        <div
          class="body-1"
          style="margin-top: 5px;"
          v-if="farmer.specificities"
        >{{ farmer.text_links }}</div>

        <div
          class="title"
          v-if="farmer.images && farmer.images.length > 0"
          style="margin-top: 20px;"
        >Images</div>
        <ImageGallery v-if="farmer.images && farmer.images.length > 0" :images="farmer.images" />
      </v-container>
    </div>
  </div>
</template>

<script>
import Vue from 'vue'
import ExperimentCard from "@/components/ExperimentCard"
import Title from "@/components/Title.vue"
import NotFound from "@/components/NotFound.vue"
import FarmerContactOverlay from "@/components/FarmerContactOverlay.vue"
import FarmerInfoBox from "@/components/FarmerInfoBox"
import Constants from "@/constants"
import ImageGallery from "@/components/ImageGallery.vue"
import utils from "@/utils"

export default {
  name: "Farmer",
  components: {
    Title,
    ExperimentCard,
    FarmerContactOverlay,
    NotFound,
    FarmerInfoBox,
    ImageGallery
  },
  metaInfo() {
    if (!this.farmer) return {}

    let title = `Exploitation de ${this.farmer.name}, ${this.departmentRegion}`
    let description = ""
    let descriptionMaxLength = 150

    if (this.farmer.production && this.farmer.production.length > 0) {
      description += `Production de ${this.farmer.production.join(", ")}. `
    }

    description += this.farmer.description || ""
    if (description.length > descriptionMaxLength)
      description = description.substring(0, descriptionMaxLength - 1) + "…"

    return {
      title: title,
      meta: [{ description: description }]
    }
  },
  data() {
    return {
      contactOverlayVisible: false,
      farmerNotFound: false,
    }
  },
  props: {
    farmerUrlComponent: {
      type: String,
      required: true
    }
  },
  computed: {
    farmer() {
      return this.$store.getters.farmerWithUrlComponent(this.farmerUrlComponent)
    },
    departmentRegion() {
      if (this.farmer && this.farmer.postal_code)
        return utils.postalCodeToDepartmentRegion(this.farmer.postal_code)
      return ""
    },
    isMobile() {
      return this.$vuetify.breakpoint.name === "xs"
    },
    breadcrumbs() {
      return [
        {
          text: "Accueil",
          disabled: false,
          to: { name: "Landing" }
        },
        {
          text: this.farmer.name,
          disabled: true
        }
      ]
    },
    approvedExperiments() {
      if (
        !this.farmer ||
        !this.farmer.experiments ||
        this.farmer.experiments.length === 0
      )
        return []
      return this.farmer.experiments.filter(x => !!x.approved)
    }
  },
  methods: {
    getLinkIcon(link) {
      const links = {
        "facebook.com": "mdi-facebook",
        "twitter.com": "mdi-twitter",
        "youtube.com": "mdi-youtube"
      }
      for (const key in links) {
        if (link.includes(key)) return links[key]
      }
      return "mdi-web"
    },
    getLinkColor(link) {
      const links = {
        "facebook.com": "#3b5998",
        "twitter.com": "#1da1f2",
        "youtube.com": "#de0000"
      }
      for (const key in links) {
        if (link.includes(key)) return links[key]
      }
      return "primary"
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
  mounted() {
    if (this.farmer) {
      return
    }

    let sequenceNumber
    try {
      sequenceNumber = this.farmerUrlComponent.split('--')[1]
    } catch (error) {
      this.farmerNotFound = true
      return
    }

    this.$store.commit('SET_FARMERS_LOADING', Constants.LoadingStatus.LOADING)
    Vue.http.get(`/api/v1/farmers/${sequenceNumber}`).then(response => {
      this.$store.commit('SET_FARMERS_LOADING', Constants.LoadingStatus.SUCCESS)
      this.$store.commit('ADD_FARMER', response.body)
    }).catch(() => {
      this.$store.commit('SET_FARMERS_LOADING', Constants.LoadingStatus.IDLE)
      this.farmerNotFound = true
    })
  }
}
</script>
