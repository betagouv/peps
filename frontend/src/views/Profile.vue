<template>
  <div>
    <Title :title="title" :breadcrumbs="breadcrumbs" />
    <Loader
      v-if="!userDataReady"
      title="Chargement en cours"
      text="Juste un instant s'il vous plaît."
    />
    <v-container v-else class="constrained">
      <!-- <AdminCard v-if="loggedUser && !!loggedUser.is_superuser" /> -->

      <div class="ma-0" v-if="farmer">
        <!-- PROFILE CARD -->
        <v-row>
          <v-col cols="12" md="8">
            <v-card outlined class="d-flex align-center pa-3">
              <div class="d-none d-sm-flex" style="margin-right: 20px;">
                <v-avatar color="grey" size="70">
                  <v-img :src="farmer.profile_image" v-if="farmer.profile_image"></v-img>
                  <v-icon v-else>mdi-account</v-icon>
                </v-avatar>
              </div>
              <div style="margin-right: 20px;" class="d-flex flex-column flex-grow-1">
                <v-card-title class="ma-0 pa-0">{{displayName}}</v-card-title>
                <div>{{farmer.email}}</div>
              </div>
              <v-btn
                text
                class="text-none"
                color="primary"
                style="text-decoration: underline;"
                v-if="farmer.approved"
                @click="seePublicProfile"
              >Voir le profil public</v-btn>
              <v-btn text class="text-none" color="grey-darken-2" v-else disabled>Profil non publié</v-btn>
            </v-card>
          </v-col>
        </v-row>

        <v-row>
          <!-- INFORMATIONS PERSONNELLES -->
          <v-col cols="12" sm="6" md="4" style="min-height: 180px;">
            <v-hover>
              <v-card
                class="fill-height"
                @click="editPersonalInformation"
                slot-scope="{ hover }"
                :elevation="hover ? 4 : 2"
              >
                <v-card-title>
                  Informations Personnelles
                  <v-icon
                    small
                    color="#333"
                    style="margin-top: 3px; margin-left: 5px;"
                  >mdi-chevron-right</v-icon>
                </v-card-title>
                <v-card-subtitle>Modifiez vos données et informations de contact</v-card-subtitle>
              </v-card>
            </v-hover>
          </v-col>

          <!-- EXPLOITATION -->
          <v-col cols="12" sm="6" md="4" style="min-height: 180px;">
            <v-hover>
              <v-card
                outlined
                class="fill-height d-flex flex-column"
                @click="editFarm"
                slot-scope="{ hover }"
                :elevation="hover ? 4 : 2"
              >
                <v-card-title>
                  Exploitation
                  <v-icon
                    small
                    color="#333"
                    style="margin-top: 3px; margin-left: 5px;"
                  >mdi-chevron-right</v-icon>
                </v-card-title>
                <v-card-subtitle
                  class="flex-grow-1"
                >Mettez à jour le descriptif de votre exploitation et sa philosophie</v-card-subtitle>
                <v-card-text v-if="!farmer.approved">
                  <v-chip small outlined color="amber darken-2">
                    <v-icon small style="margin-right: 5px;">mdi-clock-outline</v-icon>En attente de validation
                  </v-chip>
                </v-card-text>
              </v-card>
            </v-hover>
          </v-col>

          <!-- ABONNEMENTS ET NOTIFICATIONS -->
          <!-- <v-col cols="12" sm="6" md="4" style="min-height: 180px;">
            <v-hover>
              <v-card
                outlined
                class="fill-height"
                slot-scope="{ hover }"
                :elevation="hover ? 4 : 2"
              >
                <v-card-title>
                  Abonnements et notifications
                  <v-icon
                    small
                    color="#333"
                    style="margin-top: 3px; margin-left: 5px;"
                  >mdi-chevron-right</v-icon>
                </v-card-title>
                <v-card-subtitle>Reglez vos préférences de notifications et la manière d'être contacté</v-card-subtitle>
              </v-card>
            </v-hover>
          </v-col>-->
        </v-row>

        <v-row>
          <!-- RETOURS D'EXPÉRIENCE APPROUVÉS -->
          <v-col
            cols="12"
            sm="6"
            md="4"
            v-for="experiment in approvedExperiments"
            :key="experiment.id"
            style="min-height: 180px;"
          >
            <v-hover>
              <v-card
                outlined
                class="fill-height d-flex flex-column"
                @click="goToExperiment(experiment)"
                slot-scope="{ hover }"
                :elevation="hover ? 4 : 2"
              >
                <v-card-title>
                  Retour d'expérience
                  <v-icon
                    small
                    color="#333"
                    style="margin-top: 3px; margin-left: 5px;"
                  >mdi-chevron-right</v-icon>
                </v-card-title>
                <v-card-subtitle class="flex-grow-1">{{ experiment.name }}</v-card-subtitle>
                <v-card-text>
                  <v-chip small outlined color="primary">
                    <v-icon small style="margin-right: 5px;">mdi-check</v-icon>En ligne
                  </v-chip>
                </v-card-text>
              </v-card>
            </v-hover>
          </v-col>

          <!-- RETOURS D'EXPÉRIENCE EN ATTENTE -->
          <v-col
            cols="12"
            sm="6"
            md="4"
            v-for="experiment in pendingExperiments"
            :key="experiment.id"
            style="min-height: 180px;"
          >
            <v-hover>
              <v-card
                outlined
                class="d-flex flex-column fill-height"
                @click="goToExperiment(experiment)"
                slot-scope="{ hover }"
                :elevation="hover ? 4 : 2"
              >
                <v-card-title>
                  Retour d'expérience
                  <v-icon
                    small
                    color="#333"
                    style="margin-top: 3px; margin-left: 5px;"
                  >mdi-chevron-right</v-icon>
                </v-card-title>
                <v-card-subtitle class="flex-grow-1">{{ experiment.name }}</v-card-subtitle>
                <v-card-text>
                  <v-chip small outlined color="amber darken-2">
                    <v-icon small style="margin-right: 5px;">mdi-clock-outline</v-icon>En attente de validation
                  </v-chip>
                </v-card-text>
              </v-card>
            </v-hover>
          </v-col>

          <!-- RETOURS D'EXPÉRIENCE EN BROUILLON -->
          <v-col
            cols="12"
            sm="6"
            md="4"
            v-for="experiment in draftExperiments"
            :key="experiment.id"
            style="min-height: 180px;"
          >
            <v-hover>
              <v-card
                outlined
                class="d-flex flex-column fill-height"
                @click="goToExperiment(experiment)"
                slot-scope="{ hover }"
                :elevation="hover ? 4 : 2"
              >
                <v-card-title>
                  Retour d'expérience
                  <v-icon
                    small
                    color="#333"
                    style="margin-top: 3px; margin-left: 5px;"
                  >mdi-chevron-right</v-icon>
                </v-card-title>
                <v-card-subtitle class="flex-grow-1">{{ experiment.name }}</v-card-subtitle>
                <v-card-text>
                  <v-chip small outlined color="blue-grey darken-2">
                    <v-icon small style="margin-right: 5px;">mdi-lead-pencil</v-icon>Brouillon
                  </v-chip>
                </v-card-text>
              </v-card>
            </v-hover>
          </v-col>

          <!-- AJOUTER UNE XP -->
          <v-col cols="12" sm="6" md="4" style="min-height: 180px;">
            <v-hover>
              <v-card
                outlined
                color="#E0F4EE"
                class="fill-height d-flex"
                @click="createXP"
                slot-scope="{ hover }"
                :elevation="hover ? 4 : 2"
              >
                <v-card-title class="align-center">
                  <v-avatar style="margin-right: 5px;" size="40" color="primary">
                    <v-icon color="white">mdi-beaker-plus-outline</v-icon>
                  </v-avatar>Ajouter une expérience
                </v-card-title>
              </v-card>
            </v-hover>
          </v-col>
        </v-row>

        <v-row>
          <!-- MESSAGES -->
          <v-col cols="12" sm="6" md="4" style="min-height: 180px;">
            <v-hover>
              <v-card
                outlined
                class="fill-height"
                @click="goToMessages"
                slot-scope="{ hover }"
                :elevation="hover ? 4 : 2"
              >
                
                <v-card-title>
                  Messages
                  <span v-if="unreadMessageCount > 0" style="margin-left: 5px;">({{unreadMessageCount}})</span>
                  <v-icon
                    small
                    color="#333"
                    style="margin-top: 3px; margin-left: 5px;"
                  >mdi-chevron-right</v-icon>
                  <v-badge
                  dot
                  v-if="unreadMessageCount > 0"
                  color="amber"
                  style="position: absolute;top: 13px;left: 7px;"
                ></v-badge>
                </v-card-title>

                <v-card-subtitle v-if="unreadMessageCount > 0">Accèder à votre messagerie</v-card-subtitle>
                <v-card-subtitle v-else>Vous n'avez pas de nouveaux messages</v-card-subtitle>
              </v-card>
            </v-hover>
          </v-col>

          <!-- AIDE -->
          <v-col cols="12" sm="6" md="4" style="min-height: 180px;">
            <v-hover>
              <v-card
                outlined
                @click="goToHelp"
                class="fill-height"
                slot-scope="{ hover }"
                :elevation="hover ? 4 : 2"
              >
                <v-card-title>
                  Aide
                  <v-icon
                    small
                    color="#333"
                    style="margin-top: 3px; margin-left: 5px;"
                  >mdi-chevron-right</v-icon>
                </v-card-title>
                <v-card-subtitle>Vous trouverez tous les articles d'aide, les ressources et les conseils sur le site Peps</v-card-subtitle>
              </v-card>
            </v-hover>
          </v-col>
        </v-row>
      </div>
      <v-btn
        @click="logout"
        style="margin-top: 20px;"
        outlined
        color="deep-orange darken-4"
        class="text-none"
      >Se déconnecter</v-btn>
    </v-container>
  </div>
</template>

<script>
import Title from "@/components/Title.vue"
import Loader from "@/components/Loader"
import Constants from "@/constants"

export default {
  name: "Profile",
  components: { Title, Loader },
  metaInfo() {
    return {
      title: "Peps - Profil utilisateur",
      meta: [
        {
          description:
            "Modifiez et ajoutez des informations sur votre profil, vos retours d'expériences, vos préférences",
        },
      ],
    }
  },
  data() {
    return {
      title: "Mon compte",
      breadcrumbs: [
        {
          text: "Accueil",
          disabled: false,
          to: { name: "Landing" },
        },
        {
          text: "Mon compte",
          disabled: true,
        },
      ],
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
    approvedExperiments() {
      if (
        !this.farmer ||
        !this.farmer.experiments ||
        this.farmer.experiments.length === 0
      )
        return []
      return this.farmer.experiments.filter((x) => x.state === 'Validé')
    },
    pendingExperiments() {
      if (
        !this.farmer ||
        !this.farmer.experiments ||
        this.farmer.experiments.length === 0
      )
        return []
      return this.farmer.experiments.filter((x) => x.state === 'En attente de validation')
    },
    draftExperiments() {
      if (
        !this.farmer ||
        !this.farmer.experiments ||
        this.farmer.experiments.length === 0
      )
        return []
      return this.farmer.experiments.filter((x) => x.state === 'Brouillon')
    },
    unreadMessageCount() {
      return this.$store.getters.unreadMessageCount
    },
  },
  methods: {
    goToExperiment(xp) {
      let experimentUrlComponent = this.$store.getters.experimentUrlComponent(
        xp
      )
      window.sendTrackingEvent("Profile", "Edit XP", experimentUrlComponent)
      this.$router.push({
        name: "ExperimentEditor",
        query: { xp: experimentUrlComponent },
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
    editPersonalInformation() {
      let farmerUrlComponent = this.$store.getters.farmerUrlComponent(
        this.farmer
      )
      window.sendTrackingEvent(
        "Profile",
        "Edit Personal Info",
        farmerUrlComponent
      )
      this.$router.push({
        name: "PersonalInfoEditor",
        query: { agriculteur: farmerUrlComponent },
      })
    },
    editFarm() {
      let farmerUrlComponent = this.$store.getters.farmerUrlComponent(
        this.farmer
      )
      window.sendTrackingEvent("Profile", "Edit Farmer", farmerUrlComponent)
      this.$router.push({
        name: "FarmEditor",
        query: { agriculteur: farmerUrlComponent },
      })
    },
    goToHelp() {
      window.sendTrackingEvent("Profile", "Aide", "Aide")
      window.location.href = "https://aide.peps.beta.gouv.fr/"
    },
    goToMessages() {
      window.sendTrackingEvent("Profile", "Messages", this.loggedUser.email)
      this.$router.push({
        name: "Messages",
      })
    },
    logout() {
      if (window.confirm("Êtes-vous sur de vouloir fermer votre session ?")) {
        window.sendTrackingEvent("Profile", "Logout", "logout")
        window.location.href = "/logout"
      }
    },
    seePublicProfile() {
      window.sendTrackingEvent(
        "Profile",
        "Profile public",
        "Voir le profil public"
      )
      this.$router.push({
        name: "Farmer",
        params: {
          farmerUrlComponent: this.$store.getters.farmerUrlComponent(
            this.farmer
          ),
        },
      })
    },
  },
  watch: {
    userDataReady(isReady) {
      if (isReady && !this.$store.state.loggedUser)
        this.$router.push({ name: "Landing" })
    },
  },
  mounted() {
    if (this.userDataReady && !this.$store.state.loggedUser)
      this.$router.push({ name: "Landing" })
  },
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
.v-card__title {
  font-size: 1.1rem;
}
</style>
