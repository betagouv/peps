<template>
  <div>
    <Title :title="title" :breadcrumbs="breadcrumbs" />
    <v-container class="constrained">
      <div>
        <div class="display-1 primary--text">{{ displayName }}</div>
      </div>

      <AdminCard v-if="loggedUser && !!loggedUser.is_superuser" />

      <v-btn class="text-none" style="margin-top: 10px;" v-if="!!farmer" @click="createXP">
        <v-icon style="margin-right: 10px;">mdi-beaker-plus-outline</v-icon>Partager une nouvelle expérience
      </v-btn>

      <div class="title" style="margin-top: 30px; margin-bottom: 0px;">Mes retours d'expérience</div>

      <v-row v-if="farmer && farmer.experiments && farmer.experiments.length > 0">
        <v-col
          v-for="(experiment, index) in farmer.experiments"
          :key="index"
          cols="12"
          sm="6"
          md="4"
        >
          <v-btn
            @click="editXP(experiment)"
            class="text-none"
            small
            fab
            style="position: relative; z-index: 9; top: 15px;"
          >
            <v-icon>mdi-pencil</v-icon>
          </v-btn>
          <ExperimentCard :experiment="experiment" />
        </v-col>
      </v-row>

      <div class="title" v-if="farmer && farmer.pending_experiments && farmer.pending_experiments.length > 0" style="margin-top: 30px; margin-bottom: 0px;">En attente de validation</div>

      <div class="body-2" v-if="farmer && farmer.pending_experiments && farmer.pending_experiments.length > 0" style="margin-top: 0px; margin-bottom: 0px;">
        Notre équipe validera bientôt les retours d'expérience ci-dessous.
      </div>


      <v-row v-if="farmer && farmer.pending_experiments && farmer.pending_experiments.length > 0">
        <v-col
          v-for="(experiment, index) in farmer.pending_experiments"
          :key="index"
          cols="12"
          sm="6"
          md="4"
        >
          <ExperimentCard :experiment="experiment" :disabled="true" :elevation="0" />
        </v-col>
      </v-row>
    </v-container>
  </div>
</template>

<script>
import Title from "@/components/Title.vue"
import ExperimentCard from "@/components/ExperimentCard.vue"
import AdminCard from "@/components/AdminCard.vue"

export default {
  name: "Profile",
  components: { Title, ExperimentCard, AdminCard },
  data() {
    return {
      title: "Mon compte",
      breadcrumbs: [
        {
          text: "Carte de retours d'expérience",
          disabled: false,
          href: "/#/map"
        },
        {
          text: "Mon compte",
          disabled: true
        }
      ]
    }
  },
  computed: {
    loggedUser() {
      return this.$store.state.loggedUser
    },
    farmer() {
      if (!this.loggedUser || !this.loggedUser.farmer_id) return null
      return this.$store.getters.farmerWithId(
        this.loggedUser.farmer_id
      )
    },
    displayName() {
      if (!this.loggedUser) return ""
      if (this.farmer) return this.farmer.name
      if (this.loggedUser.first_name && this.loggedUser.first_name !== "")
        return this.loggedUser.first_name + " " + this.loggedUser.last_name
      if (this.loggedUser.username && this.loggedUser.username !== "")
        return this.loggedUser.username

      return this.loggedUser.email
    }
  },
  methods: {
    editXP(xp) {
      window.sendTrackingEvent("Profile", "Edit XP", xp.name)
      this.$router.push({ name: "ExperimentEditor", query: { xp: xp.name } })
    },
    createXP() {
      window.sendTrackingEvent(
        "Profile",
        "Create XP",
        "Partager une expérience"
      )
      this.$router.push({ name: "ExperimentEditor" })
    }
  }
}
</script>

<style scoped>
.theme--light.v-card > .v-card__subtitle,
.theme--light.v-card > .v-card__text {
  color: rgba(0, 0, 0, 0.87);
}
.display-1 {
  margin-top: 25px;
  margin-bottom: 10px;
}
.title {
  margin-top: 10px;
  margin-bottom: 5px;
}
.body-2 {
  line-height: 1.375rem;
}
</style>
