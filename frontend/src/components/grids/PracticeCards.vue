<template>
  <v-container class="ma-0 pa-0">
    <v-row>
      <v-col v-for="(practice, index) in practices" :key="index" cols="12" sm="6">
        <v-hover>
          <v-card
            class="pa-0 fill-height"
            outlined
            slot-scope="{ hover }"
            :elevation="hover ? 4 : 1"
            @click="goToPractice(practice)"
          >
            <v-img
              class="white--text align-end"
              height="100px"
              :src="practice.image_url || defaultImageUrl"
            />
            <v-card-title class="caption grey--text">{{ practice.mechanism.name }}</v-card-title>
            <v-card-subtitle class="subtitle-2 black--text">{{ practice.title }}</v-card-subtitle>
            <v-card-text>
              <div
                v-for="(infoItem, index) in infoItems(practice)"
                :key="index"
                style="margin-bottom: 5px;"
              >
                <div class="fill-height" style="float: left;">
                  <v-icon size="16px">{{ infoItem.icon }}</v-icon>
                </div>
                <div style="margin-left: 26px;">{{ infoItem.text }}</div>
              </div>
            </v-card-text>
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
    }
  },
  computed: {
    defaultImageUrl() {
      return this.$store.state.defaultPracticeImageUrl
    }
  },
  methods: {
    goToPractice(practice) {
      window.sendTrackingEvent('Category', 'practice', practice.title)
      this.$router.push({ name: "Practice", params: { practiceId: practice.id } })
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