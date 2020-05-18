<template>
  <div>
    <Title :title="title" :breadcrumbs="breadcrumbs" />
    <v-container class="constrained">
      <div>
        <div class="display-1 primary--text">Le constat</div>
        <div class="body-1">
          Le système agricole actuel est en pleine transformation sous l’effet de différentes
          dynamiques en particulier la mondialisation du marché agricole - qui entraîne une fluctuation
          des prix - et la réduction de l’utilisation des produits phytosanitaires - sous l’effet de
          l’apparition de résistances des adventices/ravageurs, de la demande sociétale et de la
          réglementation.
        </div>
        <div class="body-1">
          Dans ce contexte, les agriculteurs sont de plus en plus amenés à repenser leur
          exploitation. Beaucoup cherchent à réduire leurs charges alors que les prix ne sont
          pas stables et peu prédictibles. D’autres se tournent vers de nouvelles pratiques
          agroécologiques se substituant à l’action des produits phytosanitaires tandis que
          certains cherchent des nouvelles cultures ou des nouveaux débouchés afin de diversifier
          et assurer les revenus. Ces nouvelles pistes ne sont bien évidemment pas exclusives
          et sont souvent combinées.
        </div>

        <div class="display-1 primary--text">La proposition</div>
        <div class="body-1">
          Peps est d’une plateforme de partage d’expériences entre agriculteurs. Par expérience
          nous entendons l’ensemble des projets qu’un agriculteur a pu mener, des petits essais
          pour améliorer l’existant aux grands changements qui transforment structurellement
          l’exploitation.
        </div>

        <div class="title">
          Pourquoi nous avons choisi la piste du partage d’expérience?
        </div>

        <div class="body-1">
          A la suite d’entretiens avec des agriculteurs, il ressort que ceux ci sont intéressés
          par les essais mis en place par d’autres agriculteurs, en particulier quand ils sont
          proches géographiquement. En outre, le partage et l’entraide sont des pratiques
          traditionnellement répandues parmi cette profession.
        </div>

        <div class="body-1">
          Plus largement, si les agriculteurs ont toujours mené des essais sur leur
          exploitation, cette aptitude apparaît aujourd’hui d’autant plus primordiale.
          En effet, l’adoption des pratiques agroécologiques passe nécessairement par leur
          expérimentation, celles-ci présentant un caractère moins systématique et plus
          systémique que les produits phytosanitaires. En outre, la diversification et
          la recherche d’un nouveau modèle pour une exploitation agricole passe par
          l’introduction de nouvelles cultures dans les rotations et la diversification
          des débouchés (vente directe, production d’énergie, nouvel atelier…)
        </div>

        <div class="title">
          Quel sont les objectifs d’un tel service ?
        </div>

        <div class="body-1">
          L’objectif du partage d’expérience est de soutenir la pratique de
          l’expérimentation chez les agriculteurs en :
          <ul>
            <li>
              favorisant la découverte de nouvelles idées ou de nouvelles
              manières de mettre en oeuvre des pratiques qu’ils connaissent déjà,
            </li>
            <li>
              montrant ce que fait le terrain et en valorisant un monde agricole qui
              change,
            </li>
            <li>
              facilitant la mise en contact entre les agriculteurs
            </li>
          </ul>
        </div>

        <div class="title">
          Comment travaillons-nous pour créer Peps ?
        </div>

        <div class="body-1">
          Comme toutes les startups d’État, Peps se construit à partir des retours du terrain.
          Ainsi, depuis le début du projet nous avons conduit des entretiens avec plus de 150
          agriculteurs.
        </div>

        <div class="body-1">
          Aujourd’hui, nous cherchons à valider la proposition de valeur présentée plus haut
          c’est à dire nous assurer que les agriculteurs trouvent de l’intérêt dans un tel service.
          Pour ce faire, nous lançons un prototype avec les agriculteurs volontaires.
        </div>

        <div class="body-1">
          Si vous êtes agriculteurs et souhaitez participer au test de ce prototype, <a href="/#/contact" target="_blank">contactez nous</a>.
        </div>

        <div class="display-1 primary--text">Historique</div>

        <div class="body-1">
          Dans sa première version, nous avions développé un site qui, à partir de quelques
          données sur l’exploitation de l’agriculteur, proposait automatiquement des pratiques
          alternatives à la chimie. Ces pratiques étaient documentées à partir des ressources
          la plateforme d’EcophytoPIC et notre outil s’inscrivait dans le volet diffusion du
          plan Ecophyto 2+.
        </div>

        <div class="body-1">
          Aujourd’hui, la version 2 n’utilise pas ce simulateur, le choix ayant été fait de
          se focaliser sur le partage d’expérience et la recherche par zone géographique
          et/ou catégorie. Néanmoins, l’outil demeure fonctionnel et pourra être intégrée
          à la nouvelle proposition dans un second temps afin de proposer de nouvelles
          modalités de recherche d’expérience.
        </div>
      </div>



      <div style="margin-top: 10px;">
        <div class="display-1 primary--text">L'équipe actuelle</div>
        <v-container class="ma-0 pa-5">
          <v-row>
            <v-col v-for="(member, index) in team" :key="index" cols="12" sm="3">
              <v-card class="pa-0 fill-height" elevation="0">
                <v-img class="white--text align-end" height="200" contain :src="member.imageUrl" />
                <div class="caption grey--text">{{ member.name }}</div>
                <div class="subtitle-2 black--text">{{ member.title }}</div>
              </v-card>
            </v-col>
          </v-row>
        </v-container>
      </div>

    </v-container>
  </div>
</template>

<script>
import Title from "@/components/Title.vue"

export default {
  name: "About",
  components: { Title },
  data() {
    return {
      title: 'Qui sommes-nous ?',
      breadcrumbs: [{
        text: 'Accueil',
        disabled: false,
        href: '/#/'
      }, {
        text: 'Qui sommes-nous ?',
        disabled: true,
      }],
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
.body-1 {
  margin-top: 15px;
}
</style>
