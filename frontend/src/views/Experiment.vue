<template>
  <div>
    <Title :title="experiment.name" :breadcrumbs="breadcrumbs" />
    <v-container class="constrained" style="padding-top: 0px;">
      <v-img
        class="white--text align-end"
        height="110px"
        style="background: #CCC;"
        :src="farmer.backgroundPhoto"
      />

      <div class="display-1" style="margin-top: 20px;">{{ experiment.name }}</div>
      <div style="padding: 0 16px 0 16px;">
        <div class="ma-2" v-for="(iconInfo, index) in icons" :key="index">
          <v-icon left>{{iconInfo.icon}}</v-icon>
          <span class="capitalize">{{iconInfo.text}}</span>
        </div>
      </div>
      <v-divider style="margin-top: 10px; margin-bottom: -10px;" />
      <FarmerListItem :farmer="farmer" />
      <v-divider style="margin-top: 10px;" />
      <div class="subtitle-2" style="margin-top: 20px;">Objectifs</div>
      <div class="body-2" style="margin-top: 5px;">{{ experiment.objectives }}</div>
      <div class="body-2 practice-description" style="margin-top: 15px;">
        <div
          class="pa-0 fill-height"
          style="margin-bottom: 5px;"
          outlined
          v-for="(step, index) in (experiment.stages || [])"
          :key="index"
        >
          <div class="subtitle-2">{{ index + 1 }}. {{ step.title }} ({{ step.schedule }})</div>
          <v-card-text>{{ step.description }}</v-card-text>
          <v-card-text>
            <v-row>
              <v-col v-for="(photo, index) in testImages" :key="index" class="d-flex child-flex" cols="6" sm="3">
                <v-card flat tile class="d-flex">
                  <v-img
                    :src="photo"
                    aspect-ratio="1"
                    class="grey lighten-2"
                  >
                  </v-img>
                </v-card>
              </v-col>
            </v-row>
          </v-card-text>
        </div>
      </div>
    </v-container>
  </div>
</template>

<script>
import Title from "@/components/Title.vue"
import FarmerListItem from "@/components/FarmerListItem.vue"

export default {
  name: "Experiment",
  components: { Title, FarmerListItem },
  data() {
    return {
      testImages: [
        'https://images.unsplash.com/12/green.jpg?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=1350&q=80',
        'https://images.unsplash.com/40/yIdlmSvfSZCyGkCkLt0P_lucaslof_2.jpg?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjExMDk0fQ&auto=format&fit=crop&w=500&q=60',
        'https://images.unsplash.com/photo-1464972377689-e7674c48d806?ixlib=rb-1.2.1&auto=format&fit=crop&w=500&q=60',
        'https://images.unsplash.com/photo-1436462020942-723a9ea097c7?ixlib=rb-1.2.1&auto=format&fit=crop&w=500&q=60',
      ]
    }
  },
  props: {
    farmer: {
      type: Object,
      required: true
    },
    experiment: {
      type: Object,
      required: true
    }
  },
  computed: {
    icons() {
      const icons = {
        adventices: "mdi-sprout",
        insectes: "mdi-ladybug",
        maladies: "mdi-bottle-tonic-plus",
        productivite: "mdi-chart-bell-curve-cumulative",
        biodiversite: "mdi-bee",
        sol: "mdi-image-filter-hdr",
        fourrages: "mdi-cow",
        "nouvelles-cultures": "mdi-corn",
        oad: "mdi-cellphone-information"
      }
      if (!this.experiment.tags)
        return []
      return this.experiment.tags
        .map(x =>
          x in icons ? { icon: icons[x], text: x.replace("-", " ") } : null
        )
        .filter(x => x != null)
    },
    breadcrumbs() {
      return [
        {
          text: "Carte des expérimentations",
          disabled: false,
          href: "/#/map"
        },
        {
          text: this.farmer.name,
          disabled: false,
          href: "/#/agriculteur/" + this.farmer.name
        }
      ]
    }
  }
}
</script>

<style scoped>
.subtitle-2,
.body-2 {
  line-height: 1.375rem;
}

.capitalize {
  text-transform: capitalize;
}
</style>
