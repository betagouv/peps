<template>
  <v-card class="flex-container" outlined>
    <MiniMap style="padding-top: 15px;" v-if="showMiniMap" :lat='farmer.lat' :lon='farmer.lon' />

    <v-list-item class="flex-fix-item" style="margin: 5px 0 0px 0;">
      <v-list-item-avatar :size="avatarSize" color="grey" style="margin-right: 8px;">
        <v-img :src="farmer.profile_image" v-if="farmer.profile_image"></v-img>
        <v-icon v-else>mdi-account</v-icon>
      </v-list-item-avatar>
      <v-list-item-content>
        <v-list-item-title :class="{'title': !compact, 'subtitle-2': compact}" style="padding-left: 3px;">
          <img
            src="/static/images/marker-icon-2x-red.png"
            v-if="showMapPin"
            height="18px"
            style="display:inline-block; margin-bottom: -3px; margin-right: 2px;"
          />
          {{ farmer.name }}
        </v-list-item-title>
      </v-list-item-content>
    </v-list-item>

    <v-card-text
      style="padding: 5px;"
      class="flex-fix-item"
      v-if="farmer.production && farmer.production.length > 0"
    >
      <v-chip
        small
        class
        style="margin-top:-4px; margin-left: 10px;"
        v-for="(title, index) in (farmer.production || [])"
        :key="index"
      >{{ title }}</v-chip>
    </v-card-text>

    <v-card-text class="flex-fix-item" style="padding-top: 3px; padding-bottom: 0;">
      <v-btn
        block
        class="text-none"
        color="primary"
        :outlined="ctaSecondary"
        max-width="50"
        @click="goToFarmer(farmer)"
      >Voir le profil</v-btn>
    </v-card-text>

    <v-card-text
      v-if="farmer.experiments && farmer.experiments.length > 0"
      class="body-2 flex-fix-item info-item"
      style="color: #666; padding-bottom: 0; padding-top: 15px;"
    >
      <v-icon size="20" style="margin: -3px 3px 0 0;">mdi-beaker-outline</v-icon>
      <div
        style="font-weight: bold;"
      >{{farmer.experiments.length}} Expérimentation{{farmer.experiments.length > 1 ? 's' : ''}}</div>
    </v-card-text>

    <v-divider class="flex-fix-item" style="margin: 10px 15px 10px 15px;" />

    <v-card-subtitle
      v-if="farmer.groups && farmer.groups.length > 0"
      class="subtitle-2 flex-fix-item"
      style="padding-bottom: 5px; padding-top: 0;"
    >Exploitation</v-card-subtitle>

    <v-card-text
      v-if="farmer.surface"
      style="padding-bottom: 5px; padding-top: 0px;"
      class="body-2 flex-fix-item"
    >
      <div>
        {{farmer.surface}} ha
        <span v-if="farmer.surface_cultures || farmer.surface_meadows">
          dont&nbsp;
          <span v-if="farmer.surface_cultures">{{farmer.surface_cultures}} ha en cultures</span>
          <span v-if="farmer.surface_cultures && farmer.surface_meadows">&nbsp;et&nbsp;</span>
          <span v-if="farmer.surface_meadows">{{farmer.surface_meadows}} ha en prairie</span>
        </span>
      </div>
    </v-card-text>

    <v-card-text
      v-if="farmer.cultures"
      style="padding-bottom: 10px; padding-top: 0;"
      class="body-2 flex-shink-item"
    >
      <div>{{farmer.cultures}}</div>
    </v-card-text>

    <v-card-text
      v-if="farmer.agriculture_types && farmer.agriculture_types.length > 0"
      class="body-2 flex-fix-item"
      style="padding: 5px;"
    >
      <v-chip
        small
        class
        style="margin-top:-4px; margin-left: 10px;"
        v-for="(title, index) in (farmer.agriculture_types || [])"
        :key="index"
      >{{ title }}</v-chip>
    </v-card-text>

    <v-divider class="flex-fix-item" style="margin: 0px 15px 10px 15px;" />
    <v-card-subtitle
      v-if="farmer.groups && farmer.groups.length > 0"
      class="subtitle-2 flex-fix-item"
      style="padding-bottom: 5px; padding-top: 0;"
    >Groupes</v-card-subtitle>
    <v-card-text class="flex-fix-item body-2" v-if="farmer.groups && farmer.groups.length > 0">
      <span v-for="(group, index) in farmer.groups" :key="index">
        {{group}}
        <span v-if="farmer.groups.length > 1 && index < farmer.groups.length - 1">,</span>
      </span>
    </v-card-text>
  </v-card>
</template>

<script>
import MiniMap from "@/components/MiniMap.vue"

export default {
  name: "FarmerCard",
  components: { MiniMap },
  props: {
    farmer: {
      type: Object,
      required: true
    },
    ctaSecondary: {
      type: Boolean,
      default: false
    },
    showMiniMap: {
      type: Boolean,
      default: false
    },
    showMapPin: {
      type: Boolean,
      default: false
    },
    avatarSize: {
      type: Number,
      default: 40
    },
    compact: {
      type: Boolean,
      default: false
    }
  },
  methods: {
    goToFarmer(farmer) {
      window.sendTrackingEvent("FarmerCard", "seeProfile", farmer.name)
      this.$router.push({
        name: "Farmer",
        params: { farmerName: farmer.name }
      })
    },
    goToExperiment(farmer, experiment) {
      window.sendTrackingEvent(
        "FarmerCard",
        "seeXP",
        farmer.name + " : " + experiment.name
      )
      this.$router.push({
        name: "Experiment",
        params: {
          farmerName: farmer.name,
          expName: experiment.name
        }
      })
    }
  }
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

.v-chip {
  margin-bottom: 7px;
}

.info-item > div {
  margin-left: 0px;
}

.info-item > i {
  float: left;
  padding-top: 3px;
}
</style>