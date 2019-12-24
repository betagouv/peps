<template>
      <v-container class="ma-0 pa-0">
        <v-row>
          <v-col v-for="(item, index) in descriptionItems" :key="index" cols="12" sm="6" md="4">
            <v-card class="pa-0 fill-height" outlined>
              <v-card-title class="subtitle-2">{{ item.title }}</v-card-title>
              <v-card-text>{{ item.body }}</v-card-text>
              <v-btn
                class="text-none ma-3 fill-height"
                :href="item.buttonUrl"
                target="_blank"
                v-if="item.buttonText && item.buttonUrl"
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
  name: "DescriptionCards",
  data() {
    return {
      descriptionItems: [
        {
          title: "Des pratiques documentées et éprouvées par des agriculteurs",
          body:
            "Tout ce que vous trouvez ici est déjà en place ailleurs."
        },
        {
          title: "Toutes les informations sur les pratiques, au même endroit",
          body:
            "Terminées les recherches infinies sur internet."
        },
        {
          title: "Un service public numérique.",
          body:
            "Gratuit et pour tous.",
          buttonUrl: "https://beta.gouv.fr/apropos/",
          buttonText: "En savoir plus"
        }
      ]
    }
  }
}
</script>
