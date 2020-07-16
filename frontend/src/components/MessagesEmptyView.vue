<template>
  <div class="d-flex flex-column justify-center align-center" style="height: 100%; color: #999;">
    <v-icon size=80 color="#999" style="margin-bottom: 20px;">
      mdi-message-outline
    </v-icon>
    <p style="text-align: center;" class="title">
      Vous n'avez pas de messages
    </p>
    <p style="text-align: center; max-width: 400px;" class="caption">
      Pour contacter un agriculteur, clickez sur le bouton "Contacter" dans leur page de profil ou directement dans la page du retour d'expérience qui vous intéresse
    </p>
  </div>
</template>

<script>
export default {
  name: "MessagesEmptyView"
}
</script>