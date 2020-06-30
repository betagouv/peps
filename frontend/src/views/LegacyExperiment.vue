<template>
  <div>
    <Loader />
  </div>
</template>

<script>
import Loader from "@/components/Loader.vue"

export default {
  /* This view is in charge of handling the redirection towards the old
  URL scheme for experiments (/agriculteur/<url component>/experimentation/<url component>).
  It displays nothing on its own.

  Originally we used a schema /agriculteur/<url component>/experimentation/<url component>
  with an URL component that included a shortened version of a UUID which
  was still quite long.

  After https://github.com/betagouv/peps/issues/185 a serial field was added to
  experiment objects to shorten the URL. The URL changed to
  /exploitation/<new url component>/expérience/<new url component>

  This view will ensure previous URLs still work by being redirected to their
  new URL.
  */
  name: "LegacyExperiment",
  components: { Loader },
  props: {
    legacyFarmerUrlComponent: {
      type: String,
      required: true
    },
    legacyExperimentUrlComponent: {
      type: String,
      required: true
    }
  },
  computed: {
    farmer() {
      return this.$store.getters.farmerWithLegacyUrlComponent(
        this.legacyFarmerUrlComponent
      )
    },
    experiment() {
      if (!this.farmer) return
      return this.$store.getters.experimentWithLegacyUrlComponent(
        this.farmer,
        this.legacyExperimentUrlComponent
      )
    },
    experimentNotFound() {
      return this.$store.getters.experiments.length > 0 && !this.experiment
    }
  },
  methods: {
    redirectToNewUrl() {
      if (!this.experimentNotFound) {
        this.$router.push({ name: "Map" })
      }
      if (this.experiment) {
        this.$router.push({
          name: "Experiment",
          params: {
            farmerUrlComponent: this.$store.getters.farmerUrlComponent(
              this.farmer
            ),
            experimentUrlComponent: this.$store.getters.experimentUrlComponent(
              this.experiment
            )
          }
        })
      }
    }
  },
  watch: {
    experiment() {
      this.redirectToNewUrl()
    },
    experimentNotFound() {
      this.redirectToNewUrl()
    }
  },
  mounted() {
    this.redirectToNewUrl()
  }
}
</script>