<template>
    <v-card class="form-info" color="#fafafa" elevation=0>
      <v-card-text>{{ description }}</v-card-text>
    </v-card>
</template>

<script>
export default {
  name: "InfoWell",
  props: {
    description: {
      type: String
    }
  }
};
</script>

<style>
.form-info {
  border: 1px solid rgb(217, 217, 217) !important;
}
</style>