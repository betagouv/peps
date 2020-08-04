<template>
  <v-container class="constrained" style="margin: 50px auto 50px auto;">
    <div class="title">🤔 Nous n'avons pas trouvé ce que vous cherchez</div>
    <div class="body-2" style="margin-top: 20px;">
      Nous sommes désolés ! Nous n'avons pas trouvé la page que vous recherchez.
      Il se peut qu'elle ait ait été déplacée ou supprimée.
      Vérifiez que l'URL que vous avez saisie est correcte puis réessayez.
      </div>
    <div>
      <v-btn style="margin-top: 50px;" color="primary" :to="{ name: 'Landing' }" class="text-none">Revenir à l'accueil</v-btn>
    </div>
    <div>
      <v-btn color="primary" outlined elevation="0" style="margin-top: 30px;" :to="{ name: 'Contact' }">
        <v-icon style="margin-right: 5px; padding-top: 2px;" small>mdi-email</v-icon>
        <span class="text-none">Contact</span>
      </v-btn>
    </div>
    <div>
      <v-btn color="primary" outlined elevation="0" style="margin-top: 10px;" :to="{ name: 'QuiSommesNous' }">
        <v-icon style="margin-right: 5px; padding-top: 2px;" small>mdi-information</v-icon>
        <span class="text-none">En savoir plus</span>
      </v-btn>
    </div>
  </v-container>
</template>

