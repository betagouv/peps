<template>
  <div>
    <Title :title="title" :breadcrumbs="breadcrumbs" />
    <Loader
      v-if="!userDataReady"
      title="Chargement en cours"
      text="Juste un instant s'il vous plaît."
    />
    <v-container v-else class="constrained">
      <AdminCard v-if="loggedUser && !!loggedUser.is_superuser" />

      <!-- PROFILE -->
      <div v-if="!!farmer">
        <v-list-item class="flex-fix-item pa-0" style="margin: 5px 0 0px 0;">
          <v-list-item-avatar :size="80" color="grey" style="margin-right: 10px; margin-top: 10px;">
            <v-img :src="farmer.profile_image" v-if="farmer.profile_image"></v-img>
            <v-icon v-else>mdi-account</v-icon>
          </v-list-item-avatar>
          <v-list-item-content>
            <v-list-item-title
              class="title"
              style="padding-left: 3px; margin-bottom: 0; margin-top: 0;"
            >{{ farmer.name }}</v-list-item-title>
            <v-list-item style="padding-left: 3px;">
              <v-btn
                outlined
                color="primary"
                class="text-none"
                style="margin-top: 0px; margin-right: 10px;"
                @click="editFarmer"
              >
                <v-icon style="margin-right: 10px;">mdi-account</v-icon>Modifier mon profil
              </v-btn>

              <v-btn
                outlined
                color="primary"
                class="text-none"
                style="margin-top: 0px;"
                @click="createXP"
              >
                <v-icon style="margin-right: 10px;">mdi-beaker-plus-outline</v-icon>Partager une nouvelle expérience
              </v-btn>
            </v-list-item>
          </v-list-item-content>
        </v-list-item>

        <v-alert dense text v-if="!farmer.approved" border="left" type="warning" class="body-2">
          <span style="color: #333 !important;">
            Votre profil est en attente de validation par notre équipe et il sera mis en ligne une fois approuvé.
            Vous pouvez toutefois le modifier et rédiger des expériences à partager dès à présent.
          </span>
        </v-alert>

        <FarmerInfoBox :farmer="farmer" :compact="true" />
      </div>

      <!-- APPROVED EXPERIMENTS -->
      <div v-if="farmer && approvedExperiments && approvedExperiments.length > 0">
        <v-divider style="margin-top: 30px;" />

        <div
          class="title"
          style="margin-top: 30px; margin-bottom: 0px;"
        >Mes retours d'expérience en ligne</div>

        <v-row>
          <v-col
            v-for="(experiment, index) in approvedExperiments"
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
      </div>

      <!-- APPROVED EXPERIMENTS -->
      <div v-else>
        <v-divider style="margin-top: 30px;" />
        <div
          class="title"
          style="margin-top: 30px; margin-bottom: 0px;"
        >Vous n'avez pas de retours d'expérience en ligne</div>
      </div>

      <!-- PENDING EXPERIMENTS -->
      <div v-if="pendingExperiments && pendingExperiments.length > 0">
        <v-divider style="margin-top: 30px;" />

        <div
          class="title"
          style="margin-top: 30px; margin-bottom: 0px;"
        >Mes retours d'expérience en attente de validation</div>

        <div
          class="body-2"
          style="margin-top: 0px; margin-bottom: 0px;"
        >Notre équipe validera bientôt les retours d'expérience ci-dessous.</div>

        <v-row>
          <v-col
            v-for="(experiment, index) in pendingExperiments"
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
            <ExperimentCard :experiment="experiment" :disabled="true" :elevation="0" />
          </v-col>
        </v-row>
      </div>
    </v-container>
  </div>
</template>

<script>
import Title from "@/components/Title.vue"
import ExperimentCard from "@/components/ExperimentCard.vue"
import AdminCard from "@/components/AdminCard.vue"
import FarmerInfoBox from "@/components/FarmerInfoBox"
import Loader from "@/components/Loader"
import Constants from "@/constants"

export default {
  name: "Profile",
  components: { Title, ExperimentCard, AdminCard, FarmerInfoBox, Loader },
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
    userDataReady() {
      return (
        this.$store.state.loggedUserLoadingStatus ===
          Constants.LoadingStatus.SUCCESS ||
        this.$store.state.loggedUserLoadingStatus ===
          Constants.LoadingStatus.ERROR
      )
    },
    loggedUser() {
      return this.$store.state.loggedUser
    },
    farmer() {
      if (!this.loggedUser || !this.loggedUser.farmer_id) return null
      return this.$store.getters.farmerWithId(this.loggedUser.farmer_id)
    },
    displayName() {
      if (!this.loggedUser) return ""
      if (this.farmer) return this.farmer.name
      if (this.loggedUser.first_name && this.loggedUser.first_name !== "")
        return this.loggedUser.first_name + " " + this.loggedUser.last_name
      if (this.loggedUser.username && this.loggedUser.username !== "")
        return this.loggedUser.username

      return this.loggedUser.email
    },
    pendingExperiments() {
      if (
        !this.farmer ||
        !this.farmer.experiments ||
        this.farmer.experiments.length === 0
      )
        return []
      return this.farmer.experiments.filter(x => !x.approved)
    },
    approvedExperiments() {
      if (
        !this.farmer ||
        !this.farmer.experiments ||
        this.farmer.experiments.length === 0
      )
        return []
      return this.farmer.experiments.filter(x => !!x.approved)
    }
  },
  methods: {
    editXP(xp) {
      let experimentUrlComponent = this.$store.getters.experimentUrlComponent(
        xp
      )
      window.sendTrackingEvent("Profile", "Edit XP", experimentUrlComponent)
      this.$router.push({
        name: "ExperimentEditor",
        query: { xp: experimentUrlComponent }
      })
    },
    createXP() {
      window.sendTrackingEvent(
        "Profile",
        "Create XP",
        "Partager une expérience"
      )
      this.$router.push({ name: "ExperimentEditor" })
    },
    editFarmer() {
      let farmerUrlComponent = this.$store.getters.farmerUrlComponent(
        this.farmer
      )
      window.sendTrackingEvent("Profile", "Edit Farmer", farmerUrlComponent)
      this.$router.push({
        name: "FarmerEditor",
        query: { agriculteur: farmerUrlComponent }
      })
    }
  },
  watch: {
    userDataReady(isReady) {
      if (isReady && !this.$store.state.loggedUser)
        this.$router.push({ name: 'Map' })
    }
  },
  mounted() {
    if (this.userDataReady && !this.$store.state.loggedUser)
      this.$router.push({ name: 'Map' })
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
