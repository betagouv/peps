<template>
  <div>
    <Loader />
  </div>
</template>

<script>
import Constants from "@/constants"
import Loader from "@/components/Loader.vue"

export default {
  /* This view is in charge of handling the redirection towards the old
  URL scheme for farmers (/agriculteur/<url component>. It displays nothing
  on its own.

  Originally we used a schema /agriculteur/<url component> with an URL component
  that included a shortened version of a UUID which was still quite long.

  After https://github.com/betagouv/peps/issues/184 a serial field was added to
  farmer objects to shorten the URL. The URL changed to /exploitation/<new url component>

  This view will ensure previous URLs still work by being redirected to their
  new URL.
  */
  name: 'LegacyFarmer',
  components: { Loader },
  props: {
    legacyFarmerUrlComponent: {
      type: String,
      required: true,
    }
  },
  computed: {
    farmer() {
      return this.$store.getters.farmerWithLegacyUrlComponent(this.legacyFarmerUrlComponent)
    },
    farmerNotFound() {
      return (
        this.$store.state.farmersLoadingStatus ===
          Constants.LoadingStatus.SUCCESS &&
        this.$store.state.farmers.length > 0 &&
        !this.farmer
      )
    },
  },
  methods: {
    redirectToNewUrl() {
      if (!this.farmerNotFound) {
        this.$router.push({ name: "Map" })
      }
      if (this.farmer) {
        this.$router.push({
          name: "Farmer",
          params: { farmerUrlComponent: this.$store.getters.farmerUrlComponent(this.farmer) }
        })
      }
    }
  },
  watch: {
    farmer() {
      this.redirectToNewUrl()
    },
    farmerNotFound() {
      this.redirectToNewUrl()
    }
  },
  mounted() {
    this.redirectToNewUrl()
  }
}
</script>