<template>
  <div>
    <Title :title="title" :breadcrumbs="breadcrumbs" />
    <v-container class="constrained">
      <div>
        <div class="display-1 primary--text">{{ displayName }}</div>
      </div>

      <AdminCard v-if="loggedUser && !!loggedUser.is_superuser" />

      <div class="title" style="margin-top: 20px;">
        <span>Mes informations</span>
        <v-btn class="text-none" small fab style="margin-left: 15px; margin-top: -5px;">
          <v-icon>mdi-pencil</v-icon>
        </v-btn>
      </div>

      <div v-if="farmer">
        <div style="margin-top: 0px;">
          <v-icon style="margin-top: -2px; margin-right: 3px;" small>mdi-account</v-icon>
          <span class="subtitle-2" style="margin-right: 10px;">Nom</span>
          <span class="body-2">{{farmer.name}}</span>
        </div>
        <div style="margin-top: 0px;">
          <v-icon style="margin-top: -2px; margin-right: 3px;" small>mdi-leaf</v-icon>
          <span class="subtitle-2" style="margin-right: 10px;">Cultures</span>
          <span class="body-2">{{farmer.cultures || 'Nous ne connaissons pas vos cultures'}}</span>
        </div>
        <div style="margin-top: 0px;">
          <v-icon style="margin-top: -2px; margin-right: 3px;" small>mdi-tractor</v-icon>
          <span class="subtitle-2" style="margin-right: 10px;">Types d'agriculture</span>
          <span class="body-2" v-if="farmer.agriculture_types">
            <span
              v-for="(agricultureType, index) in farmer.agriculture_types"
              :key="index"
            >
              {{agricultureType}}
              <span
                v-if="farmer.agriculture_types.length > 1 && index < farmer.agriculture_types.length - 1"
              >,</span>
            </span>
          </span>
          <span v-else class="body-2">Nous ne connaissons pas votre type d'agriculture</span>
        </div>

      <div style="margin-top: 0px;">
          <v-icon style="margin-top: -2px; margin-right: 3px;" small>mdi-account-group</v-icon>
          <span class="subtitle-2" style="margin-right: 10px;">Groupes</span>
          <span class="body-2" v-if="farmer.groups">
            <span v-for="(group, index) in farmer.groups" :key="index">
              {{group}}
              <span v-if="farmer.groups.length > 1 && index < farmer.groups.length - 1">,</span>
            </span>
          </span>
          <span v-else class="body-2">Nous ne connaissons pas les groupes dont vous faites partie</span>
        </div>
      </div>

      <div v-else>Il nous manquent quelques informations sur vous</div>

      <div class="title" style="margin-top: 20px;">Mes expérimentations</div>

      <v-row v-if="farmer && farmer.experiments && farmer.experiments.length > 0">
        <v-col
          v-for="(experiment, index) in farmer.experiments"
          :key="index"
          cols="12"
          sm="6"
          md="4"
        >
        <v-btn class="text-none" small fab style="position: relative; z-index: 9; top: 15px;">
          <v-icon>mdi-pencil</v-icon>
        </v-btn>
          <ExperimentCard :experiment="experiment" />
        </v-col>
      </v-row>

      <div v-else>Vous n'avez pas d'expérimentations</div>
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
          text: "Carte des expérimentations",
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
      if (!this.loggedUser || !this.loggedUser.farmer_external_id) return null
      return this.$store.getters.farmerWithExternalId(
        this.loggedUser.farmer_external_id
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
