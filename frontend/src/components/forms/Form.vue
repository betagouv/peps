<template>
  <v-card>
    <v-container>
      <FormInfo
        v-if="!!schema.description"
        :description="schema.description"
        style="margin-bottom: 10px;"
      />
      <div v-for="(value, name) in schema.properties" :key="name">
        <FieldTitle :title="getTitle(name)" />
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
  </v-card>
</template>

<script>
import FormInfo from "@/components/forms/FormInfo.vue";
import RadioField from "@/components/forms/fields/RadioField.vue";
import CheckboxField from "@/components/forms/fields/CheckboxField.vue";
import ArrayField from "@/components/forms/fields/ArrayField.vue";
import SelectField from "@/components/forms/fields/SelectField.vue";
import TextField from "@/components/forms/fields/TextField.vue";
import FieldTitle from "@/components/forms/fields/FieldTitle.vue";

export default {
  name: "Form",
  components: {
    FormInfo,
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
    data: {
      type: Object
    },
    storeDataName: {
      type: String
    },
    updateActionName: {
      type: String
    }
  },
  methods: {
    getType(name) {
      if (this.schema.properties[name] && this.schema.properties[name].type)
        return this.schema.properties[name].type;
      if (
        this.options &&
        this.options.fields[name] &&
        this.options.fields[name].type
      )
        return this.options.fields[name].type;
      return undefined;
    },
    getTitle(name) {
      if (this.schema.properties[name] && this.schema.properties[name].title)
        return this.schema.properties[name].title;
      return name;
    },
    getOptions(name) {
      if (this.options && this.options.fields && this.options.fields[name])
        return this.options.fields[name];
      return undefined;
    },
    getData(name) {
      if (this.data && this.data[name]) return this.data[name];
      return undefined;
    }
  }
};
</script>
