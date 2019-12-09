<template>
  <v-overlay :value="loading" :dark="false">
    <v-card style="width: 500px">
    <v-card-title>{{title}}</v-card-title>
    <v-card-text v-if="text != ''">{{text}}</v-card-text>
      <v-card-text>
        <v-progress-linear indeterminate color="primary" class="mb-0"></v-progress-linear>
      </v-card-text>
    </v-card>
  </v-overlay>
</template>

<script>
export default {
  name: "Loader",
  props: {
    loading: {
      type: Boolean,
      default: true,
    },
    title: {
      type: String,
      default: "En cours..."
    },
    text: {
      type: String,
      default: ""
    },
  }
};
</script>

<style>
</style>
