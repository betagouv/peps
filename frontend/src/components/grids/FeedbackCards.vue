<template>
  <v-container class="ma-0 pa-0">
    <v-row>
      <v-col v-for="(item, index) in descriptionItems" :key="index" cols="12" sm="6" md="4">
        <v-card class="pa-0 fill-height" outlined>
          <v-card-title class="subtitle-2">{{ item.title }}</v-card-title>
          <v-card-text>{{ item.body }}</v-card-text>
          <v-btn
            class="text-none ma-3"
            :href="item.buttonUrl"
            target="_blank"
            rounded
            small
            color="primary"
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
          body:
            "Prenez 2 minutes pour nous faire vos retours et vos suggestions sur le service",
          buttonUrl: "https://alejandromg.typeform.com/to/bltLaz",
          buttonText: "Répondre au sondage"
        },
        {
          title: "J'ai un retour précis sur le service",
          body: "Par mail ou par téléphone, nous sommes tout ouïe",
          buttonUrl: "mailto:peps@beta.gouv.fr",
          buttonText: "Contacter l'équipe"
        },
        {
          title: "Je suis prêt à contribuer au projet",
          body:
            "Lors d'un entretien, de test de nouvelles interfaces, un tour de plaine...",
          buttonUrl: "https://alejandromg.typeform.com/to/gGE3LM",
          buttonText: "Je m'inscris !"
        }
      ]
    }
  }
}
</script>
