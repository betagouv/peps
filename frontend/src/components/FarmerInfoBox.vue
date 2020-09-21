<template>
  <div>
    <!-- INSTALLATION DATE -->
    <div v-if="farmer.installation_date" class="body-2 info-item">
      <v-icon small left>mdi-calendar-blank-outline</v-icon>
      <div>Installation : {{farmer.installation_date.substring(0, 4)}}</div>
    </div>

    <!-- PERSONNEL -->
    <div v-if="farmer.personnel" class="body-2 info-item">
      <v-icon small left>mdi-card-account-details-outline</v-icon>
      <div>Effectif : {{farmer.personnel}} temps plein</div>
    </div>

    <!-- LIVESTOCK TYPES -->
    <div
      v-if="farmer.livestock_types && farmer.livestock_types.length > 0"
      class="body-2 info-item"
    >
      <v-icon small left>mdi-cow</v-icon>
      <div>
        Élevage :
        <span v-for="(livestock, index) in farmer.livestock_types" :key="index">{{livestock}},</span>
        <span v-if="farmer.livestock_number">({{ farmer.livestock_number }})</span>
      </div>
    </div>

    <!-- AGRICULTURE TYPES -->
    <div
      v-if="farmer.agriculture_types && farmer.agriculture_types.length > 0"
      class="body-2 info-item"
    >
      <v-icon small left>mdi-tractor</v-icon>
      <div>
        Types d'agriculture :
        <span
          v-for="(agricultureType, index) in farmer.agriculture_types"
          :key="index"
        >
          {{agricultureType}}
          <span
            v-if="farmer.agriculture_types.length > 1 && index < farmer.agriculture_types.length - 1"
          >,</span>
        </span>
      </div>
    </div>

    <!-- CULTURES -->
    <div v-if="farmer.cultures" class="body-2 info-item">
      <v-icon small left>mdi-leaf</v-icon>
      <div>Cultures : {{farmer.cultures}}</div>
    </div>

    <!-- GROUPS -->
    <div v-if="farmer.groups && farmer.groups.length > 0" class="body-2 info-item">
      <v-icon small left>mdi-account-group</v-icon>
      <div>
        Groupes :
        <span v-for="(group, index) in farmer.groups" :key="index">
          {{group}}
          <span v-if="farmer.groups.length > 1 && index < farmer.groups.length - 1">,</span>
        </span>
      </div>
    </div>

    <!-- SOIL TYPE -->
    <div v-if="farmer.soil_type" class="body-2 info-item">
      <v-icon small left>mdi-drag-horizontal</v-icon>
      <div>Type de sol : {{farmer.soil_type}}</div>
    </div>


    <!-- SURFACE -->
    <div v-if="farmer.surface" class="body-2 info-item">
      <v-icon small left>mdi-texture-box</v-icon>
      <div>
        Surface : {{farmer.surface}} ha
        <span
          v-if="farmer.surface_cultures || farmer.surface_meadows"
        >
          dont&nbsp;
          <span
            v-if="farmer.surface_cultures"
          >{{farmer.surface_cultures}} ha en cultures</span>
          <span v-if="farmer.surface_cultures && farmer.surface_meadows">&nbsp;et&nbsp;</span>
          <span v-if="farmer.surface_meadows">{{farmer.surface_meadows}} ha en prairie</span>
        </span>
      </div>
    </div>

    <!-- OUTPUT -->
    <div v-if="farmer.output" class="body-2 info-item">
      <v-icon small left>mdi-silo</v-icon>
      <div>Potentiel de rendement en blé : {{farmer.output}} quintaux / ha</div>
    </div>
  </div>
</template>

<script>
export default {
  name: "FarmerInfoBox",
  props: {
    farmer: {
      type: Object,
      required: true
    }
  },
}
</script>

<style scoped>
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
