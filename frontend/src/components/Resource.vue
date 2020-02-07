<template>
  <v-card
    class="resource-card pa-0"
    outlined
    :href="resource.url"
    target="_blank"
    style="border-color: #FFF; margin: 10px 0 0 0;"
  >
    <div class="resource-image">
      <v-img
        class="align-start"
        position="center"
        v-if="resource.image"
        contain
        max-width="70"
        max-height="50"
        :src="resource.image"
      />
      <v-icon
        v-else
        size="35"
        color="primary"
        style="width: 70px; margin-left: auto; margin-right: auto;"
      >{{iconName}}</v-icon>
    </div>
    <div class="resource-text">
      <v-card-title class="body-1 resource-name pa-0">{{ resource.name }}</v-card-title>
      <v-card-text class="pa-0 resource-description caption">{{ resource.description }}</v-card-text>
    </div>
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
      return Object.prototype.hasOwnProperty.call(icons, type)
        ? icons[type]
        : "mdi-file-document-outline"
    }
  }
}
</script>

<style scoped>
.resource-card:hover .resource-name {
  text-decoration: underline;
}
.resource-image {
  float: left;
}
.resource-text {
  margin-left: 80px;
}
</style>
