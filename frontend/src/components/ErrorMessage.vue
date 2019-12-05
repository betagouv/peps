<template>
  <div v-if="visible">
    <v-overlay :value="visible" :dark="false">
      <v-card
        style="margin-left: 10px; margin-right: 10px; max-width: 600px;"
        class="overflow-y-auto"
      >
        <v-card-title>{{ title }}</v-card-title>
        <v-card-text>
          {{ body }}

          <div style="margin-top: 20px; padding-right: 10px; text-align: right">
            <v-btn class="text-none body-1 practice-buttons" @click="reload()" rounded>Recharger la page</v-btn>
            <v-btn
              v-if="onRetry"
              class="text-none body-1 practice-buttons"
              color="primary"
              @click="onRetry()"
              rounded
            >Ressayer</v-btn>
          </div>
        </v-card-text>
      </v-card>
    </v-overlay>
  </div>
</template>

<script>
export default {
  name: "ErrorMessage",
  props: {
    onRetry: {
      type: Function
    },
    title: {
      type: String,
      default: "Oups ! Une erreur est survenue"
    },
    body: {
      type: String,
      default: "Veuillez réessayer plus tard"
    },
    visible: {
      type: Boolean,
      required: true,
    }
  },
  methods: {
    reload() {
      location.reload()
    }
  }
}
</script>
