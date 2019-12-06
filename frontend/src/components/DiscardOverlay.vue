<template>
  <div v-if="visible">
    <v-overlay :value="visible" :dark="false">
      <v-btn @click="close()" class="close-overlay" fab dark small color="grey lighten-5">
        <v-icon color="red darken-3">mdi-close</v-icon>
      </v-btn>
      <v-card
        :style="'margin-left: 10px; margin-right: 10px; max-width: 600px; max-height:' + windowHeight + 'px'"
        class="overflow-y-auto"
      >
        <v-card-title>Cette pratique n'est pas pertinente ?</v-card-title>
        <v-card-text>
          <v-radio-group v-model="selected" :mandatory="false">
            <v-radio
              v-for="item in radioItems"
              :key="item.value"
              :label="item.text"
              :value="item.value"
              color="primary"
            ></v-radio>
          </v-radio-group>

          <div style="padding-right: 10px; text-align: right">
            <v-btn class="text-none body-1 practice-buttons" @click="close()" rounded>Annuler</v-btn>
            <v-btn
              class="text-none body-1 practice-buttons"
              color="primary"
              @click="discardPractice()"
              :disabled="!selected"
              rounded
            >Confirmer</v-btn>
          </div>
        </v-card-text>
      </v-card>
    </v-overlay>
  </div>
</template>

<script>
export default {
  name: "DiscardOverlay",
  data: () => ({
    windowHeight: window.innerHeight - 30,
    radioItems: [
      {
        value: "J'ai déjà prévu de mettre en place cette pratique",
        text: "J'ai déjà prévu de mettre en place cette pratique"
      },
      {
        value:
          "Cette pratique a été testée ou est en place sur mon exploitation",
        text: "Cette pratique a été testée ou est en place sur mon exploitation"
      },
      {
        value: "Cette pratique n’est pas applicable pour mon exploitation",
        text: "Cette pratique n’est pas applicable pour mon exploitation"
      },
      {
        value: "Autre",
        text: "Autre"
      }
    ],
    selected: undefined
  }),
  props: {
    practice: {
      type: Object
    }
  },
  computed: {
    visible() {
      return !!this.practice && Object.keys(this.practice).length > 0
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
      this.$ga.event('Practice', 'blacklist cancel', this.practice.title)
      this.$emit("done")
    },
    discardPractice() {
      this.$emit("done")
      this.$ga.event('Practice', 'blacklist confirm', this.practice.title)
      this.$store.dispatch("blacklistPractice", { practice: this.practice })
      this.sendDiscardAction()
    },
    onWindowResize() {
      this.windowHeight = window.innerHeight - 30
    },
    sendDiscardAction() {
      if (!this.practice)
        return
      const payload = {
        practice_airtable_id: this.practice.external_id,
        reason: this.selected || "Autre"
      }
      const headers = {
        "X-CSRFToken": window.CSRF_TOKEN || "",
        "Content-Type": "application/json"
      }
      this.$http.post("api/v1/discardAction", payload, { headers })
    }
  }
}
</script>
