<template>
  <div>
    <ContributionOverlay
      :visible="showContributionOverlay"
      @done="showContributionOverlay = false"
    />
    <div class="banner pa-2">
      <div style="margin-left: auto; margin-right: auto; padding: 0 30px 0 10px;">
        <v-icon style="margin-top: -7px; margin-right: 10px;">mdi-lightbulb-on</v-icon>
        <span>Nous avons besoin de vous pour faire évoluer ce service.</span>
        <a
          @click="contribute()"
          style="display: inline; margin-left: 10px; text-decoration: underline;"
        >Je contribue !</a>
      </div>
      <v-icon
        @click="close()"
        color="primary"
        style="position: absolute; right: 5px;"
      >mdi-close-circle</v-icon>
    </div>
  </div>
</template>

<script>
import ContributionOverlay from "@/components/ContributionOverlay.vue"

export default {
  name: "ContributionBanner",
  components: {
    ContributionOverlay
  },
  data: () => {
    return {
      showContributionOverlay: false
    }
  },
  methods: {
    contribute() {
      window.sendTrackingEvent("Header", "contribute", "Je contribue")
      this.showContributionOverlay = true
    },
    close() {
      this.$store.dispatch("discardContributionPrompt")
    }
  }
}
</script>
<style scoped>
.banner {
  position: relative;
  -webkit-box-align: center;
  -ms-flex-align: center;
  align-items: center;
  display: -webkit-box;
  display: -ms-flexbox;
  display: flex;
  font-size: 0.875rem;
  font-weight: 400;
  width: 100%;
  background: #F0F0F0;
  border-bottom: 2px solid #B9B9B9;
}
</style>