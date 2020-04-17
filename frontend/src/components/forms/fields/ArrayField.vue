<template>
  <div>
    <v-row no-gutters style="margin-bottom: 10px;">
      <v-select
        solo
        :items="items"
        v-model="selected"
        item-text="text"
        item-value="value"
        label="Selectionnez..."
        style="margin-right: 15px;"
      ></v-select>

      <v-btn rounded large @click="addCulture(selected)" :disabled="!selected">
        <v-icon small style="margin-right: 10px;">mdi-plus-circle</v-icon>Ajouter
      </v-btn>
    </v-row>

    <div class="culture-container" v-if="cultures.length > 0">
      <v-card class="culture-card" v-for="(culture, index) in cultures" :key="index">
        <v-btn icon fab small style="margin-right: 5px" @click="removeCulture(index)">
          <v-icon>mdi-trash-can-outline</v-icon>
        </v-btn>
        {{ getText(culture) }}
      </v-card>
    </div>
  </div>
</template>

<script>
export default {
  name: "ArrayField",
  data() {
    return {
      cultures: this.$store.state[this.storeDataName] ? (this.$store.state[this.storeDataName][this.id] || []) : [],
      selected: null
    }
  },
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
    items() {
      if (this.options && this.options.items && this.options.items.dataSource)
        return this.options.items.dataSource
      return []
    }
  },
  methods: {
    addCulture(selected) {
      this.cultures.push(selected)
      this.updateValue()
    },
    removeCulture(index) {
      this.cultures.splice(index, 1)
      this.updateValue()
    },
    getText(value) {
      return this.items.find(x => x.value === value).text
    },
    updateValue() {
      this.$store.dispatch(this.updateActionName, {
        fieldId: this.id,
        fieldValue: this.cultures
      })
    }
  }
}
</script>

<style scoped>
.v-text-field__details {
  display: none;
}
.culture-card {
  padding: 10px;
  margin: 10px;
}
.culture-container {
  margin-top: 10px;
  margin-bottom: 10px;
  border: solid 1px #e0e0e0;
  border-radius: 5px;
  background: #f0f0f0;
}
</style>
