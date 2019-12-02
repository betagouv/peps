<template>
  <div>
    <v-text-field
      :placeholder="placeholder"
      :prepend-icon="icon"
      v-model="text"
      class="ma-0 pa-0"
      outlined
      solo
      dense
      flat
    ></v-text-field>
  </div>
</template>

<script>
export default {
  name: "TextField",
  props: {
    id: {
      type: String,
      required: true
    },
    schema: {
      type: Object,
      required: true
    },
    options: {
      type: Object
    },
    storeDataName: {
      type: String
    },
    updateActionName: {
      type: String
    }
  },
  computed: {
    text: {
      get() {
        if (this.storeDataName && this.$store.state[this.storeDataName] && this.$store.state[this.storeDataName][this.id])
          return this.$store.state[this.storeDataName][this.id]
        return undefined
      },
      set(value) {
        if (this.updateActionName)
          this.$store.dispatch(this.updateActionName, { fieldId: this.id, fieldValue: value })
      }
    },
    placeholder() {
      if (this.options && this.options.placeholder)
        return this.options.placeholder;
      if (this.schema.placeholder) return this.schema.placeholder;
      return "";
    },
    icon() {
      if (this.options && this.options.mdiIcon)
        return this.options.mdiIcon
      return undefined
    }
  }
};
</script>