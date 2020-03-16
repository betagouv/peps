<template>
  <div>
    <v-list-item style="margin: 10px 0 0 0;" class="pa-0">
      <v-list-item-avatar color="grey">
        <v-img :src="farmer.profile_image ? farmer.profile_image : '/static/images/user.png'"></v-img>
      </v-list-item-avatar>
      <v-list-item-content>
        <v-list-item-title>{{ farmer.name }}</v-list-item-title>
        <v-list-item-subtitle>{{ farmer.profession }}</v-list-item-subtitle>
      </v-list-item-content>
    </v-list-item>
    <v-btn class="text-none" outlined color="primary">Contacter {{farmer.name}}</v-btn>
  </div>
</template>

<script>
export default {
  name: "FarmerListItem",
  props: {
    farmer: {
      type: Object,
      required: true
    }
  }
}
</script>
