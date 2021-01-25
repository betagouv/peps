<template>
  <div>
    <v-form
      lazy-validation
      @submit="onSubmit"
      id="mailchimpform"
      ref="form"
      action="https://gouv.us3.list-manage.com/subscribe/post?u=d220b6a57be23c698418d7a35&amp;id=9c06c2f16a"
      method="post"
      name="mc-embedded-subscribe-form"
      target="_blank"
    >
      <!-- automatically assign to newsletter group-->
      <div style="display: none">
        <ul>
          <li>
            <input
              type="checkbox"
              value="4"
              name="group[26845][4]"
              id="mce-group[26845]-26845-2"
              checked
            /><label for="mce-group[26845]-26845-2">Newsletter</label>
          </li>
        </ul>
      </div>
      <!-- real people should not fill this in and expect good things - do not remove this or risk form bot signups-->
      <div style="position: absolute; left: -5000px" aria-hidden="true">
        <input
          type="text"
          name="b_d220b6a57be23c698418d7a35_9c06c2f16a"
          tabindex="-1"
          value=""
        />
      </div>
      <v-row>
        <v-col cols="12" sm="6">
          <v-text-field
            type="email"
            label="Votre adresse email"
            outlined
            validate-on-blur
            hide-details="auto"
            dense
            value=""
            :rules="[validators.isEmail]"
            name="EMAIL"
            id="mce-EMAIL"
          ></v-text-field>
        </v-col>
        <v-col cols="auto">
          <v-btn type="submit" height="40px" color="primary" class="text-none" form="mailchimpform">
            Recevoir les témoignages
          </v-btn>
        </v-col>
      </v-row>
    </v-form>
  </div>
</template>

<script>
import validators from "@/validators"

export default {
  name: "MailChimpForm",
  methods: {
    onSubmit() {
      window.sendTrackingEvent(this.$route.name, "newsletter", "subscribe")
      return this.$refs.form.validate()
    }
  },
  computed: {
    validators() {
      return validators
    },
  },
}
</script>