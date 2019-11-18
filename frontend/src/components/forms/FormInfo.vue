<template>
    <v-card outlined color="#fafafa" elevation=0 style="border: 1px solid #e7e7e7;">
      <v-card-text>{{ description }}</v-card-text>
    </v-card>
</template>

<script>
export default {
  name: "FormInfo",
  props: {
    description: {
      type: String
    }
  }
};
</script>