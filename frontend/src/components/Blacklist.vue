<template>
  <v-card class="pa-2" style="margin-left: 10px; margin-right: 10px; max-width: 600px;">
    <v-card-title>Pratiques enlevées</v-card-title>
    <v-card-text>
      Voici les pratiques que vous avez indiquées comme n'étant pas pertinentes pour vous. Elles ne seront plus proposées.
    </v-card-text>
    <div v-for="practice in blacklist" :key="practice.id" class="pa-0">
      <v-divider />
      <v-card-text>{{ practice.title }}</v-card-text>
      <v-btn
        class="text-none caption"
        style="margin-left:10px; margin-bottom: 15px;"
        @click="removeFromBlacklist(practice)"
        rounded
      >Re-introduire cette pratique</v-btn>
    </div>
  </v-card>
</template>

<script>
export default {
  name: "Blacklist",
  computed: {
    blacklist() {
      return this.$store.state.blacklist
    }
  },
  methods: {
    removeFromBlacklist(practice) {
      window.gtag('event', 'blacklist remove', {
        event_category: 'Practice',
        event_label: practice.title,
        anonymize_ip: true
      })
      this.$store.dispatch("removeFromBlacklist", { practice: practice })
    }
  }
}
</script>