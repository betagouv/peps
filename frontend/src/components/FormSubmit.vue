<template>
  <div style="margin-top: 30px; text-align: right">
    <v-btn large :disabled="disabled" color="primary">Trouver des pratiques alternatives</v-btn>
    <p
      :style="{visibility: disabled ? 'visible' : 'hidden'}"
      class="caption"
      style="margin-top: 10px;"
    >
      <v-icon small>mdi-alert-circle</v-icon>Répondez à toutes les questions ci-dessus pour continuer
    </p>
  </div>
</template>

<script>
export default {
  name: "FormSubmit",
  computed: {
    disabled() {
      return this.$store.getters.formsAreComplete
    }
  }
}
</script>