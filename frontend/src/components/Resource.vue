<template>
  <v-card
    class="resource-card pa-0"
    outlined
    :href="resource.url"
    target="_blank"
    style="border-color: #FFF; margin: 10px 0 0 0;"
  >
    <v-card-title class="body-1" style="padding: 5px 0 5px 0;">
      <v-icon color="primary" style="margin-right:10px;">{{iconName}}</v-icon>
      <span class="resource-name">{{ resource.name }}</span>
    </v-card-title>
    <v-card-text class="pa-0">{{ resource.description }}</v-card-text>
  </v-card>
</template>

<script>
export default {
  name: "Resource",
  props: {
    resource: {
      type: Object,
      required: true
    }
  },
  computed: {
    iconName() {
      const type = this.resource.resource_type
      const icons = {
        SITE_WEB: "mdi-web",
        PDF: "mdi-pdf-box",
        VIDEO: "mdi-youtube"
      }
      return icons.hasOwnProperty(type)
        ? icons[type]
        : "mdi-file-document-outline"
    }
  }
}
</script>

<style>
.resource-card:hover .resource-name {
  text-decoration: underline;
}
</style>
