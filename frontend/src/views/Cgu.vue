<template>
  <div>
    <Title :title="title" :breadcrumbs="breadcrumbs" />
    <v-container class="constrained">
      <v-card-text style="color: #333;">
        <div class="display-1">Conditions générales d'utilisation de « nom du produit »</div>
        <div class="body-2">
          <p>Les présentes conditions d’utilisation (CGU) sont mise en œuvre conformément à l’article L. 112-9 du code des relations entre le public et l’administration. Elles s’imposent aux usagers.</p>
        </div>
        <div class="subtitle-2">1 - Présentation</div>
        <div class="body-2">
          <p>Peps (ci-après dénommé « le Service ») est mis en œuvre par le ministère de l’agriculture qui s’appuie sur l’expertise de la Direction interministérielle du numérique dans le cadre d’une délégation de gestion.</p>
          <p>Le Service est destiné à faciliter la transition vers un modèle agricole plus durable grâce au partage d'expériences entre agriculteurs ou personnes du monde agricole (gestionnaire de lycée agricole, agronome, autres). A ce titre elle ne présentera pas des retours d’expériences encourageant l’utilisation de produits phytosanitaires.</p>
        </div>
        <div class="subtitle-2">2 - Parcours usagers</div>
        <p>Le Service est une plateforme numérique de partage d’expériences avec deux parcours usagers.</p>
        <p>Un parcours visiteur, ouvert à tous, permettant de lire les fiches exploitations et expériences présentent sur la plateforme et d’entrer en contact avec l’agriculteur qui les partage. La création d’un compte est facultative.</p>
        <p>Un parcours « partageur » où une personne du monde agricole (ci après nommé « Partageur ») partage sur la plateforme des informations sur son exploitation et les expériences qu’il a pu y mener. Dans ce parcours, la création d’un compte est obligatoire.</p>
        <p>La création du compte s’effectue au moyen d’une adresse e-mail. Elle peut être faite directement par l’équipe chargée du Service ou par l’usager. Le compte ne nécessite pas de mot de passe mais un lien d’accès est envoyé à l’e-mail renseigné. Un compte permet de créer et modifier une fiche exploitation et des fiches expériences. Afin que ces fiches soient publiées sur le Service, le compte doit être approuvé par l’équipe chargée du service. Un compte permet de choisir la possibilité d’être contacté par d’autres agriculteurs.</p>
        <p>Le Service permet la prise de contact avec les usagers partageant leurs expériences. Celle-ci est intermédiée par l’équipe du Service qui délivre les coordonnées de ces derniers après une demande de l’usager.</p>

        <div class="subtitle-2">3 - Mentions légales</div>

        <p>Editeur : Ministère de l’Agriculture et de l’Alimentation.</p>
        <p>Directeur de la publication : Ministère de l’Agriculture et de l’Alimentation.</p>
        <p>Prestataire d'hébergement : Clevercloud, 3 rue de l'Allier, 44000 Nantes, France.</p>

        <div class="subtitle-2">4 – Modalités d’utilisation du Service</div>

        <p>L'utilisation du Service, est facultative et gratuite.</p>
        <p>Pour utiliser le service, il est requis de disposer d'un navigateur web récent. Pour Internet Explorer, il s'agit d'une version égale ou supérieure à IE11. Des dysfonctionnements ou impossibilité d'exploitation totale ou partielle du site et de ses fonctionnalités peuvent découler de ces incompatibilités.</p>
        <p>Le Service dépose des cookies de mesure d’audience (nombre de visites, pages consultées), respectant les conditions d’exemption du consentement de l’internaute définies par la recommandation « Cookies » de la Commission nationale informatique et libertés (CNIL); il utilise Matomo, un outil libre, paramétré pour ce faire. Cela signifie, notamment, que ces cookies ne servent qu’à la production de statistiques anonymes et ne permettent pas de suivre la navigation de l’internaute sur d’autres sites.</p>
        <p>Le Service dépose des cookies de navigation, aux fins strictement techniques, qui ne sont pas conservés.</p>

        <div class="subtitle-2">5 - Traitement des données</div>
        <p>Le Service ne collecte que les données strictement nécessaires à sa mise en œuvre.</p>
        <p>Les catégories de données traitées sont les suivantes :</p>
        <ul>
          <li>les données obligatoires pour la création du compte : nom, prénom, numéro de téléphone, adresse e-mail. L’équipe chargé du Service est destinataire de ces données,</li>
          <li>les données facultatives : l’ensemble des champs composant le profil et les expériences y compris les photos sont des champs libres. L’équipe chargée du Service se réserve néanmoins le droit de supprimer ou de proposer une modification lorsque le contenu proposé ne répond à des critères minimaux de qualité, en particulier la complétude et la véracité scientifique. L’équipe chargée du Service et les usagers sont destinataires de ces données.</li>
        </ul>
        <p>Les données sont conservées jusqu’à la fin de fonctionnement du Service.</p>
        <p>Le ministère de l’agriculture s'engage à prendre toutes précautions utiles pour préserver la sécurité des données collectées auprès de l'usager, et notamment empêcher qu'elles soient déformées et endommagées ou que des tiers non autorisés y aient accès.</p>
        <p>Le ministère de l’agriculture garantit aux usagers du Service les droits d'accès, de rectification et d'opposition prévus par la loi n° 78-17 du 6 janvier 1978 relative à l'informatique aux fichiers et aux libertés.</p>
        <p>Ces droits s’exercent auprès de l’équipe du Service. (peps@beta.gouv.fr)</p>
        <p>Le ministère de l’agriculture s'engage à n'opérer aucune commercialisation des informations et documents transmis par l'usager au moyen du Service, et à ne pas les communiquer à des tiers, en dehors des cas prévus par la loi.</p>
        <p>Les informations transmises par l'usager/utilisateur restent sous son contrôle. Il peut à tout moment les modifier ou les supprimer. Il peut choisir de supprimer toutes les informations de son compte en supprimant son compte. Seules sont conservées les informations permettant de répondre à d'éventuelles contestations et aux besoins statistiques du service.</p>

        <div class="subtitle-2">6 - Engagements et responsabilité</div>
        <p>Le présent Service est mis en œuvre selon les dispositions du code des relations entre le public et l’administration (CRPA).</p>
        <p>
          Le Service a été développé sous licence MIT , le code est disponible à l’adresse suivante :
          <a href="https://github.com/betagouv/peps/">https://github.com/betagouv/peps/</a>
        </p>
        <p>Le Service est mis à disposition sans autres garanties expresses ou tacites que celles qui sont prévues par les présentes.</p>
        <p>Le service est développé conformément à l’état de l’art. Toutefois, il n’est pas garanti qu’il soit exempt d’anomalies ou erreurs. Le service est donc mis à disposition sans garantie sur sa disponibilité et ses performances. A ce titre, le ministère de l’agriculture ne peut être tenu responsable des pertes et/ou préjudices, de quelque nature qu’ils soient, qui pourraient être causés à la suite d’un dysfonctionnement ou une indisponibilité du service. De telles situations n'ouvriront droit à aucune compensation financière.</p>
        <p>L’utilisateur s’engage à respecter les présentes CGU et la législation en vigueur. Il s’engage notamment à ne fournir, dans le cadre de l'utilisation du Service, que des informations exactes, à jour et complètes.</p>
        <p>Dans l'hypothèse où l'usager ne s'acquitterait pas de ses engagements, le ministère de l’agriculture se réserve le droit de suspendre ou résilier le service pour cet usager, sans préjudice des éventuelles actions en responsabilité pénale et civile qui pourraient être engagées à son encontre.</p>
        <p>Il est rappelé que toute personne procédant à une fausse déclaration pour elle-même ou pour autrui s'expose, notamment, aux sanctions prévues à l'article 441-1 du Code Pénal, prévoyant des peines pouvant aller jusqu'à trois ans d'emprisonnement et 45 000 euros d'amende.</p>

        <div class="subtitle-2">7 - Modification et évolution du Service</div>
        <p>Le ministère de l’agriculture se réserve la liberté de faire évoluer, de modifier ou de suspendre, sans préavis, le Service pour des raisons de maintenance ou pour tout autre motif jugé nécessaire. Une page d'information est alors affichée à l'usager lui mentionnant cette indisponibilité.</p>
        <p>Les termes des présentes conditions d’utilisation peuvent être modifiés ou complétés à tout moment, sans préavis, en fonction des modifications apportées au Service, de l’évolution de la législation ou pour tout autre motif jugé nécessaire. Ces modifications et mises à jour s’imposent à l’utilisateur qui doit, en conséquence, se référer régulièrement à cette rubrique pour vérifier les conditions générales en vigueur.</p>

        <div class="subtitle-2">8 - Nous contacter</div>
        <p>Difficultés techniques : peps@beta.gouv.fr</p>
        <p>Problèmes liés à la procédure : peps@beta.gouv.fr</p>
        <p>Droit d’accès CNIL : peps@beta.gouv.fr</p>
      </v-card-text>
    </v-container>
  </div>
</template>

<script>
import Title from "@/components/Title.vue"

export default {
  name: "CGU",
  components: { Title },
  metaInfo() {
    return {
      title: "Conditions générales d’utilisation",
      meta: [
        {
          description:
            "Voici la politique de confidentialité, les conditions générales d’utilisation et la politique des données & cookies"
        }
      ]
    }
  },
  data() {
    return {
      title: "Politique de confidentialité",
      breadcrumbs: [
        {
          text: "Accueil",
          disabled: false,
          to: { name: "Landing" }
        },
        {
          text: "Politique de confidentialité",
          disabled: true
        }
      ]
    }
  }
}
</script>