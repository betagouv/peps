<template>
  <div>
    <v-card outlined color="#E0F4EE">
      <v-card-text class="subtitle-2">
        <v-icon color="amber">mdi-octagram</v-icon>Utilisateur admin
      </v-card-text>

      <v-container>
        <v-row>
          <v-col cols="12" sm="6" md="4">
            <v-card @click="updateXpData">
              <v-card-subtitle>
                <v-icon size="20" style="margin: 0px 5px 0 0;">mdi-beaker-outline</v-icon>Mettre à jour les données XP
              </v-card-subtitle>
            </v-card>
          </v-col>

          <v-col cols="12" sm="6" md="4">
            <v-card @click="updateFormData">
              <v-card-subtitle>
                <v-icon size="20" style="margin: 0px 5px 0 0;">mdi-format-list-checks</v-icon>Mettre à jour les données formulaire
              </v-card-subtitle>
            </v-card>
          </v-col>

          <v-col cols="12" sm="6" md="4">
            <v-card href="https://github.com/betagouv/peps" target="_blank">
              <v-card-subtitle>
                <v-icon size="20" style="margin: 0px 5px 0 0;">mdi-github</v-icon>Repo Github
              </v-card-subtitle>
            </v-card>
          </v-col>
        </v-row>
      </v-container>
    </v-card>

    <v-overlay :value="overlayVisible" :dark="false">
      <v-btn
        @click="overlayVisible = false"
        class="close-overlay"
        fab
        dark
        small
        v-if="!requestOngoing"
        color="grey lighten-5"
      >
        <v-icon color="red darken-3">mdi-close</v-icon>
      </v-btn>
      <v-card width="330">
        <v-card-title>{{ overlayTitle }}</v-card-title>
        <v-card-text>{{ overlayText }}</v-card-text>
        <v-card-text>
          <v-progress-linear height="16" :value="progress" rounded></v-progress-linear>
        </v-card-text>
        <v-card-text
          style="max-height: 250px; overflow-x: hidden; background: rgb(225, 225, 225) none repeat scroll 0% 0%;overflow-y: scroll;"
        >
          <v-card
            outlined
            :href="issue.url"
            target="__blank"
            v-for="(issue, index) in overlayIssues"
            :key="index"
            style="margin-bottom: 10px;"
            :color="issue.fatal ? 'red lighten-5' : 'amber lighten-5'"
          >
            <v-card-text>
              <v-icon v-if="issue.fatal" color="red">mdi-skull-crossbones</v-icon>
              <v-icon v-else color="amber">mdi-alert</v-icon>
              {{ issue.message }}
            </v-card-text>
          </v-card>
        </v-card-text>
      </v-card>
    </v-overlay>
  </div>
</template>

<script>
import Constants from "@/constants"

const headers = {
  "X-CSRFToken": window.CSRF_TOKEN || "",
  "Content-Type": "application/json"
}

export default {
  name: "AdminCard",
  data() {
    return {
      xpRefreshStatus: Constants.LoadingStatus.IDLE,
      formRefreshStatus: Constants.LoadingStatus.IDLE,
      overlayVisible: false,
      overlayTitle: "",
      overlayText: "",
      overlayIssues: [],
      progress: 0,
      interval: null,
      iterations: 0
    }
  },
  computed: {
    requestOngoing() {
      return !!this.interval
    }
  },
  methods: {
    updateXpData() {
      this.updateData("Mise à jour des données XP", "/api/v1/refreshXPData")
    },
    updateFormData() {
      this.updateData(
        "Mise à jour des données Formulaire",
        "/api/v1/refreshData"
      )
    },
    updateData(title, url) {
      if (this.overlayVisible) return
      this.overlayIssues = []
      this.overlayTitle = title
      this.overlayText = "Obtention des données Airtable"
      this.overlayVisible = true
      this.startProgressBar()
      this.$http
        .post(url, {}, { headers })
        .then(response => {
          this.endProgressBar(true)
          this.overlayText = response.body.success
            ? "✔ Données à jour"
            : "✖ La mise à jour des données a échoué"
          this.overlayIssues = response.body.errors
        })
        .catch(() => {
          this.endProgressBar(false)
          this.overlayText =
            "Il y a eu une erreur en mettant à jour les données Airtable"
        })
    },
    startProgressBar() {
      if (this.interval) this.endProgressBar(false)
      this.progress = 0
      this.interval = setInterval(() => {
        this.progress += 1 / 4
      }, 0 + (Math.random() * (200 - 0)))
    },
    endProgressBar(success) {
      if (this.interval) window.clearInterval(this.interval)
      this.interval = null
      this.progress = success ? 100 : 0
    }
  }
}
</script>