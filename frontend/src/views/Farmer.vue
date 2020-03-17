<template>
  <div>
    <div v-if="farmer">
      <Title :title="farmer.name" :breadcrumbs="breadcrumbs" />
      <v-container class="constrained" style="padding-top: 10px;">
        <v-card style="margin-bottom: 20px" outlined shaped>
          <!-- <v-img
          class="white--text align-end"
          height="110px"
          :src="farmer.backgroundPhoto"
          style="background: #CCC;"
          />-->

          <div style="margin: 20px 20px 20px 20px;  " class="pa-0 d-flex">
            <v-avatar size="100" color="grey">
              <v-img :src="farmer.profile_image" v-if="farmer.profile_image"></v-img>
              <v-icon v-else large>mdi-account</v-icon>
            </v-avatar>
            <div style="padding-left: 30px;">
              <div class="title">
                {{ farmer.name }}
                <v-chip
                  small
                  class
                  style="margin-top:-4px; margin-left: 10px;"
                  v-for="(title, index) in (farmer.profession || [])"
                  :key="index"
                >{{ title }}</v-chip>
              </div>
              <div v-if="farmer.postal_code" style="margin-top: 3px;" class="caption">
                <v-icon small>mdi-map-marker</v-icon>
                {{ farmer.postal_code }}
              </div>

              <v-btn
                v-if="farmer.contact_possible"
                class="text-none"
                style="margin-top: 10px"
                small
                outlined
                color="primary"
              >Contacter {{farmer.name}}</v-btn>
            </div>
          </div>
        </v-card>

        <div v-if="farmer.installation_date" class="caption info-item">
          <v-icon small left style="padding-bottom: 3px;">mdi-calendar-blank-outline</v-icon>
          Exploitation installée depuis le {{farmer.installation_date}}
        </div>
        <div v-if="farmer.personnel" class="caption info-item">
          <v-icon small left style="padding-bottom: 3px;">mdi-account-group</v-icon>
          Effectif : {{farmer.personnel}}
        </div>
        <div v-if="farmer.livestock_type" class="caption info-item">
          <v-icon small left style="padding-bottom: 3px;">mdi-cow</v-icon>
          Élevage : {{farmer.livestock_type}}
          <span
            v-if="farmer.livestock_number"
          >({{ farmer.livestock_number }})</span>
        </div>
        <div v-if="farmer.cultures" class="caption info-item">
          <v-icon small left style="padding-bottom: 3px;">mdi-leaf</v-icon>
          Cultures : {{farmer.cultures}}
        </div>
        <div v-if="farmer.soil_type" class="caption info-item">
          <v-icon small left style="padding-bottom: 3px;">mdi-drag-horizontal</v-icon>
          Type de sol : {{farmer.soil_type}}
        </div>
        <div v-if="farmer.surface" class="caption info-item">
          <v-icon small left style="padding-bottom: 3px;">mdi-texture-box</v-icon>
          Surface : {{farmer.surface}}
          <span
            v-if="farmer.surface_cultures || farmer.surface_meadows"
          >
            dont&nbsp;
            <span v-if="farmer.surface_cultures">{{farmer.surface_cultures}} en cultures</span>
            <span v-if="farmer.surface_cultures && farmer.surface_meadows">&nbsp;et&nbsp;</span>
            <span v-if="farmer.surface_meadows">{{farmer.surface_meadows}} en prairie</span>
          </span>
        </div>
        <div v-if="farmer.output" class="caption info-item">
          <v-icon small left style="padding-bottom: 3px;">mdi-silo</v-icon>
          Rendement : {{farmer.output}} quintaux / ha
        </div>

        <div class="subtitle-2" style="margin-top: 20px;">Son exploitation</div>
        <div class="body-2 practice-description" style="margin-top: 5px;">{{ farmer.description }}</div>

        <div class="subtitle-2" style="margin-top: 20px;" v-if="farmer.specificities">Spécifités</div>
        <div
          class="body-2 practice-description"
          style="margin-top: 5px;"
          v-if="farmer.specificities"
        >{{ farmer.specificities }}</div>

        <div class="subtitle-2" style="margin-top: 20px;">Ses expérimentations</div>
        <v-row>
          <v-col
            v-for="(experiment, index) in farmer.experiments"
            :key="index"
            cols="12"
            sm="6"
            md="4"
          >
            <ExperimentCard :experiment="experiment" />
          </v-col>
        </v-row>
      </v-container>
    </div>
  </div>
</template>

<script>
import ExperimentCard from "@/components/ExperimentCard"
import Title from "@/components/Title.vue"

export default {
  name: "Farmer",
  components: { Title, ExperimentCard },
  props: {
    farmerName: {
      type: String,
      required: true
    }
  },
  computed: {
    farmer() {
      return this.$store.getters.farmerWithName(this.farmerName)
    },
    breadcrumbs() {
      return [
        {
          text: "Carte des expérimentations",
          disabled: false,
          href: "/#/map"
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

.info-item {
  margin-top: 5px;
}
</style>
