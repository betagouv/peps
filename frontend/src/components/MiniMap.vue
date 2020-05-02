<template>
  <div style="width: 100%;">
    <v-img
      :width="size"
      style="margin-left: auto; margin-right: auto;"
      src="/static/images/hexagone.png"
    >
      <div
        class="minimap-pin"
        :style="`left: ${pinLocation.x}px; top: ${pinLocation.y}px; width: ${pinSize}px; height: ${pinSize}px;`"
      ></div>
    </v-img>
  </div>
</template>

<script>
export default {
  name: "MiniMap",
  data() {
    return {
      pinSize: 10
    }
  },
  props: {
    lat: {
      type: Number
    },
    lon: {
      type: Number
    },
    size: {
      type: Number,
      default: 130
    }
  },
  computed: {
    pinLocation() {
      if (!this.lat || !this.lon)
        return {x: 0, y: 0}

      const width = this.size
      const height = this.size
      const topLatitude = 51.16
      const bottomLatitude = 42.093
      const leftLongitude = -4.881
      const rightLongitude = 8.432

      const top = topLatitude * (Math.PI / 180)
      const bottom = bottomLatitude * (Math.PI / 180)
      const right = rightLongitude * (Math.PI / 180)
      const left = leftLongitude * (Math.PI / 180)
      const latitude = this.lat * (Math.PI / 180)
      const longitude = this.lon * (Math.PI / 180)

      const ymin = Math.log(Math.tan((bottom / 2) + (Math.PI / 4)));
      const ymax = Math.log(Math.tan((top / 2) + (Math.PI / 4)));
      const xfactor = width / (right - left);
      const yfactor = height / (ymax - ymin);

      const x = (longitude - left) * xfactor;
      const y = (ymax - Math.log(Math.tan((latitude / 2) + (Math.PI / 4)))) * yfactor;

      return {x: x - this.pinSize / 2, y: y - this.pinSize / 2}
    }
  }
}
</script>

<style scoped>
.minimap-pin {
  background-color: #f15f6e;
  border: 1px solid #c12838;
  position: absolute;
  border-radius: 50%;
}
</style>