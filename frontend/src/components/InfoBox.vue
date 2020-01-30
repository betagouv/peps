<template>
    <v-card tile color="#E0F4EE" elevation="0" style="border-color: #E0F4EE !important;">
      <v-card-text>
        <v-container v-for="(item, index) in infoItems" :key="index" class="pa-0">
        <v-row no-gutters v-if="infoItems && infoItems.length > 0" class="caption" style="margin-bottom: 7px;">
          <v-col cols="12" sm="3" class="pa-0">
            {{item.title}}
          </v-col>
          <v-col class="pa-0" style="color: #333;">{{item.text}}
          </v-col>
        </v-row>
        </v-container>
      </v-card-text>
    </v-card>
</template>

<script>

export default {
  name: "InfoBox",
  props: {
    infoItems: {
      type: Array,
      required: true
    }
  }
}
</script>

