<template>
  <div>
    <v-select :items="selectItems" v-model="selected" item-text="text" item-value="value" dense outlined label="Selectionnez..."></v-select>
  </div>
</template>

<script>
import store from "@/store/index";

export default {
  name: "SelectField",
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
    selectItems() {
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