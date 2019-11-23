<template>
  <div>
    <Loader v-if="!!loading" :title="loadingTitle" />
    <div v-else>
      <Form
        style="margin-bottom: 10px;"
        v-if="shouldShowMiaForm"
        :schema="miaFormDefinition.schema"
        :options="miaFormDefinition.options"
        updateActionName="addMiaFormData"
        storeDataName="miaFormData"
      />
      <Form
        style="margin-bottom: 10px;"
        v-if="shouldShowStatsForm"
        :schema="statsFormDefinition.schema"
        :options="statsFormDefinition.options"
        updateActionName="addStatsFormData"
        storeDataName="statsFormData"
      />
      <Form
        style="margin-bottom: 10px;"
        v-if="shouldShowContactForm"
        :schema="contactFormDefinition.schema"
        :options="contactFormDefinition.options"
        updateActionName="addContactFormData"
        storeDataName="contactFormData"
      />
      <FormSubmit />
    </div>
  </div>
</template>

<script>
import Loader from "@/components/Loader.vue";
import Form from "@/components/forms/Form.vue";
import Constants from "@/constants";
import FormSubmit from "@/components/FormSubmit.vue";

export default {
  name: "FormsContainer",
  components: { Loader, Form, FormSubmit },
  data() {
    return {
      loadingTitle: "Juste un instant..."
    };
  },
  computed: {
    loading() {
      return (
        this.$store.state.formDefinitionsLoadingStatus ===
        Constants.LoadingStatus.LOADING
      );
    },
    miaFormDefinition() {
      return this.$store.state.miaFormDefinition;
    },
    statsFormDefinition() {
      return this.$store.state.statsFormDefinition;
    },
    contactFormDefinition() {
      return this.$store.state.contactFormDefinition;
    },
    shouldShowMiaForm() {
      return true;
    },
    shouldShowStatsForm() {
      return true;
    },
    shouldShowContactForm() {
      return true;
    }
  }
};
</script>
