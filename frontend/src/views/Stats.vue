<template>
  <div>
    <Title :title="title" :breadcrumbs="breadcrumbs" />
    <v-container class="constrained">
      <iframe
          src="http://peps-metabase.cleverapps.io/public/dashboard/00536261-3e78-4d92-aa9b-a5996c5bf8fb"
          style="border: 1px solid rgb(204, 204, 204);box-shadow: 3px 3px 7px -3px #999;"
          width="100%"
          height="1100"
          allowtransparency
      ></iframe>
    </v-container>
  </div>
</template>

<script>
import Title from "@/components/Title.vue"

export default {
  name: "Stats",
  components: { Title },
  metaInfo() {
    return {
      title: "Peps - Statistiques",
      meta: [{ description: 'Les statistiques de Peps' }]
    }
  },
  data() {
    return {
      title: "Statistiques",
      breadcrumbs: [
        {
          text: "Accueil",
          disabled: false,
          to: { name: "Landing" }
        },
        {
          text: "Statistiques",
          disabled: true
        }
      ],
    }
  }
}
</script>
