<template>
  <v-row>
    <v-col v-for="(video, index) in videos" :key="index" cols="12" sm="6">
      <v-card flat style="cursor: pointer;">
        <video style="height: 230px; width: 100%; background: #333;" controls="controls">
          <source type="video/mp4" :src="video.video" />Votre navigateur ne peut pas afficher des vidéos.
        </video>
        <v-card-subtitle class="caption" style="padding: 5px;">{{video.label}}</v-card-subtitle>
      </v-card>
    </v-col>
  </v-row>
</template>

<script>

export default {
  name: "VideoGallery",
  props: {
    videos: {
      type: Array,
      required: true
    }
  }
}
</script>