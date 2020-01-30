<template>
  <v-container class="constrained ma-0 pa-0">
    <v-row>
      <v-col v-for="(practice, index) in practices" :key="index" cols="12" sm="6" md="4">
        <v-hover>
          <v-card
            class="pa-0 fill-height"
            outlined
          >
            <v-img
              class="white--text align-end"
              height="120px"
              :src="practice.image || defaultImageUrl"
            />
            <v-card-title class="caption grey--text">{{ practice.mechanism.name }}</v-card-title>
            <v-card-subtitle class="practice-title subtitle-2 black--text" @click="goToPractice(practice)">{{ practice.title }}</v-card-subtitle>
            <v-card-text :style="'margin-bottom:' + textBottomMargin + ';'">
              <div
                v-for="(infoItem, index) in infoItems(practice)"
                :key="index"
                style="margin-bottom: 5px;"
              >
                <div class="fill-height" style="float: left;">
                  <v-icon size="16px">{{ infoItem.icon }}</v-icon>
                </div>
                <div class="caption" style="margin-left: 22px;">{{ infoItem.text }}</div>
              </div>
            </v-card-text>
            <div style="bottom: 16px; position: absolute; width: 100%;">
              <div style="margin: 0 16px 0 16px;">
                <v-btn
                  block
                  class="text-none"
                  v-if="displayDiscardButton"
                  text
                  style="text-decoration: underline; margin-bottom:5px;"
                  color="primary"
                  @click.stop.prevent="blacklistPractice(practice)"
                >Recalculer sans cette pratique</v-btn>
                <v-btn
                  block
                  rounded
                  class="text-none"
                  color="primary"
                  @click.stop.prevent="goToPractice(practice)"
                >En savoir plus</v-btn>
              </div>
            </div>
          </v-card>
        </v-hover>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
export default {
  name: "PracticeCards",
  props: {
    practices: {
      type: Array,
      required: true
    },
    displayDiscardButton: {
      type: Boolean,
      default: false
    }
  },
  computed: {
    defaultImageUrl() {
      return this.$store.state.defaultPracticeImageUrl
    },
    textBottomMargin() {
      return this.displayDiscardButton ? "77px" : "45px"
    }
  },
  methods: {
    goToPractice(practice) {
      window.sendTrackingEvent("Practice", "more-info", practice.title)
      this.$router.push({
        name: "Practice",
        params: { practiceShortTitle: practice.short_title }
      })
    },
    blacklistPractice(practice) {
      window.sendTrackingEvent("Practice", "blacklist", practice.title)
      this.$emit("blacklist", practice)
    },
    infoItems(practice) {
      let infoItems = []
      const infoItemsDescriptors = [
        {
          property: "equipment",
          icon: "mdi-wrench"
        },
        {
          property: "schedule",
          icon: "mdi-calendar-blank-outline"
        },
        {
          property: "impact",
          icon: "mdi-leaf"
        },
        {
          property: "additional_benefits",
          icon: "mdi-plus-circle"
        },
        {
          property: "success_factors",
          icon: "mdi-information"
        }
      ]
      for (let i = 0; i < infoItemsDescriptors.length; i++) {
        if (practice[infoItemsDescriptors[i].property]) {
          infoItems.push({
            icon: infoItemsDescriptors[i].icon,
            text: practice[infoItemsDescriptors[i].property]
          })
        }
      }
      return infoItems
    }
  }
}
</script>

<style scoped>
.practice-title {
  text-decoration: underline;
  cursor: pointer;
}
</style>