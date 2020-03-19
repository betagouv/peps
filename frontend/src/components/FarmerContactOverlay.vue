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
          <v-card-text>
            Laissez nous vos coordonnées, notre équipe vous mettra en contact avec {{ farmer.name }}.
          </v-card-text>
          <v-card-text>
            <Form
              style="margin-bottom: 0px;"
              :elevation="0"
              :schema="contactSchema"
              :options="contactOptions"
              updateActionName="addContactFormData"
              storeDataName="contactFormData"
            />
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
                :disabled="!complete"
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
import formutils from "@/formutils"
import Constants from "@/constants"
import Loader from "@/components/Loader.vue"
import Form from "@/components/forms/Form.vue"

export default {
  name: "FarmerContactOverlay",
  components: { Loader, Form },
  data: () => ({
    windowHeight: window.innerHeight - 30,
    contactSchema: {
      type: "object",
      properties: {
        name: {
          type: "string"
        },
        email: {
          type: "string"
        },
        phone: {
          type: "string"
        }
      }
    },
    contactOptions: {
      fields: {
        name: {
          placeholder: "Nom Prénom",
          mdiIcon: "mdi-account"
        },
        email: {
          placeholder: "nom@adresse.com",
          mdiIcon: "mdi-email"
        },
        phone: {
          placeholder: "06 12 34 56 78",
          mdiIcon: "mdi-cellphone-android"
        }
      }
    }
  }),
  props: {
    farmer: {
      type: Object,
      required: true,
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
    complete() {
      return formutils.formIsComplete(
        this.contactSchema,
        this.contactOptions,
        this.$store.state.contactFormData
      )
    }
  },
  created() {
    window.addEventListener("resize", this.onWindowResize)
  },
  destroyed() {
    window.removeEventListener("resize", this.onWindowResize)
  },
  methods: {
    close() {
      this.$store.dispatch("resetContactLoadingStatus")
      this.$emit("done")
    },
    cancelImplementation() {
      window.sendTrackingEvent("Landing", "contactFarmer cancel", "")
      this.$emit("done")
    },
    sendImplementation() {
      window.sendTrackingEvent("Landing", "contactFarmer confirm", "")
      this.$store.dispatch("sendFarmerContactRequest", { farmer: this.farmer })
    },
    onWindowResize() {
      this.windowHeight = window.innerHeight - 30
    }
  },
  watch: {
    sendingError(value) {
      if (value) {
        this.close()
      }
    }
  }
}
</script>

<style scoped>
.v-overlay {
  z-index: 99999 !important;
}
.close-overlay {
  position: absolute;
  right: -10px;
  top: -20px;
  z-index: 99999;
}
</style>