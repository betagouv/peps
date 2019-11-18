<template>
  <v-dialog v-model="loading" persistent width="300">
    <v-card>
    <v-card-title>{{title}}</v-card-title>
    <v-card-text v-if="text != ''">{{text}}</v-card-text>
      <v-card-text>
        <v-progress-linear indeterminate color="primary" class="mb-0"></v-progress-linear>
      </v-card-text>
    </v-card>
  </v-dialog>
</template>

<script>
export default {
  name: "Loader",
  data() {
    return {
      loading: true
    };
  },
  props: {
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
