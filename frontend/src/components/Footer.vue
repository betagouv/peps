<template>
  <v-container>
    <v-divider style="margin-bottom: 25px;" />

    <v-card color="#EEE" tile elevation="0">
      <div style="text-align: center; margin-bottom: 12px;">
        <img src="/static/images/betagouv.png" style="height:35px; opacity:0.5;" />
      </div>
      <div class="caption" style="color: #777; text-align: center;">
        {{ new Date().getFullYear() }} — Peps
      </div>
      <v-card-text style="text-align: center;">
        <v-btn icon class="mx-2" href="https://twitter.com/pepsagriculture" target="_blank">
          <v-icon size="24px">mdi-twitter</v-icon>
        </v-btn>
        <v-btn icon class="mx-2" href="https://www.facebook.com/pepsagriculture/" target="_blank">
          <v-icon size="24px">mdi-facebook-box</v-icon>
        </v-btn>
      </v-card-text>
    </v-card>
  </v-container>
</template>

<script>
export default {
  name: "Footer"
}
</script> 