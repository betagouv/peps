<template>
  <div>
    <v-divider style="margin-bottom: 25px;" />

    <div style="text-align:center;">
      <a href="https://www.beta.gouv.fr/apropos/" target="_blank" style="text-align: center; margin-bottom: 12px;">
        <img src="/static/images/betagouv.png" style="height:35px; opacity:0.5;" />
      </a>

      <div
        class="d-flex flex-no-wrap justify-space-between"
        style="color: #777; text-align: center; max-width: 450px; margin-left: auto; margin-right: auto;"
      >
        <img src="/static/images/minagri.png" class="ma-3" height='70px' style="opacity:0.5;" />
        <div
          class="caption fill-height ma-3"
          style="text-align: left;"
        >Peps est un service proposé par le Ministère de l'Agriculture et de l'Alimentation dans le cadre du plan Ecophyto
        <br /> <a href="/#/qui-sommes-nous" target="_blank">En savoir plus</a>
        </div>
      </div>

      <div
        class="caption ma-2"
        style="color: #777; text-align: center;"
      >{{ new Date().getFullYear() }} — Peps</div>
      <div class="caption" style="color: #777; text-align: center;">
        <a href="/#/politique-de-confidentialite">Politique de confidentialité</a>
      </div>
      <div style="text-align: center; margin-bottom: 20px;">
        <v-btn icon class="mx-2" href="https://twitter.com/pepsagriculture" target="_blank">
          <v-icon size="24px">mdi-twitter</v-icon>
        </v-btn>
        <v-btn icon class="mx-2" href="https://www.facebook.com/pepsagriculture/" target="_blank">
          <v-icon size="24px">mdi-facebook-box</v-icon>
        </v-btn>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: "Footer"
}
</script> 