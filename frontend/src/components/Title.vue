<template>
  <div class="title-container">
    <v-container class="constrained">
      <v-breadcrumbs dark v-if="breadcrumbs" :items="desktopBreadcrumbs" class="body-1 pa-0 d-none d-sm-flex">
        <template v-slot:divider>
          <v-icon>mdi-chevron-right</v-icon>
        </template>
      </v-breadcrumbs>
      <v-breadcrumbs dark v-if="breadcrumbs" :items="mobileBreadcrumbs" class="body-1 pa-0 d-flex d-sm-none">
        <template v-slot:divider>
          <v-icon>mdi-chevron-right</v-icon>
        </template>
      </v-breadcrumbs>
      <div v-if="title" class="title font-weight-black" style="margin-top: 6px;">{{ title }}</div>
    </v-container>
  </div>
</template>

<script>
export default {
  name: "Resource",
  props: {
    title: {
      type: String,
      required: false
    },
    breadcrumbs: {
      type: Array
    }
  },
  methods: {
    goBack() {
      this.$router.go(-1)
    }
  },
  computed: {
    breakpoint() {
      return this.$vuetify.breakpoint
    },
    desktopBreadcrumbs() {
      if (!this.breadcrumbs)
        return []

      return this.breadcrumbs.map(breadcrumbItem => {
        return {
          text: breadcrumbItem.text,
          disabled: breadcrumbItem.disabled,
          to: breadcrumbItem.to,
          exact: true
        }
      })
    },
    mobileBreadcrumbs() {
      if (!this.breadcrumbs)
        return []

      const processMobileText = function(text) {
        const lengthLimit = 25
        const ending = '...'
        if (text.length > lengthLimit)
          return text.substring(0, lengthLimit - ending.length) + ending;
        return text
      }
      let mobileBreadcrumbs = this.breadcrumbs.map(breadcrumbItem => {
        return {
          text: processMobileText(breadcrumbItem.text),
          disabled: breadcrumbItem.disabled,
          to: breadcrumbItem.to,
          exact: true
        }
      })
      return mobileBreadcrumbs.slice(0, -1)
    },
  }
}
</script>

<style>
.v-breadcrumbs a.v-breadcrumbs__item {
  color: white;
}
</style>

<style scoped>
.title-container {
  background: #008763;
  padding-top: 7px;
  padding-bottom: 3px;
  color: white;
  box-shadow: inset 0px -11px 10px -15px #333;
}
.v-btn {
	float: left;
	margin-right: 10px;
	margin-top: -3px;
}
</style>
