<template>
  <v-card dark tile elevation="0">
    <v-footer v-show="loadingComplete" class="font-weight-medium">
      <v-col class="text-center" cols="12">
        {{ new Date().getFullYear() }} —
        <strong>Peps</strong>
      </v-col>
    </v-footer>
  </v-card>
</template>

<script>
import Constants from "@/constants";

export default {
  name: "Footer",
  computed: {
    loadingComplete() {
      return (
        this.$store.state.formDefinitionsLoadingStatus !==
        Constants.LoadingStatus.LOADING
      );
    }
  }
};
</script>