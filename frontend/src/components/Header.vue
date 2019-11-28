<template>
  <v-app-bar app color="primary" dark>
    <v-toolbar-title>Peps</v-toolbar-title>
    <v-spacer></v-spacer>
    <v-btn icon href="mailto:peps@beta.gouv.fr" target="_blank">
      <v-icon>mdi-email</v-icon>
    </v-btn>

    <v-btn icon href="https://www.peps.beta.gouv.fr/qui-sommes-nous" target="_blank">
      <v-icon>mdi-information</v-icon>
    </v-btn>
  </v-app-bar>
</template>

<script>

export default {
  name: "Header",
};
</script>