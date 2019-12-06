<template>
  <div v-if="visible">
    <Loader v-if="!!sendingInProgress" title="Juste un instant..." />

    <v-overlay :value="visible" :dark="false">
      <div v-if="sendingIdle">
        <v-btn @click="cancelImplementation()" class="close-overlay" fab dark small color="grey lighten-5">
          <v-icon color="red darken-3">mdi-close</v-icon>
        </v-btn>
        <v-card
          :style="'margin-left: 10px; margin-right: 10px; max-width: 600px; max-height:' + windowHeight + 'px'"
          class="overflow-y-auto"
        >
          <v-card-text style="padding-bottom: 0; color: #333;">
            Quelles informations ou actions vous semblent nécessaires afin de vous
            décider sur le test de cette pratique ?
            (il est possible de sélectionner plusieurs items) :
          </v-card-text>
          <Form
            style="margin-bottom: 0px;"
            :elevation="0"
            :schema="reasonsSchema"
            :options="reasonsOptions"
            updateActionName="addImplementationFormData"
            storeDataName="implementationFormData"
          />
          <v-card-text
            style="padding-top: 0; padding-bottom: 0; color: #333;"
          >Ces informations nous permettront d'aller plus loin dans la compréhension des freins à la mise en place de pratiques alternatives. Pouvons-nous vous contacter afin d'approfondir ces sujets avec vous ?</v-card-text>
          <Form
            style="margin-bottom: 0px;"
            :elevation="0"
            :schema="contactSchema"
            :options="contactOptions"
            updateActionName="addContactFormData"
            storeDataName="contactFormData"
          />
          <div style="padding-right: 10px; text-align: right">
            <v-btn class="text-none body-1 practice-buttons" @click="cancelImplementation()" rounded>Annuler</v-btn>
            <v-btn
              class="text-none body-1 practice-buttons"
              color="primary"
              :disabled="!complete"
              @click="sendImplementation()"
              rounded
            >Confirmer</v-btn>
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
          <v-card-text style="padding-top: 30px; color: #333;">
            Merci ! Notre équipe vous contactera bientôt
          </v-card-text>
          <div style="padding-right: 10px; text-align: right">
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
import Form from "@/components/forms/Form.vue"
import formutils from "@/formutils"
import Constants from '@/constants'
import Loader from "@/components/Loader.vue";

export default {
  name: "ImplementationOverlay",
  components: { Form, Loader },
  data: () => ({
    windowHeight: window.innerHeight - 30,
    reasonsSchema: {
      type: "object",
      properties: {
        implementationReason: {
          required: false
        }
      }
    },
    reasonsOptions: {
      fields: {
        implementationReason: {
          hideNone: true,
          sort: false,
          type: "checkbox",
          multiple: true,
          dataSource: [
            {
              text: "Échanger avec un conseiller",
              value: "Échanger avec un conseiller"
            },
            {
              text:
                "Avoir le retour d'expérience d'un agriculteur l'ayant déjà mis en place",
              value:
                "Avoir le retour d'expérience d'un agriculteur l'ayant déjà mis en place"
            },
            {
              text:
                "Obtenir plus de documentation technique et un protocole de test",
              value:
                "Obtenir plus de documentation technique et un protocole de test"
            },
            {
              text: "Connaitre les aides disponibles pour cette pratique",
              value: "Connaitre les aides disponibles pour cette pratique"
            },
            {
              text: "Connaitre les cahiers des charges incluant cette pratique",
              value: "Connaitre les cahiers des charges incluant cette pratique"
            },
            {
              text: "Avoir une estimation du risque économique pris",
              value: "Avoir une estimation du risque économique pris"
            },
            {
              text: "Connaitre le matériel nécessaire et disponible",
              value: "Connaitre le matériel nécessaire et disponible"
            },
            {
              text: "Autre",
              value: "Autre"
            }
          ]
        },
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
    },
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
    },
  }),
  props: {
    practice: {
      type: Object
    }
  },
  computed: {
    visible() {
      return !!this.practice && Object.keys(this.practice).length > 0
    },
    sendingIdle() {
      return this.$store.state.implementationLoadingStatus ===
        Constants.LoadingStatus.IDLE
    },
    sendingInProgress() {
      return this.$store.state.implementationLoadingStatus ===
        Constants.LoadingStatus.LOADING
    },
    sendingSucceeded() {
      return this.$store.state.implementationLoadingStatus ===
        Constants.LoadingStatus.SUCCESS
    },
    sendingError() {
      return this.$store.state.implementationLoadingStatus ===
        Constants.LoadingStatus.ERROR
    },
    complete() {
      const reasonComplete = formutils.formIsComplete(
        this.reasonsSchema,
        this.reasonsOptions,
        this.$store.state.implementationFormData
      )
      const contactComplete = formutils.formIsComplete(
        this.contactSchema,
        this.contactOptions,
        this.$store.state.contactFormData
      )
      return reasonComplete && contactComplete
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
      this.$store.dispatch("resetImplementationForm")
      this.$emit("done")
    },
    cancelImplementation() {
      this.$ga.event('Practice', 'try cancel', this.practice.title)
      this.$store.dispatch("resetImplementationForm")
      this.$emit("done")
    },
    sendImplementation() {
      this.$ga.event('Practice', 'try confirm', this.practice.title)
      this.$store.dispatch("sendImplementation", { practice: this.practice })
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

<style>
.close-overlay {
  position: absolute;
  right: -10px;
  top: -20px;
  z-index: 5;
}
</style>