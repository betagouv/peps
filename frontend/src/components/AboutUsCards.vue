<template>
  <v-row>
    <v-col v-for="item in items" :key="item.title" cols="12" sm="6" md="4">
      <v-card elevation="0">
        <v-img height="180px" contain :src="item.imageSource" />
        <v-card-title>{{item.title}}</v-card-title>
        <v-card-subtitle>{{item.text}}</v-card-subtitle>
        <v-card-actions>
          <v-btn
            color="primary"
            :to="item.ctaTo"
            :href="item.ctaLink"
            class="primary--text text-decoration-underline text-none"
            :target="item.ctaLink ? '_blank' : undefined"
            text
          >{{item.ctaText}}</v-btn>
        </v-card-actions>
      </v-card>
    </v-col>
  </v-row>
</template>

<script>
export default {
  name: "AboutUsCards",
  data() {
    return {
      items: [
        {
          imageSource: "/static/images/aidants.jpg",
          title: "Un service public",
          text:
            "Gratuit et pour tous ! Ce projet s'inscrit dans le plan Ecophyto, financé par le Ministère d'Agriculture et de l'Environnement",
          ctaText: "En savoir plus",
          ctaTo: null,
          ctaLink: "https://beta.gouv.fr/startups/peps.html",
        },
        {
          imageSource: "/static/images/agriculteurs_tracteur.jpg",
          title: "Sur le terrain !",
          text:
            "Ce service est construit à partir des retours des utilisateurs et au contact du terrain. Vous pouvez participer !",
          ctaText: "Nous contacter",
          ctaTo: { name: "Contact" },
          ctaLink: null,
        },
        {
          imageSource: "/static/images/agriculteurs_echange.jpg",
          title: "Une équipe autonome",
          text:
            "Spécialistes du numérique et de l'agronomie pour développer le meilleur service possible",
          ctaText: "Qui sommes nous ?",
          ctaTo: { name: "QuiSommesNous" },
          ctaLink: null,
        },
      ],
    }
  },
}
</script>