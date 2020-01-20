<template>
  <div>
    <v-container class="pa-0">
      <InfoWell
        v-if="!!schema.description"
        :description="schema.description"
        style="margin-bottom: 10px;"
      />
      <div v-for="(value, name) in visibleFieldsSchema" :key="name">
        <FieldTitle :title="getTitle(name)" v-if="getTitle(name)" />
        <RadioField
          v-if="getType(name) == 'radio'"
          :schema="value"
          :options="getOptions(name)"
          :id="name"
          :updateActionName="updateActionName"
          :storeDataName="storeDataName"
        />
        <CheckboxField
          v-if="getType(name) == 'checkbox'"
          :schema="value"
          :options="getOptions(name)"
          :id="name"
          :storeDataName="storeDataName"
          :updateActionName="updateActionName"
        />
        <ArrayField
          v-if="getType(name) == 'array'"
          :schema="value"
          :options="getOptions(name)"
          :id="name"
          :updateActionName="updateActionName"
          :storeDataName="storeDataName"
        />
        <TextField
          v-if="getType(name) == 'string'"
          :schema="value"
          :options="getOptions(name)"
          :id="name"
          :updateActionName="updateActionName"
          :storeDataName="storeDataName"
        />
        <SelectField
          v-if="getType(name) == 'select'"
          :schema="value"
          :options="getOptions(name)"
          :id="name"
          :updateActionName="updateActionName"
          :storeDataName="storeDataName"
        />
      </div>
    </v-container>
  </div>
</template>

<script>
import formutils from "@/formutils"
import InfoWell from "@/components/InfoWell.vue"
import RadioField from "@/components/forms/fields/RadioField.vue"
import CheckboxField from "@/components/forms/fields/CheckboxField.vue"
import ArrayField from "@/components/forms/fields/ArrayField.vue"
import SelectField from "@/components/forms/fields/SelectField.vue"
import TextField from "@/components/forms/fields/TextField.vue"
import FieldTitle from "@/components/forms/fields/FieldTitle.vue"

export default {
  name: "Form",
  components: {
    InfoWell,
    RadioField,
    CheckboxField,
    ArrayField,
    SelectField,
    TextField,
    FieldTitle
  },
  props: {
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
    visibleFieldsSchema() {
      let visibleSchemaFields = {}
      let data = this.$store.state[this.storeDataName]
      let visibleFields = formutils.getVisibleFields(
        this.schema,
        this.options,
        data
      )

      for (let i = 0; i < visibleFields.length; i++) {
        let name = visibleFields[i]
        visibleSchemaFields[name] = this.schema.properties[name]
      }
      return visibleSchemaFields
    }
  },
  methods: {
    getType(name) {
      if (this.schema.properties[name] && this.schema.properties[name].type)
        return this.schema.properties[name].type
      if (
        this.options &&
        this.options.fields[name] &&
        this.options.fields[name].type
      )
        return this.options.fields[name].type
    },
    getTitle(name) {
      if (this.schema.properties[name] && this.schema.properties[name].title)
        return this.schema.properties[name].title
      return null
    },
    getOptions(name) {
      if (this.options && this.options.fields && this.options.fields[name])
        return this.options.fields[name]
    }
  }
}
</script>
