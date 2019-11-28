<template>
  <v-card dark tile elevation="0">
    <v-footer class="font-weight-medium">
      <v-col class="text-center" cols="12">
        {{ new Date().getFullYear() }} —
        <strong>Peps</strong>
      </v-col>
    </v-footer>
  </v-card>
</template>

<script>

export default {
  name: "Footer",
}
</script>