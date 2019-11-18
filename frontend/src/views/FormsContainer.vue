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
    </div>
  </div>
</template>

<script>
import store from "@/store/index";
import Loader from "@/components/Loader.vue";
import Form from "@/components/forms/Form.vue";
import Constants from "@/constants";

export default {
  name: "FormsContainer",
  components: { Loader, Form },
  data() {
    return {
      loadingTitle: "Juste un instant..."
    };
  },
  computed: {
    loading: () =>
      store.state.formDefinitionsLoadingStatus ===
      Constants.LoadingStatus.LOADING,
    miaFormDefinition: () => store.state.miaFormDefinition,
    statsFormDefinition: () => store.state.statsFormDefinition,
    contactFormDefinition: () => store.state.contactFormDefinition,
    shouldShowMiaForm: () => true,
    shouldShowStatsForm: () => true,
    shouldShowContactForm: () => true
  }
};
</script>
