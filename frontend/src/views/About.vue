<template>
  <div>
    <v-card>
      <v-card-title class="display-1 primary--text">Le constat</v-card-title>
      <v-divider />
      <v-card-subtitle class="title">Des agriculteurs qui souhaitent faire évoluer leur système</v-card-subtitle>
      <v-card-text>
        Augmentation des charges, efficacité en baisse de certains produits, impasses techniques... La plupart des
         agriculteurs font ces observations directement sur leur exploitation. Il devient alors nécessaire de 
         trouver d'autres pratiques pour répondre aux problèmes d'adventice, de ravageur ou de maladie.
      </v-card-text>
      <v-card-text>
        D'autre part, les agriculteurs sont les premiers concernés par l'impact sur la santé du tout chimique et
        subissent une pression sociale parfois violente.
      </v-card-text>

      <v-card-subtitle class="title">Des agriculteurs connectés</v-card-subtitle>
      <v-card-text>
        Les agriculteurs sont l'une des catégories socio-professionnelles les plus connectées. L'étude Agrinautes
        2018 réalisée par BVA pour Terre-net Média et Hyltel montre que 85% des agrinautes recherchent sur internet
        des informations technique sur leurs cultures.
      </v-card-text>

      <v-card-subtitle class="title">Beaucoup d’initiatives locales qui fonctionnent et sont documentées</v-card-subtitle>
      <v-card-text>
        Depuis plusieurs années, l'ensemble du monde agricole s'est mobilisé pour tester des pratiques alternatives
        à la chimie. Les résultats sont très positifs et de nombreux agriculteurs utilisent désormais ces techniques
        dans leur exploitation.
      </v-card-text>
      <v-card-text>
        Ces pratiques sont documentées et recensées dans différentes bases de données au niveau national : EcophytoPic,
        GECO, les CEPP, le Centre National de Ressource Glyphosate, sur les sites des instituts techniques...
      </v-card-text>
      <v-card-text>
        Des expériences d'agriculteurs sont également la pour concrétiser ces documentations, par exemple celles des
        agriculteurs du réseau DEPHY, des CETA, de groupes GIEE ou 30000 et bien d'autres !
      </v-card-text>
    </v-card>

    <v-card style="margin-top: 10px;">
      <v-card-title class="display-1 primary--text">Notre demarche</v-card-title>
      <v-divider />
      <v-card-subtitle class="title">Un service public numérique</v-card-subtitle>
      <v-card-text>
        Peps est une startup d'État dont l'objectif est d'accompagner les agriculteurs vers des pratiques économes
        en produits phytosanitaires.
      </v-card-text>
      <v-card-text>
        Le dispositif Startup d’Etat vise à utiliser les principes de fonctionnement des Startups pour répondre
        à un problème lié à une politique publique. Le service est ainsi co-conçu à partir d'atelier avec les
        acteurs du terrain. Une première version, même imparfaite, est lancée rapidement et améliorée par la
        suite avec le retours des agriculteurs et des acteurs du monde agricole. Au lieu de sortir dans 5 ans
        un produit a priori parfait mais jamais confronté au terrain, une Startup d'Etat lance un service public
        petit qu'elle fait grandir au fur et à mesure avec ses utilisateurs. L'objectif est de construire avec le
        terrain un service utile et utilisé.
      </v-card-text>

      <v-card-subtitle class="title">Concevoir avec et pour les utilisateurs</v-card-subtitle>
      <v-card-text>
        À l’instar des autres Startup d’État, l’équipe de Peps s’attache d'abord à comprendre les problématiques
        de chacune des parties prenantes pour créer un service adapté en synergie avec les outils et dynamiques
        existantes.
      </v-card-text>
      <v-card-text>
        Pour se faire, nous prenons contact avec toutes les personnes qui œuvrent sur le sujet et nous allons
        autant que possible au contact du terrain pour les rencontrer. Ainsi, Peps a organisé des journées de
        travail avec l'ensemble du monde agricole : agriculteurs, syndicats, DRAAF, DDT, Chambres d'agricultures,
        coopératives, association environnementale, CUMA. L'équipe Peps suit aussi des conseillers de coopératives
        et des agriculteurs dans leur journée de travail.
      </v-card-text>
    </v-card>

    <v-card style="margin-top: 10px;">
      <v-card-title
        class="display-1 primary--text"
      >Nos administrations référentes</v-card-title>
      <v-divider />
      <v-container class="ma-0 pa-5">
        <v-row>
          <v-col v-for="(admin, index) in administrations" :key="index" cols="12" :sm="admin.size">
            <v-card class="pa-0 fill-height" elevation="0">
              <v-img class="white--text align-end" height="200px" :src="admin.imageUrl" contain />
            </v-card>
          </v-col>
        </v-row>
      </v-container>
    </v-card>

    <v-card style="margin-top: 10px;">
      <v-card-title class="display-1 primary--text">L'équipe</v-card-title>
      <v-divider />
      <v-container class="ma-0 pa-5">
        <v-row>
          <v-col v-for="(member, index) in team" :key="index" cols="12" sm="3">
            <v-card class="pa-0 fill-height" elevation="0">
              <v-img
                class="white--text align-end"
                height="200"
                contain
                :src="member.imageUrl"
              />
              <v-card-title class="caption grey--text">{{ member.name }}</v-card-title>
              <v-card-subtitle class="subtitle-2 black--text">{{ member.title }}</v-card-subtitle>
            </v-card>
          </v-col>
        </v-row>
      </v-container>
    </v-card>

    <v-card style="margin-top: 10px;">
      <v-card-title class="display-1 primary--text">Dans la presse</v-card-title>
      <v-divider />
      <v-container class="ma-0 pa-5">
        <v-row>
          <v-col v-for="(article, index) in articles" :key="index" cols="12" sm="4">
            <v-card class="pa-0 fill-height" elevation="0">
              <v-img
                class="white--text align-end"
                height="100"
                contain
                :src="article.imageUrl"
              />
              <v-card-title class="caption grey--text">{{ article.journal }}</v-card-title>
              <v-card-subtitle class="subtitle-2 black--text">{{ article.title }}</v-card-subtitle>
              <v-btn
                class="text-none ma-3 fill-height"
                :href="article.url"
                target="_blank"
                rounded
                small
                color="primary"
              >Voir l'article</v-btn>
            </v-card>
          </v-col>
        </v-row>
      </v-container>
    </v-card>
  </div>
</template>

<script>
export default {
  name: "About",
  data() {
    return {
      team: [
        {
          name: "Maud Blanck",
          title: "Experte métier",
          imageUrl: "/static/images/maud_blanck.png"
        },
        {
          name: "Alejandro Mantecon Guillen",
          title: "CTO / Développement logiciel",
          imageUrl: "/static/images/alejandro_m_g.png"
        },
        {
          name: "Mathilde Petit",
          title: "Cheffe de produit informatique",
          imageUrl: "/static/images/mathilde_petit.png"
        },
        {
          name: "Benjamin Doberset",
          title: "Chargé de déploiement",
          imageUrl: "/static/images/benjamin_doberset.png"
        }
      ],
      administrations: [
        {
          imageUrl: "/static/images/dinum.png",
          size: 2
        },
        {
          imageUrl: "/static/images/minagri.png",
          size: 2
        },
        {
          imageUrl: "/static/images/mineco.jpg",
          size: 3
        },
        {
          imageUrl: "/static/images/ecophyto.png",
          size: 2
        },
        {
          imageUrl: "/static/images/inra.jpg",
          size: 2
        }
      ],
      articles: [
        {
          journal: "Le contrat de solutions",
          title:
            "Peps : accompagner les agriculteurs dans la réduction des produits phytosanitaires",
          imageUrl: "/static/images/contrat-de-solutions.png",
          url:
            "https://contratsolutions.fr/actualites/peps-accompagner-les-agriculteurs-dans-la-reduction-des-produits-phytosanitaires/"
        },
        {
          journal: "Agrifind",
          title:
            "Peps : Une initiative pour la durabilité agronomique des exploitations agricoles",
          imageUrl: "/static/images/agrifind.png",
          url:
            "https://www.agrifind.fr/peps-une-initiative-pour-la-durabilite-agronomique-des-exploitations-agricoles/"
        },
        {
          journal: "La France Agricole",
          title:
            "Task force, enquête flash, start-up d’État, centre de ressources…",
          imageUrl: "/static/images/la-france-agricole.png",
          url:
            "http://www.lafranceagricole.fr/actualites/cultures/sortie-du-glyphosate-task-force-enquete-flash-start-up-detat-centre-de-ressources-1,8,2751982137.html"
        }
      ]
    }
  }
}
</script>

<style scoped>
.theme--light.v-card > .v-card__subtitle, .theme--light.v-card > .v-card__text {
  color: rgba(0, 0, 0, 0.87);
}
</style>
