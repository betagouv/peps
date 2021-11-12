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
          <div>
            <v-card-title>Partager une expérience</v-card-title>
            <v-card-text style="padding-bottom: 5px;">Avant de partager une expérience sur le site, nous avons besoin d'en savoir un peu plus sur vous.</v-card-text>
            <v-card-text style="padding-top: 0px; padding-bottom: 20px;">
              <v-container style="padding-top: 0px; padding-bottom: 0px;">
                <v-row>
                  <v-col cols="12" sm="5" :style="showBorder ? 'border-right: solid 1px #DDD;' : ''">
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
                  <v-col cols="12" sm="7" style="padding-left: 20px;">
                    <div class="subtitle-2">
                      Je continue sans compte
                    </div>
                    <div class="caption">
                      L'équipe Peps vous facilite la tâche pour que cela vous prenne le moins de
                      temps possible : après un court entretien téléphonique nous vous proposons
                      un brouillon que vous validez avant publication
                    </div>
                    <div>
                      <v-btn
                        style="margin-top: 5px;"
                        class="text-none practice-buttons"
                        color="primary"
                        v-on:click="goToShare"
                      >Commencer</v-btn>
                    </div>
                  </v-col>
                </v-row>
              </v-container>
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
import Constants from "@/constants"
import Loader from "@/components/Loader.vue"

export default {
  name: "ContributionOverlay",
  components: { Loader },
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
    showBorder() {
      return this.$vuetify.breakpoint.name != 'xs'
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
      window.sendTrackingEvent("Landing", "shareXP cancel", "")
      this.$emit("done")
    },
    onWindowResize() {
      this.windowHeight = window.innerHeight - 30
    },
    goToShare() {
      this.$router.push({
        name: "Share",
      })
      this.close()
    }
  },
  watch: {
    sendingError(value) {
      if (value && this.visible) {
        this.close()
      }
    }
  }
}
</script>
