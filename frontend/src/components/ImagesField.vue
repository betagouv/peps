<template>
  <v-row>
    <v-col
      v-for="(image, index) in imageArray"
      :key="index"
      class="d-flex child-flex"
      cols="12"
      sm="6"
      md="4"
    >
      <v-card flat class="d-flex flex-column fill-height">
        <v-img :src="image.image" aspect-ratio="1.4" class="grey lighten-2"></v-img>
        <div style="position: absolute; top: 10px; left: 10px;">
          <v-btn fab small @click="deleteImage(index)">
            <v-icon color="red">mdi-trash-can-outline</v-icon>
          </v-btn>
        </div>
        <v-text-field
          hide-details="auto"
          class="caption"
          v-model="image.label"
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
          :for="uniqueId + '_image-input'"
          style="width: 100%; height: 100%; cursor: pointer;"
        >
          <v-icon class="align-center">mdi-camera</v-icon>
          <div class="subtitle-2">Ajoutez des images</div>
        </label>
        <input
          :id="uniqueId + '_image-input'"
          multiple="multiple"
          accept="image/*"
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
  name: "ImagesField",
  props: {
    imageArray: {
      type: Array,
      required: true
    }
  },
  computed: {
    uniqueId() {
      return this.uid 
    },
  },
  methods: {
    emitChange() {
      this.$emit("change", this.imageArray)
    },
    deleteImage(index) {
      this.imageArray.splice(index, 1)
      this.emitChange()
    },
    addImages(e) {
      if (!e) return
      const files = e.target.files
      this.emitChange()

      for (let i = 0; i < files.length; i++) {
        const file = files[i]
        utils.toBase64(file, base64 => {
          this.imageArray.push({
            image: base64,
            label: ""
          })
        })
      }
    },
  },
  mounted() {
    if (this.$el) {
      const domElement = this.$el.querySelector('#' + this.uniqueId + '_image-input')
      domElement.addEventListener("change", this.addImages)
    }
  },
  beforeDestroy() {
    this.$el
      .querySelector('#' + this.uniqueId + '_image-input')
      .removeEventListener("change", this.addImages)
  }
}
</script>