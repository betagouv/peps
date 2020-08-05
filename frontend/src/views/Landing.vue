<template>
  <div>
    <ContributionOverlay
      :visible="showContributionOverlay"
      @done="showContributionOverlay = false"
    />
    <v-container class="constrained">
      <!-- Intro top -->
      <v-row>
        <v-col cols="12" md="9">
          <div class="display-1">
            Le savoir partagé
            <span
              class="cursive"
              style="font-size: 38px; letter-spacing: 0em;"
            >entre agriculteurs</span>
          </div>
          <v-card-text
            class="body-1"
            style="padding: 16px 16px 0px 0;"
          >
          <span style="font-weight: bold;">Voir et partager</span> ses expériences de pratiques agricoles, se <span style="font-weight: bold;">mettre en relation et échanger</span></v-card-text>
          <v-card-text
            class="body-1"
            style="padding: 16px 16px 20px 0;"
          >Peps est un <span style="font-weight: bold;">service public</span> qui permet que les retours de chacun bénéficient aux autres dans la construction d'une agriculture <span style="font-weight: bold;">plus durable pour l'environnement et les Hommes</span></v-card-text>
          <v-btn color="primary" style="margin-bottom: 20px;" href="#explore-xp">
            <v-icon small style="margin-right: 5px;">mdi-beaker-outline</v-icon>
            <span class="text-none">Explorer les expériences</span>
          </v-btn>
        </v-col>

        <v-col cols="3" class="d-none d-md-flex">
          <v-img src="/static/images/agriculteurs-discussion-salade.jpg"></v-img>
        </v-col>
      </v-row>

      <!-- Experiment filters -->
      <h2 class="title pa-0" id="explore-xp" style="margin: 16px 0px;">Explorez les retours d'expérience</h2>
      <ExperimentFilter />

      <!-- Experiments by location -->
      <h2 class="title pa-0" style="margin: 16px 0px;">Des exploitations sur tout le territoire</h2>
      <p class="body-1 pa-0" style="margin: 16px 0px;">Ces exploitantes et exploitants partagent leurs retours d'expériences sur des pratiques agricoles et leurs évolutions</p>
      <v-row style="padding: 0 16px 0 16px;">
        <v-autocomplete
          style="z-index: 9999;"
          :items="departments"
          hide-no-data
          hide-selected
          hide-details
          item-text="nom"
          item-value="code"
          v-model="selectedDepartment"
          placeholder="Trouvez votre département"
          :prepend-icon="searchIcon"
          return-object
        ></v-autocomplete>
        <v-btn
          v-if="showGeolocation"
          outlined
          @click="geolocate()"
          color="primary"
          class="text-none"
          style="margin: 10px 0 0 10px;"
        >
          <v-icon small style="margin: 0 5px 0 0;">mdi-crosshairs-gps</v-icon>
          <span class="d-none d-sm-flex">Me localiser</span>
        </v-btn>
        <v-spacer class="hidden-sm-and-down" />
      </v-row>

      <v-row>
        <v-col cols="12" sm="8">
          <l-map
            ref="map"
            :options="{ zoomSnap: 0.2, maxZoom: 10, minZoom: 4, maxBounds: maxBounds }"
            :zoom="zoom"
            :center="center"
            :style="'height: ' + mapHeight + ';border: solid 1px #DDD;'"
          >
            <l-geo-json
              v-if="geojson"
              :geojson="geojson"
              :options="options"
              :options-style="styleOptions"
            />
            <l-marker
              v-for="(farmer, index) in markersInfo"
              :key="index"
              :lat-lng="toLatLon(farmer.lat, farmer.lon)"
              :icon="selectedFarmer && farmer.id === selectedFarmer.id ? selectedMarkerIcon : markerIcon"
              @click="selectFarmer(farmer.id)"
            ></l-marker>
          </l-map>
        </v-col>
        <v-col cols="12" sm="4">
          <FarmerCard :showMapPin="true" :farmer="selectedFarmer" v-if="!!selectedFarmer" />
          <div v-else class="hidden-sm-and-down">
            <div
              class="title"
              style="color: #AAA"
            >Sélectionnez un point sur la carte pour voir les détails</div>
            <v-icon large color="#AAA">mdi-subdirectory-arrow-left</v-icon>
          </div>
        </v-col>
      </v-row>

      <!-- Contribution proposal -->
      <div style="margin: 20px 0 0px 15px;">
        Vous souhaitez partager votre expérience ?
        <v-btn
          @click="onShareXPClick"
          outlined
          color="primary"
          class="text-none primary--text"
          style="margin-left: 10px; margin-top: -2px;"
        >Partager une expérience</v-btn>
      </div>
    </v-container>
  </div>
</template>

<script>
import { LMap, LGeoJson, LMarker } from "vue2-leaflet"
import { latLng, latLngBounds, polygon, icon } from "leaflet"
import L from "leaflet"
import FarmerCard from "@/components/FarmerCard.vue"
import ExperimentFilter from "@/components/ExperimentFilter.vue"
import Constants from "@/constants"
import ContributionOverlay from "@/components/ContributionOverlay.vue"

export default {
  name: "Landing",
  metaInfo() {
    return {
      title:
        "Peps, les expériences d'agriculteurs - adventices ravageurs maladies",
      meta: [
        {
          description:
            "Grâce aux essais d’agriculteurs, trouvez des réponses à vos questions sur de nombreux thèmes (réduction des charges, autonomie fourragère, maladies…)",
        },
      ],
    }
  },
  components: {
    LMap,
    LMarker,
    LGeoJson,
    FarmerCard,
    ExperimentFilter,
    ContributionOverlay,
  },
  data() {
    return {
      showContributionOverlay: false,
      markersInfo: [],
      showGeolocation: !!window.navigator.geolocation,
      showParagraph: false,
      zoom: 5.6,
      center: latLng(46.61322, 2.7),
      maxBounds: latLngBounds(
        latLng(51.581167, -6.811523),
        latLng(40.868665, 11.513672)
      ),
      markerIcon: icon({
        iconUrl: "/static/images/marker-icon-2x-green.png",
        shadowUrl:
          "https://cdnjs.cloudflare.com/ajax/libs/leaflet/0.7.7/images/marker-shadow.png",
        iconSize: [28, 38],
        iconAnchor: [14, 38],
        popupAnchor: [0, -32],
        shadowSize: [38, 38],
      }),
      selectedMarkerIcon: icon({
        iconUrl: "/static/images/marker-icon-2x-red.png",
        shadowUrl:
          "https://cdnjs.cloudflare.com/ajax/libs/leaflet/0.7.7/images/marker-shadow.png",
        iconSize: [28, 38],
        iconAnchor: [14, 38],
        popupAnchor: [0, -32],
        shadowSize: [38, 38],
      }),
      styleOptions: {
        weight: 1,
        color: "#777",
        opacity: 1,
        fillColor: "#fff",
        fillOpacity: 1,
      },
    }
  },
  computed: {
    geojson() {
      return this.$store.state.geojson
    },
    selectedFarmer() {
      return this.$store.getters.selectedFarmer
    },
    selectedDepartment: {
      get() {
        return this.$store.state.selectedDepartment
      },
      set(department) {
        this.$store.dispatch("setSelectedDepartment", { department })
      },
    },
    farmersLoadingStatus() {
      return this.$store.state.farmersLoadingStatus
    },
    cases() {
      return this.$store.state.farmers
    },
    departments() {
      return this.geojson ? this.geojson.features.map((x) => x.properties) : []
    },
    loggedUser() {
      return this.$store.state.loggedUser
    },
    mapHeight() {
      return this.$vuetify.breakpoint.name === "xs" ? "180px" : "520px"
    },
    searchIcon() {
      return this.$vuetify.breakpoint.name === "xs"
        ? undefined
        : "mdi-map-search-outline"
    },
    options() {
      return {
        onEachFeature: (feature, layer) => {
          const currentLayer = layer
          currentLayer.id = feature.properties.code
          layer.on({
            click: this.onMapDepartmentClick(feature),
            mouseover: () => currentLayer.setStyle({ fillColor: "#d8f3ec" }),
            mouseout: () => {
              const color =
                this.selectedDepartment &&
                currentLayer.id === this.selectedDepartment.code
                  ? "#A6E4D3"
                  : "#FFF"
              currentLayer.setStyle({ fillColor: color })
            },
          })
        },
      }
    },
  },
  methods: {
    onMapDepartmentClick(feature) {
      return () => {
        const department = this.departments.find(
          (x) => x.code === feature.properties.code
        )
        this.selectedDepartment = department
      }
    },
    onShareXPClick() {
      window.sendTrackingEvent("Header", "shareXP", "Partager une expérience")
      if (this.loggedUser && this.loggedUser.farmer_id)
        this.$router.push({ name: "ExperimentEditor" })
      else if (this.loggedUser)
        window.alert("Vous n'avez pas un profil agriculteur sur notre site")
      else this.showContributionOverlay = true
    },
    refreshMapMarkers() {
      this.markersInfo = []
      for (const farmer of this.$store.state.farmers.filter(
        (x) => !!x.approved
      )) {
        this.markersInfo.push(
          Object.assign(
            {},
            {
              lat: farmer.lat,
              lon: farmer.lon,
              name: farmer.name,
              id: farmer.id,
            }
          )
        )
      }
    },
    selectFarmer(farmerId) {
      this.$store.dispatch("setSelectedFarmer", { farmerId })
    },
    toLatLon(latitude, longitude) {
      return latLng(latitude, longitude)
    },
    geolocate() {
      if (!this.geojson) return
      const self = this
      function showPosition(position) {
        const lng = position.coords.longitude
        const lat = position.coords.latitude

        const geojsonFeature = self.geojson.features.find((x) => {
          // Note we reverse lat and lon in the L.latLng object because of
          // https://stackoverflow.com/questions/43549199/leaflet-how-to-swap-coordinates-received-from-an-ajax-call/43549799
          return L.polygon(x.geometry.coordinates).contains(L.latLng(lng, lat))
        })
        const department = self.departments.find(
          (x) => x.code === geojsonFeature.properties.code
        )
        self.selectedDepartment = department
      }
      function handleError(error) {
        console.log(error)
      }
      window.navigator.geolocation.getCurrentPosition(showPosition, handleError)
    },
  },
  created: function () {
    this.refreshMapMarkers()
  },
  watch: {
    selectedDepartment(newValue) {
      if (!newValue || !this.geojson) return
      const geojsonFeature = this.geojson.features.find(
        (x) => x.properties.code == newValue.code
      )
      if (geojsonFeature && geojsonFeature.geometry) {
        const bounds = polygon(geojsonFeature.geometry.coordinates).getBounds()
        const leafletBounds = latLngBounds(
          latLng(bounds._northEast.lng, bounds._northEast.lat),
          latLng(bounds._southWest.lng, bounds._southWest.lat)
        )

        // We use fitBounds with animate: false because of https://github.com/Leaflet/Leaflet/issues/3249
        // If we wanted animation we would have to use flyToBounds but there is the render lag problem
        this.$refs.map.mapObject.fitBounds(leafletBounds, {
          padding: [70, 70],
          animate: false,
        })
      }
      Object.values(this.$refs.map.mapObject._layers).forEach((x) => {
        if (!x.setStyle) return
        x.id === this.selectedDepartment.code
          ? x.setStyle({ fillColor: "#A6E4D3" })
          : x.setStyle({ fillColor: "#fff" })
      })
    },
    farmersLoadingStatus(newValue) {
      if (newValue === Constants.LoadingStatus.SUCCESS) this.refreshMapMarkers()
    },
  },
  mounted() {
    if (
      !this.geojson &&
      this.$store.state.geojsonLoadingStatus !== Constants.LoadingStatus.LOADING
    )
      this.$store.dispatch("fetchGeojson")
  },
}
</script>

<style scoped>
.leaflet-container {
  background: #f5f5f5;
  border-radius: 5px;
}
#landing-image {
  background: #fff;
  background-repeat: no-repeat;
  background-position: center;
  background-size: cover;
  padding-bottom: 10px;
}
</style>
