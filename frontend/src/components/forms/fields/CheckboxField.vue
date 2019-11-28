<template>
  <div>
    <v-checkbox
      class="ma-0 pa-0"
      color="primary"
      v-for="(item, index) in checkboxItems"
      v-model="checkboxModels[index]"
      :key="index"
      :label="item.text"
      :value="item.value"
      @change="updateState()"
    ></v-checkbox>
  </div>
</template>

<script>
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
      if (
        this.storeDataName &&
        this.$store.state[this.storeDataName] &&
        this.$store.state[this.storeDataName][this.id]
      )
        storeData = this.$store.state[this.storeDataName][this.id]

      return this.checkboxItems.map(x => {
        if (storeData.indexOf(x.value) != -1) return x.value
      })
    },
    checkboxItems() {
      if (this.options && this.options.dataSource)
        return this.options.dataSource
      if (this.options && this.options.enum)
        return this.options.enum.map(x => {
          return { text: x, value: x }
        })
      if (this.schema.enum)
        return this.schema.enum.map(x => {
          return { text: x, value: x }
        })
      return []
    }
  },
  methods: {
    updateState() {
      let newValue = this.checkboxModels.filter(x => !!x)
      if (this.updateActionName)
        this.$store.dispatch(this.updateActionName, {
          fieldId: this.id,
          fieldValue: newValue
        })
    }
  },
}
</script>

<style>
.ma-0.pa-0.v-input--checkbox .v-input__slot {
  margin: 0;
}
</style>