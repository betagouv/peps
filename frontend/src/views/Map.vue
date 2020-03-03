<template>
  <div>
    <v-container class="constrained">
      <div class="pa-0" style="margin-top: 10px;">
        <div class="display-1">
          Le savoir partagé
          <span
            class="cursive"
            style="font-size: 38px; letter-spacing: 0em;"
          >entre agriculteurs</span>
        </div>
        <v-card-text class="title" style="padding: 16px 16px 0px 0;">Trouvez des exemples près de chez vous</v-card-text>
        <v-row style="padding: 0 16px 0 16px;">
          <v-autocomplete
            v-on:change="onAutocompleteChange"
            style="z-index: 9999;"
            :items="departments"
            hide-no-data
            hide-selected
            item-text="nom"
            item-value="code"
            placeholder="Trouvez votre département"
            prepend-icon="mdi-map-search-outline"
            return-object
          ></v-autocomplete>
          <v-btn outlined color="primary" style="margin: 10px 0 0 10px;">
            <v-icon small style="margin: 0 5px 0 0;">mdi-crosshairs-gps</v-icon>Me localiser
          </v-btn>
          <v-spacer class="hidden-sm-and-down" />
        </v-row>
      </div>
    </v-container>

    <v-container class="constrained" style="padding-top:0;">
      <v-row>
        <v-col cols="12" sm="8">
          <l-map
            ref="map"
            :options="{ zoomSnap: 0.2, maxZoom: 10, minZoom: 4, maxBounds: maxBounds }"
            :zoom="zoom"
            :center="center"
            style="height: 520px;border: solid 1px #DDD;"
          >
            <l-geo-json :geojson="geojson" :options="options" :options-style="styleOptions" />
            <l-marker
              v-for="(farmer, index) in markersInfo"
              :key="index"
              :lat-lng="toLatLon(farmer.location.lat, farmer.location.lon)"
              :icon="selectedFarmer && farmer.name === selectedFarmer.name ? selectedMarkerIcon : markerIcon"
              @click="selectFarmer(farmer.name)"
            ></l-marker>
          </l-map>
        </v-col>
        <v-col cols="12" sm="4">
          <FarmerCard
            :farmer="selectedFarmer"
            v-if="selectedFarmer != null"
            style="max-height: 520px; overflow: hidden;"
          />
        </v-col>
      </v-row>

      <div
        class="title"
        style="margin: 30px 0 0px 0;"
      >Vous cherchez une expérimentation en particulier ?</div>
      <v-row style="padding: 0 16px 0 16px;">
        <v-text-field prepend-icon="mdi-file-search" />
        <v-btn outlined color="primary" style="margin: 10px 0 0 10px;">
          <v-icon small style="margin: 0 5px 0 0;">mdi-magnify</v-icon>Chercher
        </v-btn>
        <v-spacer class="hidden-sm-and-down" />
      </v-row>
      <v-row style="padding: 0 16px 0 16px;">
        <v-chip class="ma-2" color="#999" outlined>
          <v-icon left>mdi-sprout</v-icon>Adventices
        </v-chip>
        <v-chip class="ma-2" color="#999" outlined>
          <v-icon left>mdi-ladybug</v-icon>Insectes
        </v-chip>
        <v-chip class="ma-2" color="#999" outlined>
          <v-icon left>mdi-bottle-tonic-plus</v-icon>Maladies
        </v-chip>
        <v-chip class="ma-2" color="#999" outlined>
          <v-icon left>mdi-chart-bell-curve-cumulative</v-icon>Productivité
        </v-chip>
        <v-chip class="ma-2" color="#999" outlined>
          <v-icon left>mdi-bee</v-icon>Biodiversité
        </v-chip>
        <v-chip class="ma-2" color="#999" outlined>
          <v-icon left>mdi-image-filter-hdr</v-icon>Sol
        </v-chip>
        <v-chip class="ma-2" color="#999" outlined>
          <v-icon left>mdi-cow</v-icon>Fourrages
        </v-chip>
        <v-chip class="ma-2" color="#999" outlined>
          <v-icon left>mdi-corn</v-icon>Nouvelles cultures
        </v-chip>
        <v-chip class="ma-2" color="#999" outlined>
          <v-icon left>mdi-cellphone-information</v-icon>OAD
        </v-chip>
      </v-row>
      <v-row>
        <v-col v-for="n in 9" :key="n" cols="12" sm="6" md="4">
          <v-hover>
            <v-card
              class="pa-0 fill-height"
              outlined
              slot-scope="{ hover }"
              :elevation="hover ? 4 : 0"
            >
              <v-img
                class="white--text align-end"
                height="120px"
                style="background: #DDD;"
              />
              <v-card-title>Expérimentation {{n}}</v-card-title>
              <v-card-text>Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam</v-card-text>
            </v-card>
          </v-hover>
        </v-col>
      </v-row>
    </v-container>
  </div>
</template>

<script>
import { LMap, LGeoJson, LMarker } from "vue2-leaflet"
import { latLng, latLngBounds, polygon, icon } from "leaflet"
import FarmerCard from "@/components/FarmerCard.vue"
import geojson from "../resources/departments.json"

export default {
  name: "Map",
  components: { LMap, LMarker, LGeoJson, FarmerCard },
  data() {
    return {
      markersInfo: [],
      showParagraph: false,
      zoom: 5.6,
      center: latLng(46.61322, 2.7),
      geojson: geojson,
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
        shadowSize: [38, 38]
      }),
      selectedMarkerIcon: icon({
        iconUrl: "/static/images/marker-icon-2x-red.png",
        shadowUrl:
          "https://cdnjs.cloudflare.com/ajax/libs/leaflet/0.7.7/images/marker-shadow.png",
        iconSize: [28, 38],
        iconAnchor: [14, 38],
        popupAnchor: [0, -32],
        shadowSize: [38, 38]
      }),
      styleOptions: {
        weight: 1,
        color: "#777",
        opacity: 1,
        fillColor: "#fff",
        fillOpacity: 1
      }
    }
  },
  computed: {
    selectedFarmer() {
      return this.$store.state.selectedFarmer
    },
    selectedDeparment() {
      return this.$store.state.selectedDepartment
    },
    cases() {
      return this.$store.state.cases
    },
    departments() {
      return this.geojson.features.map(x => x.properties)
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
                this.selectedDeparment &&
                currentLayer.id === this.selectedDeparment.code
                  ? "#A6E4D3"
                  : "#FFF"
              currentLayer.setStyle({ fillColor: color })
            }
          })
        }
      }
    }
  },
  methods: {
    onMapDepartmentClick(feature) {
      return () => {
        const department = this.departments.find(
          x => x.code === feature.properties.code
        )
        this.$store.dispatch("setSelectedDepartment", { department })
      }
    },
    selectFarmer(farmerName) {
      this.$store.dispatch("setSelectedFarmer", { farmerName })
    },
    toLatLon(latitude, longitude) {
      return latLng(latitude, longitude)
    },
    onAutocompleteChange(department) {
      this.$store.dispatch("setSelectedDepartment", { department })
    }
  },
  created: function() {
    this.markersInfo = []
    for(const farmer of this.$store.state.cases) {
      this.markersInfo.push(Object.assign({}, {
        location: farmer.location,
        name: farmer.name
      }))
    }    
  },
  watch: {
    selectedDeparment(newValue) {
      if (!newValue) return
      const geojsonFeature = this.geojson.features.find(
        x => x.properties.code == newValue.code
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
          animate: false
        })
      }
      Object.values(this.$refs.map.mapObject._layers).forEach(x => {
        if (!x.setStyle) return
        x.id === this.selectedDeparment.code
          ? x.setStyle({ fillColor: "#A6E4D3" })
          : x.setStyle({ fillColor: "#fff" })
      })
    }
  }
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
