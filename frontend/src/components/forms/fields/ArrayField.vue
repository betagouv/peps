<template>
  <div>
    <v-select :items="items" dense outlined label="array field"></v-select>
  </div>
</template>

<script>
export default {
  name: "ArrayField",
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
      return ["Foo", "Bar"];
    }
  }
};
</script>