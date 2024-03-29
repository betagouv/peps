<template>
  <div>
    <Title :title="title" :breadcrumbs="breadcrumbs" />
    <v-container class="constrained">
      <div class="title">Un service public numérique</div>
      <div class="body-1">
        Le projet Peps a pour but d'accompagner la transition agroécologique des exploitations.
        Il est financé par le Ministère de l’Agriculture et de l’Alimentation et le Ministère de
        la Transition Écologique dans le cadre du plan Ecophyto 2+. Peps est gratuit et repose sur
        le volontariat.
      </div>
      <div class="body-1">
        Peps est développé un sein de l’incubateur Beta.gouv de la Direction Interministérielle du
        Numérique. L’expertise de cet incubateur est de construire des services numériques simples,
        faciles à utiliser, à l’impact maximal pour les usagers.
      </div>

      <v-btn
        href="https://beta.gouv.fr/"
        target="_blank"
        outlined
        color="primary"
        class="text-none"
        style="margin-top: 10px;"
      >En savoir plus</v-btn>

      <div class="title">Un monde agricole en pleine mutation</div>
      <div class="body-1">
        Entre mondialisation des marchés agricoles et pression pour diminuer l’usage des produits
        phytosanitaires, les exploitations changent grâce à l’adoption de nouvelles pratiques
        agroécologiques. Beaucoup cherchent à réduire leurs charges alors que les prix sont instables
        et imprédictibles. D’autres cherchent de nouvelles cultures ou de nouveaux débouchés afin de
        diversifier et assurer les revenus. Dans cette période particulièrement instable pour les exploitations,
        le partage et l’entraide sont d’autant plus importants. Échanger et apprendre permet d’avoir de
        nouvelles idées, d’éviter les échecs et finalement de trouver son équilibre, entre performance
        économique, agronomique, charge de travail et aspirations personnelles.
      </div>

      <div class="title">Peps facilite l’échange d'expériences entre agriculteurs</div>
      <div class="body-1">
        Sur le site, vous pouvez consulter des témoignages d’agriculteurs, partager vos retours d’expérience
        et échanger entre agriculteurs autour des retours d’expériences déjà en ligne. Par expériences nous
        entendons l’ensemble des projets que vous avez pu mener, des petits essais pour améliorer l’existant
        aux grands changements qui transforment structurellement votre exploitation.
      </div>
      <div class="body-1">
        Vous pourrez ainsi découvrir des pratiques concrètes, déjà mises en oeuvre par d’autres agriculteurs.
        Les témoignages sont variés, autant sur le plan géographique, que sur les thèmes évoqués ou encore le
        type d’agriculture pratiqué par les exploitants. L’objectif est que chacun puisse découvrir de nouvelles
        techniques ou projets et en approfondir d’autres.
      </div>
      <div class="body-1">
        La plateforme permet également de se mettre en contact avec d’autres agriculteurs via une messagerie
        sécurisée. Le contact entre agriculteurs permet de parler concrètement de l’action avec celui qui l’a
        mise en œuvre en pratique.
      </div>

      <div class="title">Un développement au plus proche du terrain</div>
      <div class="body-1">
        La réussite du projet est mesurée par l’utilité que vous trouvez à utiliser ce site. Il est donc développé
        grâce au contact constant avec ses utilisateurs, les agriculteurs. Nous sommes à l’écoute de tous retours,
        questions ou suggestions d’amélioration.
      </div>
      <v-btn
        :to="{ name: 'Contact' }"
        outlined
        color="primary"
        class="text-none"
        style="margin-top: 10px;"
      >Nous contacter</v-btn>

      <div class="title">L'équipe</div>
      <v-container class="ma-0 pa-5">
        <v-row>
          <v-col v-for="(member, index) in team" :key="index" cols="12" sm="3">
            <div style="text-align: center">
              <v-avatar :size="$vuetify.breakpoint.name === 'sm' ? 130 : 180">
                <v-img :src="member.imageUrl" />
              </v-avatar>
            </div>
            <div class="title" style="text-align: center; margin-bottom: 0px;">{{ member.name }}</div>
            <div class style="text-align: center;">{{ member.title }}</div>
          </v-col>
        </v-row>
      </v-container>

      <div class="title">Les soutiens</div>
      <v-container class="ma-0 pa-5">
        <v-row>
          <v-col v-for="(admin, index) in administrations" :key="index" cols="12" :sm="admin.size">
            <v-card class="pa-0 fill-height" elevation="0" :href="admin.url">
              <v-img class="white--text align-end" height="200px" :src="admin.imageUrl" contain />
            </v-card>
          </v-col>
        </v-row>
      </v-container>

      <div class="title">On parle de nous</div>
      <v-container class="ma-0 pa-5">
        <v-row>
          <v-col v-for="(article, index) in articles" :key="index" cols="12" sm="4">
            <v-card outlined class="pa-0 fill-height" elevation="0">
              <v-img class="white--text align-end" height="100" :src="article.imageUrl" :contain="article.contain" />
              <v-card-title class="caption grey--text">{{ article.journal }}</v-card-title>
              <v-card-subtitle class="subtitle-2 black--text">{{ article.title }}</v-card-subtitle>
              <v-btn
                class="text-none ma-3 fill-height"
                :href="article.url"
                target="_blank"
                color="primary"
                outlined
              >Voir l'article</v-btn>
            </v-card>
          </v-col>
        </v-row>
      </v-container>
    </v-container>
  </div>
</template>

<script>
import Title from "@/components/Title.vue"

export default {
  name: "About",
  components: { Title },
  metaInfo() {
    return {
      title: "Peps - une Startup d'État autonome financée par le plan Ecophyto",
      meta: [
        {
          description:
            "Le projet se construit à partir des retours du terrain, avec et pour les agriculteurs. Notre équipe est à votre écoute pour répondre à vos besoins",
        },
      ],
    }
  },
  data() {
    return {
      title: "Qui sommes-nous ?",
      breadcrumbs: [
        {
          text: "Accueil",
          disabled: false,
          to: { name: "Landing" },
        },
        {
          text: "Qui sommes-nous ?",
          disabled: true,
        },
      ],
      team: [
        {
          name: "Maud Blanck",
          title: "Experte métier",
          imageUrl: "/static/images/maud_blanck.png",
        },
        {
          name: "Alejandro M Guillén",
          title: "CTO / Développeur",
          imageUrl: "/static/images/alejandro_m_g.png",
        },
        {
          name: "Mathilde Petit",
          title: "Cheffe de produit informatique",
          imageUrl: "/static/images/mathilde_petit.png",
        },
        {
          name: "Benjamin Doberset",
          title: "Chargé de déploiement",
          imageUrl: "/static/images/benjamin_doberset.png",
        },
      ],
      administrations: [
        {
          imageUrl: "/static/images/dinum.png",
          size: 2,
          url: "https://www.numerique.gouv.fr/dinum/",
        },
        {
          imageUrl: "/static/images/minagri.png",
          size: 2,
          url: "https://agriculture.gouv.fr/",
        },
        {
          imageUrl: "/static/images/mineco.jpg",
          size: 2,
          url: "https://ecologie.gouv.fr/",
        },
        {
          imageUrl: "/static/images/ecophyto.png",
          size: 2,
          url: "https://agriculture.gouv.fr/ecophyto",
        },
        {
          imageUrl: "/static/images/inra.jpg",
          size: 2,
          url: "https://www.inrae.fr/",
        },
        {
          imageUrl: "/static/images/ofb.png",
          size: 2,
          url: "https://ofb.gouv.fr/",
        },
      ],
      articles: [
        {
          journal: "Ministère de l'Agriculture et de l'Alimentation",
          title:
            "Réduction des phytos : Peps facilite les retours d'expériences entre agriculteurs",
          imageUrl: "https://agriculture.gouv.fr/sites/minagri/files/styles/affichage_pleine-page_790x435/public/12093_072.jpg",
          contain: false,
          url:
            "https://agriculture.gouv.fr/reduction-des-phytos-peps-facilite-les-retours-dexperiences-entre-agriculteurs",
        },
        {
          journal: "Ministère de la Transition Écologique",
          title:
            "Transition du modèle agricole : Peps facilite les retours d’expérience entre agriculteurs",
          imageUrl: "https://www.ecologie.gouv.fr/sites/default/files/AB042750.jpg",
          contain: false,
          url:
            "https://www.ecologie.gouv.fr/transition-du-modele-agricole-peps-facilite-retours-dexperience-entre-agriculteurs",
        },
        {
          journal: "Ministère de la Transition Écologique",
          title:
            "L’agriculture et l’alimentation durables",
          imageUrl: "https://www.ecologie.gouv.fr/sites/default/files/Bandeau-foret-AB045452.jpg",
          contain: false,
          url:
            "https://www.ecologie.gouv.fr/lagriculture-et-lalimentation-durables",
        },
        {
          journal: "OFB : Le portail technique",
          title:
            "Plan Écophyto, réduire et améliorer l'utilisation des produits phytosanitaires",
          imageUrl: "https://professionnels.ofb.fr/sites/default/files/phyto.png",
          contain: false,
          url:
            "https://professionnels.ofb.fr/fr/node/286",
        },
        {
          journal: "Écophyto PIC",
          title:
            "Transition du modèle agricole : Peps facilite les retours d’expérience entre agriculteurs",
          imageUrl: "https://ecophytopic.fr/sites/default/files/styles/a_la_une_175x140_/public/2020-09/PEPS.jpg",
          contain: true,
          url:
            "https://ecophytopic.fr/concevoir-son-systeme/transition-du-modele-agricole-peps-facilite-les-retours-dexperience-entre",
        },
      ],
    }
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
.body-1 {
  margin-top: 15px;
}
</style>
