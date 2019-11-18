<template>
  <div>
    <v-text-field
      :placeholder="placeholder"
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
import store from "@/store/index";

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
        if (this.storeDataName && store.state[this.storeDataName] && store.state[this.storeDataName][this.id])
          return store.state[this.storeDataName][this.id]
        return undefined
      },
      set(value) {
        if (this.updateActionName)
          store.dispatch(this.updateActionName, { fieldId: this.id, fieldValue: value })
      }
    },
    placeholder() {
      if (this.options && this.options.placeholder)
        return this.options.placeholder;
      if (this.schema.placeholder) return this.schema.placeholder;
      return "";
    }
  }
};
</script>