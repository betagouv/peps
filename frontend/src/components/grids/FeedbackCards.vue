<template>
  <v-container class="constrained ma-0 pa-0">
    <v-row>
      <v-col v-for="(item, index) in descriptionItems" :key="index" cols="12" sm="6">
        <v-card class="pa-0 fill-height">
          <v-card-title class="subtitle-2">{{ item.title }}</v-card-title>
          <v-card-text style="margin-bottom: 40px;">{{ item.body }}</v-card-text>
          <v-btn
            class="text-none ma-3 fill-height"
            @click="item.onClick()"
            target="_blank"
            rounded
            small
            color="primary"
            style="position: absolute; bottom: 0;"
          >{{item.buttonText}}</v-btn>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
export default {
  name: "FeedbackCards",
  data() {
    return {
      descriptionItems: [
        {
          title: "Je donne mon avis",
          onClick: () => this.feedbackCallback ? this.feedbackCallback() : this.goToContact(),
          body:
            "Prenez 2 minutes pour nous faire vos retours et vos suggestions sur le service",
          buttonText: "Faire un retour"
        },
        {
          title: "Je contribue au projet",
          onClick: () => this.contributionCallback ? this.contributionCallback() : this.goToContact(),
          body:
            "Lors d'un entretien, de test de nouvelles interfaces, un tour de plaine...",
          buttonText: "Je contribue !"
        }
      ]
    }
  },
  methods: {
    goToContact: function() {
      this.$router.push({
        name: "Contact"
      })
    }
  },
  props: {
    feedbackCallback: {
      type: Function,
    },
    contributionCallback: {
      type: Function,
    }
  }
}
</script>
