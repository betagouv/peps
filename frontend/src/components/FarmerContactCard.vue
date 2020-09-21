<template>
  <v-card class="flex-container" outlined>

    <v-list-item class="flex-fix-item" style="margin: 5px 0 0px 0;">
      <v-list-item-avatar size="70" color="grey" style="margin-right: 8px;">
        <v-img :src="farmer.profile_image" v-if="farmer.profile_image"></v-img>
        <v-icon v-else>mdi-account</v-icon>
      </v-list-item-avatar>
      <v-list-item-content>
        <v-list-item-title class="subtitle-2" style="padding-left: 3px;">
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
      <v-btn block class="text-none d-block pa-2" height="auto" color="primary" @click="onContactClick">
        <span style="white-space: normal;">
        Discuter avec {{ farmer.name }}
        <v-icon small style="margin-left: 5px;">mdi-message</v-icon>
        </span>
      </v-btn>
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
      class="body-2 flex-shrink-item"
    >
      <div>{{farmer.cultures}}</div>
    </v-card-text>

    <MiniMap :lat="farmer.lat" :lon="farmer.lon" :size="100" />

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

      <v-btn block class="text-none" text tile color="#2c3e50" style="border-top: solid 1px;" @click="goToFarmer(farmer)">
        Voir son profil
      </v-btn>
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
      required: true,
    },
    onContactClick: {
      type: Function,
      required: true
    },
    goToFarmer: {
      type: Function,
      required: true
    }
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