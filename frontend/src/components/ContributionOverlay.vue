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
          <div v-if="needsAccount === undefined">
            <v-card-title>Identifiez vous pour partager une expérience</v-card-title>

            <v-card-text>
              <v-container>
              <v-row style="text-align: center;">
                <v-col cols="6" style="border-right: solid 1px #ccc;">
                  J'ai déjà un compte
                  
                    <div style="text-align: center">
                      <v-btn
                        class="text-none practice-buttons"
                        color="primary"
                        style="margin-top: 10px"
                        outlined
                        href="/login"
                      >S'identifier</v-btn>
                    </div>

                </v-col>
                <v-col cols="6">
                  Je n'ai pas de compte Peps
                    <div style="text-align: center">
                      <v-btn
                        class="text-none practice-buttons"
                        color="primary"
                        style="margin-top: 10px"
                        href="/register"
                      >Créer mon compte</v-btn>
                    </div>

                </v-col>
              </v-row>
            </v-container>
            </v-card-text>
          </div>

          <div v-if="needsAccount === true">
            <v-card-title>Créer votre compte</v-card-title>
            <v-card-text>Laissez-nous vos coordonnées pour que nous prenions contact.</v-card-text>
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
                  class="text-none practice-buttons"
                  style="margin-right: 10px;"
                  @click="cancelImplementation()"
                  text
                >Annuler</v-btn>
                <v-btn
                  class="text-none practice-buttons"
                  color="primary"
                  :disabled="!complete"
                  @click="sendImplementation()"
                >Confirmer</v-btn>
              </div>
            </v-card-text>
          </div>
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
          >Merci ! Notre équipe vous contactera bientôt</v-card-text>
          <div style="padding: 10px; text-align: right">
            <v-btn class="text-none body-1 practice-buttons" color="primary" @click="close()">OK</v-btn>
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
  name: "ContributionOverlay",
  components: { Loader, Form },
  data: () => ({
    windowHeight: window.innerHeight - 30,
    needsAccount: undefined,
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
      this.needsAccount = undefined
    },
    cancelImplementation() {
      window.sendTrackingEvent("Landing", "shareXP cancel", "")
      this.$emit("done")
    },
    sendImplementation() {
      window.sendTrackingEvent("Landing", "shareXP confirm", "")
      this.$store.dispatch("sendContributionInfo")
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
