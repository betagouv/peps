<template>
  <v-row>
    <v-col
      v-for="(video, index) in videoArray"
      :key="index"
      class="d-flex child-flex"
      cols="12"
      sm="6"
      md="4"
    >
      <v-card flat class="d-flex flex-column fill-height">
        <video style="height: 230px; background: #333;" controls>
          <source type="video/mp4" :src="video.video" />Votre navigateur ne peut pas afficher des vidéos.
        </video>
        <div style="position: absolute; top: 10px; left: 10px;">
          <v-btn fab small @click="deleteVideo(index)">
            <v-icon color="red">mdi-trash-can-outline</v-icon>
          </v-btn>
        </div>
        <v-text-field
          hide-details="auto"
          class="caption"
          v-model="video.label"
          @input="emitChange"
          outlined
          placeholder="Ajoutez une description"
          style="margin-top: 5px;"
        ></v-text-field>
      </v-card>
    </v-col>

    <v-col cols="12" sm="6" md="4">
      <v-card class="fill-height" style="min-height: 270px" color="#E0F4EE">
        <label
          class="d-flex flex-column align-center justify-center"
          :for="uniqueId + '_video-input'"
          style="width: 100%; height: 100%; cursor: pointer;"
        >
          <v-icon class="align-center">mdi-video</v-icon>
          <div class="subtitle-2">Ajoutez des vidéos</div>
        </label>
        <input
          :id="uniqueId + '_video-input'"
          multiple="multiple"
          accept="video/*"
          type="file"
          style="position: absolute; opacity: 0; width: 0.1px; height: 0.1px; overflow: hidden; z-index: -1;"
        />
      </v-card>
    </v-col>
  </v-row>
</template>

<script>
import utils from "@/utils"

export default {
  name: "VideosField",
  props: {
    videoArray: {
      type: Array,
      required: true
    }
  },
  computed: {
    uniqueId() {
      return this.uid
    }
  },
  methods: {
    emitChange() {
      this.$emit("change", this.videoArray)
    },
    deleteVideo(index) {
      this.videoArray.splice(index, 1)
      this.emitChange()
    },
    addVideo(e) {
      if (!e) return
      const files = e.target.files
      this.emitChange()

      for (let i = 0; i < files.length; i++) {
        const file = files[i]
        utils.toBase64(file, base64 => {
          this.videoArray.push({
            video: base64,
            label: ""
          })
        })
      }
    }
  },
  mounted() {
    if (this.$el) {
      const domElement = this.$el.querySelector(
        "#" + this.uniqueId + "_video-input"
      )
      domElement.addEventListener("change", this.addVideo)
    }
  },
  beforeDestroy() {
    this.$el
      .querySelector("#" + this.uniqueId + "_video-input")
      .removeEventListener("change", this.addVideo)
  }
}
</script>