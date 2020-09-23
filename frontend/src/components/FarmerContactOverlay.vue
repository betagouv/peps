<template>
  <div v-if="visible">
    <v-overlay :value="visible" :dark="false">
      <div>
        <v-btn @click="close()" class="close-overlay" fab dark small color="grey lighten-5">
          <v-icon color="red darken-3">mdi-close</v-icon>
        </v-btn>
        <v-card
          :style="'margin-left: 10px; margin-right: 10px; max-width: 600px; max-height:' + windowHeight + 'px'"
          class="overflow-y-auto"
        >
          <div v-if="step === 1">
            <v-card-title>1/2 Discuter avec {{ farmer.name }}</v-card-title>

            <v-card-text>
              <v-form ref="formStep1" v-model="form1IsValid">
                <v-text-field :rules="[validators.notEmpty]" label="Votre nom" outlined v-model="name"></v-text-field>
                <v-text-field :rules="[validators.notEmpty, validators.isEmail]" label="Votre email" outlined v-model="email"></v-text-field>
              </v-form>
              <div style="text-align: right;">
                <v-btn color="primary" text class="text-none" :href="`/login?next=/messages/${farmerUrlComponent}`">J'ai déjà utilisé Peps</v-btn>
                <v-btn class="text-none" color="primary" @click="submitStep1">Envoyer</v-btn>
              </div>
            </v-card-text>
          </div>
          <div v-if="step === 2">
            <v-card-title><v-btn icon @click="step = 1;"><v-icon>mdi-arrow-left</v-icon></v-btn> 2/2 Discuter avec {{ farmer.name }}</v-card-title>
            <v-card-text>
              Nous allons vous créer un compte avant de commencer la
              discussion. Rien de compliqué, uniquement un email qui vous sera
              envoyé pour vous connecter
              <v-form ref="formStep2" v-model="form2IsValid" :action="`/register?next=/messages/${farmerUrlComponent}`" method="post" @submit="submitStep2">
                <input type="hidden" name="csrfmiddlewaretoken" :value="csrfToken">
                <input type="hidden" :value="name" name="name">
                <input type="hidden" :value="email" name="email">
                <input type="hidden" :value="email" name="email2">
                <input type="hidden" value="" name="phone_number">
                <input type="hidden" :value="true" name="cgu_approved">
                <v-checkbox :v-model="cguApproved" :rules="[validators.notEmpty]">
                  <template v-slot:label>
                    <div>
                      J'ai lu et j'accepte les 
                      <a href="/conditions-generales-d-utilisation" class="d-inline" taget="_blank">
                      conditions d'utilisation
                      </a>
                    </div>
                  </template>
                </v-checkbox>
                <v-btn color="primary" type="submit" class="text-none">Créer mon compte</v-btn>
              </v-form>
            </v-card-text>
            <v-card-text>
              <v-sheet class="pa-2" color="#E0F4EE">
                <div class="font-weight-medium"><v-icon style="margin-right: 6px;">mdi-information</v-icon>Pourquoi dois-je créer un compte ?</div>
                <div style="padding-left: 30px;" class="caption">
                  {{farmer.name}} a très envie de discuter avec vous, beaucoup moins
                  avec des robots spammeurs... C'est uniquement pour ça qu'on vous
                  demande de créer un compte Peps.
                </div>
              </v-sheet>
            </v-card-text>
          </div>
        </v-card>
      </div>
    </v-overlay>
  </div>
</template>

<script>
import validators from "@/validators"

export default {
  name: "FarmerContactOverlay",
  data: () => ({
    windowHeight: window.innerHeight - 30,
    step: 1,
    name: '',
    email: '',
    form1IsValid: true,
    form2IsValid: true,
    cguApproved: false,
  }),
  props: {
    farmer: {
      type: Object,
      required: true,
    },
    visible: {
      type: Boolean,
      default: false,
    },
  },
  computed: {
    validators() {
      return validators
    },
    csrfToken() {
      return window.CSRF_TOKEN
    },
    farmerUrlComponent() { 
      return encodeURIComponent(this.$store.getters.farmerUrlComponent(this.farmer))
    }
  },
  mounted() {
    window.addEventListener("resize", this.onWindowResize)
    this.step = 1
  },
  beforeDestroy() {
    window.removeEventListener("resize", this.onWindowResize)
    this.step = 1
  },
  methods: {
    close() {
      this.$emit("done")
      this.step = 1
    },
    onWindowResize() {
      this.windowHeight = window.innerHeight - 30
    },
    submitStep1() {
      this.$refs.formStep1.validate()
      if (this.form1IsValid)
        this.step = 2
    },
    submitStep2() {
      console.log(`Send call ${this.name}, ${this.email}`)
      this.$refs.formStep2.validate()
      return this.form2IsValid
    }
  },
}
</script>
