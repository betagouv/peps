<template>
  <div>
    <v-checkbox
      class="ma-0 pa-0"
      v-for="(item, index) in checkboxItems"
      v-model="checkboxModels[index]"
      :key="index"
      :label="item.text"
      :value="item.value"
      @click="updateValue"
    ></v-checkbox>
  </div>
</template>

<script>
import store from "@/store/index";

export default {
  name: "CheckboxField",
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
    checkboxModels() {
      let storeData = []
      if (this.storeDataName && store.state[this.storeDataName] && store.state[this.storeDataName][this.id])
        storeData = store.state[this.storeDataName][this.id]

      return this.checkboxItems.map(x => {
        if (storeData.indexOf(x.value) != -1)
          return x.value
        return undefined
      })
    },
    checkboxItems() {
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
  },
  methods: {
    updateValue() {
      let newValue = this.checkboxModels.filter(x => !!x)
      if (this.updateActionName)
          store.dispatch(this.updateActionName, { fieldId: this.id, fieldValue: newValue })
    }
  }
};
</script>

<style>
.ma-0.pa-0.v-input--checkbox .v-input__slot {
    margin: 0;
}
</style>