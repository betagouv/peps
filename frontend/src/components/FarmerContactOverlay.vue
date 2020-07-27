<template>
  <div v-if="visible">

    <v-overlay :value="visible" :dark="false">
      <div>
        <v-btn
          @click="close()"
          class="close-overlay"
          fab
          dark
          small
          color="grey lighten-5"
        >
          <v-icon color="red darken-3">mdi-close</v-icon>
        </v-btn>
        <v-card
          :style="'margin-left: 10px; margin-right: 10px; max-width: 600px; max-height:' + windowHeight + 'px'"
          class="overflow-y-auto"
        >
          <v-card-title>Contacter {{ farmer.name }}</v-card-title>
          <v-card-text>Afin de garantir la qualité des échanges sur la plateforme, il est nécessaire d'avoir un compte avant d'entrer en contact avec un agriculteur.</v-card-text>
          <v-card-text style="padding-top: 0px; padding-bottom: 20px;">
              <v-container style="padding-top: 0px; padding-bottom: 0px;">
                <v-row>
                  <v-col  cols="12" sm="6" :style="'padding-bottom: 0px; ' + ($vuetify.breakpoint.name !== 'xs' ? 'border-right: solid 1px #DDD;' : '')">
                    <div class="subtitle-2">J'ai déjà un compte</div>
                    <div style="margin-bottom: 20px;">
                      <v-btn
                        style="margin-top: 5px;"
                        class="text-none practice-buttons"
                        color="primary"
                        outlined
                        href="/login"
                      >M'identifier</v-btn>
                    </div>
                  </v-col>
                  <v-col  cols="12" sm="6" style="padding-bottom: 0px;">
                    <div class="subtitle-2">Je créé un compte</div>
                    <div>
                      <v-btn
                        style="margin-top: 5px;"
                        class="text-none practice-buttons"
                        color="primary"
                        outlined
                        href="/register"
                      >Créer mon compte</v-btn>
                    </div>
                  </v-col>
                </v-row>
              </v-container>
            </v-card-text>
        </v-card>
      </div>
    </v-overlay>
  </div>
</template>

<script>
export default {
  name: "FarmerContactOverlay",
  data: () => ({
    windowHeight: window.innerHeight - 30,
  }),
  props: {
    farmer: {
      type: Object,
      required: true
    },
    visible: {
      type: Boolean,
      default: false
    }
  },
  computed: {
    loggedUser() {
      return this.$store.state.loggedUser
    }
  },
  mounted() {
    window.addEventListener("resize", this.onWindowResize)
    this.name = this.getInitialName()
    this.email = this.getInitialEmail()
    this.phoneNumber = this.getInitialPhoneNumber()
  },
  beforeDestroy() {
    window.removeEventListener("resize", this.onWindowResize)
  },
  methods: {
    close() {
      this.$emit("done")
    },
    onWindowResize() {
      this.windowHeight = window.innerHeight - 30
    },
    getInitialName() {
      if (this.loggedUser && this.loggedUser.farmer_id)
        return this.$store.getters.farmerWithId(this.loggedUser.farmer_id).name
      if (this.$store.state.lastContactInfo && this.$store.state.lastContactInfo.name)
        return this.$store.state.lastContactInfo.name
      return null
    },
    getInitialEmail() {
      if (this.loggedUser)
        return this.loggedUser.email
      if (this.$store.state.lastContactInfo && this.$store.state.lastContactInfo.email)
        return this.$store.state.lastContactInfo.email
      return null
    },
    getInitialPhoneNumber() {
      if (this.loggedUser && this.loggedUser.farmer_id)
        return this.$store.getters.farmerWithId(this.loggedUser.farmer_id).phone_number
      if (this.$store.state.lastContactInfo && this.$store.state.lastContactInfo.phoneNumber)
        return this.$store.state.lastContactInfo.phoneNumber
      return null
    }
  }
}
</script>
