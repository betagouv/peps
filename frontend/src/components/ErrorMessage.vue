<template>
  <div v-if="visible">
    <v-overlay :value="visible" :dark="false">
      <v-btn 
        @click="close()"
        class="close-overlay"
        fab
        dark
        small
        color="grey lighten-5"
        v-if="this.showCloseButton"
      >
        <v-icon color="red darken-3">mdi-close</v-icon>
      </v-btn>
      <v-card
        style="margin-left: 10px; margin-right: 10px; max-width: 600px; max-height: 80vh;"
        class="overflow-y-auto"
      >
        <v-card-title>{{ title }}</v-card-title>
        <v-card-text>
          {{ body }}

          <div style="margin-top: 20px; padding-right: 10px; text-align: right" v-if="this.ctaText && this.ctaAction">
            <v-btn class="text-none body-1 practice-buttons" @click="ctaAction()" rounded>{{ this.ctaText }}</v-btn>
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
    },
    ctaText: {
      type: String,
    },
    ctaAction: {
      type: Function,
    },
    showCloseButton: {
      type: Boolean,
      default: true
    }
  },
  methods: {
    close() {
      this.$emit("done")
    },
  }
}
</script>
