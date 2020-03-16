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
        <v-card-text
          class="title"
          style="padding: 16px 16px 0px 0;"
        >Trouvez des exemples près de chez vous</v-card-text>
        <v-row style="padding: 0 16px 0 16px;">
          <v-autocomplete
            style="z-index: 9999;"
            :items="departments"
            hide-no-data
            hide-selected
            item-text="nom"
            item-value="code"
            v-model="selectedDepartment"
            placeholder="Trouvez votre département"
            prepend-icon="mdi-map-search-outline"
            return-object
          ></v-autocomplete>
          <v-btn
            v-if="showGeolocation"
            outlined
            @click="geolocate()"
            color="primary"
            style="margin: 10px 0 0 10px;"
          >
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
              :lat-lng="toLatLon(farmer.lat, farmer.lon)"
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
      <ExperimentFilter />
    </v-container>
  </div>
</template>

<script>
import { LMap, LGeoJson, LMarker } from "vue2-leaflet"
import { latLng, latLngBounds, polygon, icon } from "leaflet"
import L from "leaflet"
import FarmerCard from "@/components/FarmerCard.vue"
import ExperimentFilter from "@/components/ExperimentFilter.vue"
import geojson from "../resources/departments.json"

export default {
  name: "Map",
  components: { LMap, LMarker, LGeoJson, FarmerCard, ExperimentFilter },
  data() {
    return {
      markersInfo: [],
      showGeolocation: !!window.navigator.geolocation,
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
    selectedDepartment: {
      get() {
        return this.$store.state.selectedDepartment
      },
      set(department) {
        this.$store.dispatch("setSelectedDepartment", { department })
      }
    },
    cases() {
      return this.$store.state.farmers
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
                this.selectedDepartment &&
                currentLayer.id === this.selectedDepartment.code
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
        this.selectedDepartment = department
      }
    },
    selectFarmer(farmerName) {
      this.$store.dispatch("setSelectedFarmer", { farmerName })
    },
    toLatLon(latitude, longitude) {
      return latLng(latitude, longitude)
    },
    geolocate() {
      const self = this
      function showPosition(position) {
        const lng = position.coords.longitude
        const lat = position.coords.latitude
        console.log(`longitude: ${lng} | latitude: ${lat}`)

        const geojsonFeature = self.geojson.features.find(x => {
          // Note we reverse lat and lon in the L.latLng object because of
          // https://stackoverflow.com/questions/43549199/leaflet-how-to-swap-coordinates-received-from-an-ajax-call/43549799
          return L.polygon(x.geometry.coordinates).contains(L.latLng(lng, lat))
        })
        console.log(`geojson Feature: ${geojsonFeature}`)
        const department = self.departments.find(
          x => x.code === geojsonFeature.properties.code
        )
        self.selectedDepartment = department
      }
      function handleError(error) {
        console.log(error)
      }
      window.navigator.geolocation.getCurrentPosition(showPosition, handleError)
    }
  },
  created: function() {
    this.markersInfo = []
    for (const farmer of this.$store.state.farmers) {
      this.markersInfo.push(
        Object.assign(
          {},
          {
            lat: farmer.lat,
            lon: farmer.lon,
            name: farmer.name
          }
        )
      )
    }
  },
  watch: {
    selectedDepartment(newValue) {
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
        x.id === this.selectedDepartment.code
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