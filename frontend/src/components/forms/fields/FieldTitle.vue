<template>
    <p class="title">{{title}}</p>
</template>

<script>
export default {
  name: "FieldTitle",
  props: {
    title: {
      type: String
    }
  }
};
</script>