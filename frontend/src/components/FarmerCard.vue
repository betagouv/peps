<template>
  <v-card>
    <v-img :src="farmer.backgroundPhoto" height="100px" style="background: #CCC;"></v-img>
    <v-list-item style="margin: 10px 0 0 0;">
      <v-list-item-avatar color="grey">
        <v-img :src="farmer.profilePhoto"></v-img>
      </v-list-item-avatar>
      <v-list-item-content>
        <v-list-item-title>
          <img
            src="/static/images/marker-icon-2x-red.png"
            height="18px"
            style="display:inline-block; margin-bottom: -3px; margin-right: 2px;"
          />
          {{ farmer.name }}
        </v-list-item-title>
        <v-list-item-subtitle>GAEC Les Champs</v-list-item-subtitle>
      </v-list-item-content>
    </v-list-item>
    <v-card-subtitle class="subtitle-2" style="padding-bottom: 4px;">Son histoire</v-card-subtitle>
    <v-card-text>{{ farmer.background | truncate(115, '...') }}</v-card-text>
    <v-card-subtitle class="subtitle-2" style="padding-bottom: 4px;">Son exploitation</v-card-subtitle>
    <v-card-text>{{ farmer.description | truncate(115, '...') }}</v-card-text>
    <div class="pa-5">
    <v-btn
      block
      rounded
      class="text-none"
      color="primary"
      max-width=50
      @click="goToFarmer(farmer)"
    >En savoir plus</v-btn>
    </div>
  </v-card>
</template>

<script>
export default {
  name: "FarmerCard",
  props: {
    farmer: {
      type: Object,
      required: true
    }
  },
  data() {
    return {}
  },
  methods: {
    goToFarmer(farmer) {
      this.$router.push({
        name: "Farmer",
        params: { farmerName: farmer.name }
      })
    }
  }
}
</script>
