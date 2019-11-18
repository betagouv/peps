<template>
  <div>
    <v-radio-group v-model="selected" :mandatory="false">
      <v-radio v-for="item in radioItems" :key="item.value" :label="item.text" :value="item.value"></v-radio>
    </v-radio-group>
  </div>
</template>

<script>

import store from "@/store/index";

export default {
  name: "RadioField",
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
    selected: {
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
    radioItems() {
      if (this.options && this.options.dataSource)
        return this.options.dataSource;
      if (this.options && this.options.enum)
        return this.options.enum.map(x => {
          return { text: x, value: x };
        });
      if (this.schema.enum)
        return this.schema.enum.map(x => {
          return { text: x, value: x };
        });
      return [];
    }
  }
};
</script>