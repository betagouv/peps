<template>
  <div id="farmer-edit">
    <Loader v-if="updateInProgress" title="Juste un instant..." :loading="updateInProgress" />
    <Title :breadcrumbs="breadcrumbs" />

    <v-container class="constrained">
      <v-app-bar
        style="margin-left: auto; margin-right: auto;"
        max-width="1000"
        color="white"
        :elevation="toolbarOnTop ? 2 : 0"
        :fixed="toolbarOnTop"
        id="button-toolbar"
      >
        <v-toolbar-title class="primary--text"></v-toolbar-title>
        <v-spacer></v-spacer>
        <v-btn
          :small="$vuetify.breakpoint.name === 'xs'"
          style="margin-right: 10px;"
          @click="cancelEdit"
          class="text-none"
        >
          <v-icon :small="$vuetify.breakpoint.name === 'xs'">mdi-arrow-left</v-icon>
          <span v-if="$vuetify.breakpoint.name !== 'xs'">Annuler</span>
        </v-btn>

        <v-btn
          :small="$vuetify.breakpoint.name === 'xs'"
          class="text-none"
          :disabled="!hasChanged"
          color="primary"
          @click="updateFarmer"
        >
          <v-icon :small="$vuetify.breakpoint.name === 'xs'">mdi-content-save</v-icon>Sauvegarder
        </v-btn>
      </v-app-bar>

      <v-form ref="form" v-model="formIsValid">
        <v-row>
          <v-col class="justify-center justify-sm-start d-flex" cols="12" sm="3" md="2">
            <!-- PROFILE IMAGE -->
            <div class="field">
              <div style="position: relative; margin-left: 10px; margin-top: 10px;">
                <v-avatar size="120" style="border: solid 3px #CCC">
                  <v-img v-if="dummyFarmer.profile_image" :src="dummyFarmer.profile_image"></v-img>
                  <v-icon size="80" v-else>mdi-account</v-icon>
                </v-avatar>

                <div style="position: absolute; top: -10px;">
                  <v-btn
                    v-if="dummyFarmer.profile_image"
                    fab
                    small
                    @click="changeProfileImage(undefined)"
                  >
                    <v-icon color="red">mdi-trash-can-outline</v-icon>
                  </v-btn>
                </div>
              </div>

              <v-btn
                class="text-none"
                outlined
                color="primary"
                style="margin-top: 10px"
                @click="onProfilePhotoUploadClick"
                small
              >Choisir une photo</v-btn>
              <input
                ref="uploader"
                class="d-none"
                type="file"
                accept="image/*"
                @change="onProfilePhotoChanged"
              />
            </div>
          </v-col>
          <v-col cols="12" sm="9" md="10" class="d-flex flex-column">
            <!-- NAME -->
            <div class="field" style="margin-bottom: 5px;">
              <div class="field-title title">
                Votre prénom et nom
                <span class="mandatory">- obligatoire</span>
              </div>
              <v-text-field
                hide-details="auto"
                :rules="[validators.notEmpty]"
                @input="hasChanged = true"
                outlined
                dense
                v-model="dummyFarmer.name"
              ></v-text-field>
            </div>

            <!-- EMAIL (READONLY) -->
            <div class="field" style="margin-bottom: 0px;">
              <v-text-field
                hide-details="auto"
                outlined
                disabled
                dense
                background-color="#EFEFEF"
                messages="Cette information n'est pas modifiable. Si elle n'est pas correcte, contactez nous pour la changer"
                :value="dummyFarmer.email"
              ></v-text-field>
            </div>
          </v-col>
        </v-row>

        <!-- PHONE NUMBER -->
        <div class="field">
          <div class="field-title title">
            Votre numéro téléphone
            <span class="mandatory">- obligatoire</span>
          </div>
          <v-text-field
            hide-details="auto"
            @input="hasChanged = true"
            outlined
            dense
            v-model="dummyFarmer.phone_number"
            style="max-width: 200px;"
          ></v-text-field>
        </div>

        <!-- CONTACT POSSIBLE -->

        <div class="field">
          <div class="field-title title">
            Contact
            <span class="mandatory">- obligatoire</span>
          </div>
          <v-checkbox
            @click.native="hasChanged = true"
            v-model="dummyFarmer.contact_possible"
            label="J'accepte d'être contacté par des utilisateurs de Peps qui souhaitent en savoir plus sur mes témoignages"
          ></v-checkbox>
        </div>

        <!-- EMAIL POSSIBLE -->

        <div class="field">
          <div class="field-title title">
            Email
            <span class="mandatory"></span>
          </div>
          <v-checkbox
            @click.native="hasChanged = true"
            v-model="dummyFarmer.email_for_messages_allowed"
            label="J'accepte de revoir un email pour me notifier d'un nouveau message envoyé par un utilisateur sur Peps"
          ></v-checkbox>
        </div>

        <!-- GROUPS -->

        <div class="field">
          <div class="field-title title">Appartenez-vous à des groupes ?</div>
          <div class="field-helper subtitle-2">Vous pouvez en sélectionner plusieurs</div>

          <v-checkbox
            @click.native="hasChanged = true"
            v-model="dummyFarmer.groups"
            label="DEPHY"
            value="DEPHY"
          ></v-checkbox>
          <v-checkbox
            @click.native="hasChanged = true"
            v-model="dummyFarmer.groups"
            label="GIEE"
            value="GIEE"
          ></v-checkbox>
          <v-checkbox
            @click.native="hasChanged = true"
            v-model="dummyFarmer.groups"
            label="30000"
            value="30000"
          ></v-checkbox>
          <v-checkbox
            @click.native="hasChanged = true"
            v-model="dummyFarmer.groups"
            label="CETA"
            value="CETA"
          ></v-checkbox>
          <v-checkbox
            @click.native="hasChanged = true"
            v-model="dummyFarmer.groups"
            label="Groupe de coopérative"
            value="Groupe de coopérative"
          ></v-checkbox>
          <v-checkbox
            @click.native="hasChanged = true"
            v-model="dummyFarmer.groups"
            label="Groupe de négoce"
            value="Groupe de négoce"
          ></v-checkbox>
          <v-checkbox
            @click.native="hasChanged = true"
            v-model="dummyFarmer.groups"
            label="Groupe de chambre d'agriculture"
            value="Groupe de chambre d'agriculture"
          ></v-checkbox>
          <v-checkbox
            @click.native="hasChanged = true"
            v-model="dummyFarmer.groups"
            label="Groupe de voisins"
            value="Groupe de voisins"
          ></v-checkbox>
          <v-checkbox
            @click.native="hasChanged = true"
            v-model="dummyFarmer.groups"
            label="CUMA"
            value="CUMA"
          ></v-checkbox>
          <v-checkbox
            @click.native="hasChanged = true"
            v-model="dummyFarmer.groups"
            label="Civam"
            value="Civam"
          ></v-checkbox>
          <v-checkbox
            @click.native="hasChanged = true"
            v-model="dummyFarmer.groups"
            label="Autre"
            value="Autre"
          ></v-checkbox>
        </div>
      </v-form>
    </v-container>

    <v-overlay :value="updateSucceeded || updateFailed" :dark="false">
      <div>
        <v-btn @click="closeOverlay()" class="close-overlay" fab dark small color="grey lighten-5">
          <v-icon color="red darken-3">mdi-close</v-icon>
        </v-btn>
        <v-card :style="'max-width: 600px;'" class="overflow-y-auto">
          <v-card-text style="padding: 30px; color: #333;">
            <span v-if="updateSucceeded">
              <v-icon style="margin-top: -3px; margin-right: 5px;">mdi-check-circle</v-icon>
              <span v-if="farmerUrlComponent">Votre profil a bien été mis à jour !</span>
              <span v-else>Votre profil a bien été créé ! Notre équipe la mettra en ligne bientôt.</span>
            </span>
            <span v-else>
              <v-icon style="margin-top: -3px; margin-right: 5px;">mdi-emoticon-sad-outline</v-icon>Oops ! On n'a pas pu mettre à jour votre profil. Veuillez essayer plus tard.
            </span>
          </v-card-text>
          <div style="padding: 10px; text-align: right">
            <v-btn
              class="text-none body-1 practice-buttons"
              color="primary"
              @click="closeOverlay()"
              rounded
            >OK</v-btn>
          </div>
        </v-card>
      </div>
    </v-overlay>
  </div>
</template>

<script>
import Title from "@/components/Title.vue"
import validators from "@/validators"
import utils from "@/utils"
import Loader from "@/components/Loader.vue"
import Constants from "@/constants"

export default {
  name: "PersonalInfoEditor",
  components: { Title, Loader },
  metaInfo() {
    return {
      title: "Peps - Mettez à jour vos données personnelles",
      meta: [
        {
          description:
            "Modifiez vos données personnelles et votre information de contact",
        },
      ],
    }
  },
  props: {
    farmerUrlComponent: {
      type: String,
      default: null,
    },
  },
  data() {
    return {
      dummyFarmer: {
        groups: [],
      },
      hasChanged: false,
      formIsValid: true,
      toolbarOnTop: false,
      initialToolbarTop: 0,
    }
  },
  computed: {
    updateInProgress() {
      return (
        this.$store.state.farmerEditLoadingStatus ==
        Constants.LoadingStatus.LOADING
      )
    },
    updateSucceeded() {
      return (
        this.$store.state.farmerEditLoadingStatus ===
        Constants.LoadingStatus.SUCCESS
      )
    },
    updateFailed() {
      return (
        this.$store.state.farmerEditLoadingStatus ===
        Constants.LoadingStatus.ERROR
      )
    },
    validators() {
      return validators
    },
    farmer() {
      if (!this.farmerUrlComponent) return undefined
      return this.$store.getters.farmerWithUrlComponent(this.farmerUrlComponent)
    },
    breadcrumbs() {
      return [
        {
          text: "Accueil",
          disabled: false,
          to: { name: "Landing" },
        },
        {
          text: "Mon compte",
          disabled: false,
          to: { name: "Profile" },
        },
        {
          text: this.farmer ? this.farmer.name : "Nouveau profil",
          disabled: true,
        },
      ]
    },
  },
  methods: {
    updateFarmer() {
      this.$refs.form.validate()

      if (!this.formIsValid) {
        window.scrollTo(0, 0)
        window.alert("Merci de vérifier les champs en rouge et réessayer")
        return
      }

      if (this.farmer) {
        const payload = utils.getObjectDiff(this.farmer, this.dummyFarmer)

        this.$store.dispatch("patchFarmer", {
          farmer: this.farmer,
          changes: payload,
        })
      } else {
        // Create farmer
      }
    },
    closeOverlay() {
      const success = this.updateSucceeded
      this.$store.dispatch("resetFarmerEditLoadingStatus")
      if (success)
        this.$router.push({
          name: "Profile",
        })
      else this.resetMediaFields()
    },
    cancelEdit() {
      this.$router.go(-1)
    },
    resetdummyFarmer() {
      if (this.farmer)
        this.dummyFarmer = JSON.parse(JSON.stringify(this.farmer))
    },
    resetMediaFields() {
      this.dummyFarmer.profile_image = this.farmer
        ? JSON.parse(JSON.stringify(this.farmer.profile_image))
        : null
    },

    changeProfileImage(file) {
      this.hasChanged = true
      if (!file) {
        this.dummyFarmer.profile_image = undefined
        return
      }
      utils.toBase64(file, (base64) => {
        this.dummyFarmer.profile_image = base64
      })
    },
    onProfilePhotoUploadClick() {
      this.$refs.uploader.click()
    },
    onProfilePhotoChanged(e) {
      if (e && e.target && e.target.files && e.target.files.length > 0) {
        this.changeProfileImage(e.target.files[0])
      } else {
        this.changeProfileImage(undefined)
      }
    },
    handleUnload(e) {
      if (this.hasChanged) {
        e.preventDefault()
        e.returnValue = ""
      } else {
        delete e["returnValue"]
      }
    },
    onScroll() {
      this.toolbarOnTop = window.scrollY > this.initialToolbarTop
    },
  },
  watch: {
    updateSucceeded(newValue) {
      if (newValue) this.hasChanged = false
    },
    updateFailed(newValue) {
      if (newValue) this.hasChanged = false
    },
  },
  beforeMount() {
    this.resetdummyFarmer()
  },
  mounted() {
    window.addEventListener("beforeunload", this.handleUnload)
    this.initialToolbarTop =
      this.$el.querySelector("#button-toolbar").offsetTop || 0
  },
  created() {
    window.addEventListener("scroll", this.onScroll)
  },
  beforeDestroy() {
    window.removeEventListener("scroll", this.onScroll)
    window.removeEventListener("beforeunload", this.handleUnload)
  },
  beforeRouteLeave(to, from, next) {
    if (!this.hasChanged) {
      next()
      return
    }

    const answer = window.confirm(
      "Êtes-vous sûr de vouloir quitter cette page ? Vous avez des changements non-sauvegardés"
    )
    if (answer) {
      next()
    } else {
      next(false)
    }
  },
}
</script>

<style scoped>
.v-input--checkbox {
  margin-top: 0;
  padding-top: 0;
}
</style>

<style>
.v-input--checkbox .v-input__slot {
  margin-bottom: 0;
}
</style>
