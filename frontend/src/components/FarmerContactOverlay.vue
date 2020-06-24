<template>
  <div v-if="visible">
    <Loader v-if="sendingInProgress" title="Juste un instant..." :loading="sendingInProgress" />

    <v-overlay :value="visible" :dark="false">
      <div v-if="sendingIdle">
        <v-btn
          @click="cancelImplementation()"
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
          <v-card-text>Laissez nous vos coordonnées, notre équipe vous mettra en contact avec {{ farmer.name }}.</v-card-text>
          <v-card-text>
            <v-form ref="form" v-model="formIsValid">
              <div style="margin-bottom: 5px;">
                <v-text-field
                  placeholder="Nom Prénom"
                  hide-details="auto"
                  outlined
                  prepend-icon="mdi-account"
                  dense
                  :rules="[validators.notEmpty]"
                  v-model="name"
                ></v-text-field>
              </div>
              <div style="margin-bottom: 5px;">
                <v-text-field
                  placeholder="nom@adresse.com"
                  hide-details="auto"
                  outlined
                  prepend-icon="mdi-email"
                  dense
                  :rules="[validators.notEmpty]"
                  v-model="email"
                ></v-text-field>
              </div>
              <div style="margin-bottom: 20px;">
                <v-text-field
                  placeholder="06 12 34 56 78"
                  hide-details="auto"
                  outlined
                  prepend-icon="mdi-cellphone-android"
                  dense
                  :rules="[validators.notEmpty]"
                  v-model="phoneNumber"
                ></v-text-field>
              </div>
            </v-form>

            <div style="text-align: right">
              <v-btn
                class="text-none body-1 practice-buttons"
                style="margin-right: 10px;"
                @click="cancelImplementation()"
                rounded
              >Annuler</v-btn>
              <v-btn
                class="text-none body-1 practice-buttons"
                color="primary"
                @click="sendImplementation()"
                rounded
              >Confirmer</v-btn>
            </div>
          </v-card-text>
        </v-card>
      </div>

      <div v-if="sendingSucceeded">
        <v-btn @click="close()" class="close-overlay" fab dark small color="grey lighten-5">
          <v-icon color="red darken-3">mdi-close</v-icon>
        </v-btn>
        <v-card
          :style="'max-width: 600px; max-height:' + windowHeight + 'px'"
          class="overflow-y-auto"
        >
          <v-card-text
            style="padding: 30px; color: #333;"
          >Merci ! {{ farmer.name }} se mettra en contact avec vous bientôt !</v-card-text>
          <div style="padding: 10px; text-align: right">
            <v-btn
              class="text-none body-1 practice-buttons"
              color="primary"
              @click="close()"
              rounded
            >OK</v-btn>
          </div>
        </v-card>
      </div>
    </v-overlay>
  </div>
</template>

<script>
import Constants from "@/constants"
import Loader from "@/components/Loader.vue"
import validators from "@/validators"

export default {
  name: "FarmerContactOverlay",
  components: { Loader },
  data: () => ({
    windowHeight: window.innerHeight - 30,
    formIsValid: true,
    name: "",
    email: "",
    phoneNumber: ""
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
    sendingIdle() {
      return (
        this.$store.state.contactLoadingStatus === Constants.LoadingStatus.IDLE
      )
    },
    sendingInProgress() {
      return (
        this.$store.state.contactLoadingStatus ===
        Constants.LoadingStatus.LOADING
      )
    },
    sendingSucceeded() {
      return (
        this.$store.state.contactLoadingStatus ===
        Constants.LoadingStatus.SUCCESS
      )
    },
    sendingError() {
      return (
        this.$store.state.contactLoadingStatus === Constants.LoadingStatus.ERROR
      )
    },
    validators() {
      return validators
    },
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
      this.$store.dispatch("resetContactLoadingStatus")
      this.$emit("done")
    },
    cancelImplementation() {
      window.sendTrackingEvent(this.$route.name, "contactFarmer cancel", "")
      this.$emit("done")
    },
    sendImplementation() {
      window.sendTrackingEvent(this.$route.name, "contactFarmer confirm", "")
      this.$store.dispatch("sendFarmerContactRequest", {
        farmer: this.farmer,
        name: this.name,
        email: this.email,
        phoneNumber: this.phoneNumber
      })
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
  },
  watch: {
    sendingError(value) {
      if (value) {
        window.alert("Oops ! Une erreur s’est produite. Veuillez essayer plus tard")
        this.close()
      }
    }
  }
}
</script>
