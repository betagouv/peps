<template>
  <v-card
    class="resource-card"
    outlined
    :href="resource.url"
    target="_blank"
    style="border-color: #FFF;"
  >
    <v-card-title class="body-1 resource-title" style="padding-bottom: 5px;">
      <v-icon color="primary" style="margin-right:10px;">{{iconName}}</v-icon>
      {{ resource.name }}
    </v-card-title>
    <v-card-text>{{ resource.description }}</v-card-text>
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
.resource-card:hover .resource-title {
  text-decoration: underline;
}
</style>
