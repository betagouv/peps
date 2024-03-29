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
        <!-- FARM NAME -->
        <div class="field">
          <div class="field-title title">
            Le nom de votre exploitation
            <span class="mandatory">- obligatoire</span>
          </div>
          <v-text-field
            hide-details="auto"
            @input="hasChanged = true"
            outlined
            dense
            v-model="dummyFarmer.farm_name"
            :rules="[validators.notEmpty]"
          ></v-text-field>
        </div>

        <!-- PRODUCTIONS -->
        <div class="field">
          <div class="field-title title">
            Quelles productions sont présentes sur l'exploitation ?
            <span class="mandatory">- obligatoire</span>
          </div>
          <div class="field-helper">Vous pouvez en sélectionner plusieurs</div>
          <v-checkbox
            @click.native="hasChanged = true"
            v-model="dummyFarmer.production"
            label="Grandes cultures"
            value="Grandes cultures"
            hide-details
            :rules="[hasProductions]"
          ></v-checkbox>
          <v-checkbox
            @click.native="hasChanged = true"
            v-model="dummyFarmer.production"
            label="Cultures industrielles"
            value="Cultures industrielles"
            hide-details
            :rules="[hasProductions]"
          ></v-checkbox>
          <v-checkbox
            @click.native="hasChanged = true"
            v-model="dummyFarmer.production"
            label="Élevage allaitant"
            value="Élevage allaitant"
            hide-details
            :rules="[hasProductions]"
          ></v-checkbox>
          <v-checkbox
            @click.native="hasChanged = true"
            v-model="dummyFarmer.production"
            label="Élevage laitier"
            value="Élevage laitier"
            hide-details
            :rules="[hasProductions]"
          ></v-checkbox>
          <v-checkbox
            @click.native="hasChanged = true"
            v-model="dummyFarmer.production"
            label="Élevage engraissement"
            value="Élevage engraissement"
            hide-details
            :rules="[hasProductions]"
          ></v-checkbox>
          <v-checkbox
            @click.native="hasChanged = true"
            v-model="dummyFarmer.production"
            label="Élevage poule"
            value="Élevage poule"
            hide-details
            :rules="[hasProductions]"
          ></v-checkbox>
          <v-checkbox
            @click.native="hasChanged = true"
            v-model="dummyFarmer.production"
            label="Cultures légumières"
            value="Cultures légumières"
            hide-details
            :rules="[hasProductions]"
          ></v-checkbox>
          <v-checkbox
            @click.native="hasChanged = true"
            v-model="dummyFarmer.production"
            label="Vigne"
            value="Vigne"
            hide-details
            :rules="[hasProductions]"
          ></v-checkbox>
          <v-checkbox
            @click.native="hasChanged = true"
            v-model="dummyFarmer.production"
            label="Cultures spécialisées"
            value="Cultures spécialisées"
            hide-details
            :rules="[hasProductions]"
          ></v-checkbox>
          <v-checkbox
            @click.native="hasChanged = true"
            v-model="dummyFarmer.production"
            label="Apiculture"
            value="Apiculture"
            hide-details
            :rules="[hasProductions]"
          ></v-checkbox>
          <v-checkbox
            @click.native="hasChanged = true"
            v-model="dummyFarmer.production"
            label="Autre"
            value="Autre"
            :rules="[hasProductions]"
          ></v-checkbox>
        </div>

        <!-- INSTALLATION DATE -->

        <div class="field">
          <div class="field-title title">
            Quand vous êtes-vous installé sur l'exploitation ?
            <span class="mandatory">- obligatoire</span>
          </div>
          <div class="field-helper">Renseignez l'année (par exemple, 2001)</div>

          <v-text-field
            hide-details="auto"
            @input="onInstallationYearChange"
            :rules="[validators.isYear, validators.notEmpty]"
            outlined
            dense
            :value="installationYear"
          ></v-text-field>
        </div>

        <!-- POSTAL CODE -->

        <div class="field">
          <div class="field-title title">
            Le code postal de votre exploitation
            <span class="mandatory">- obligatoire</span>
          </div>
          <v-text-field
            hide-details="auto"
            :rules="[validators.notEmpty]"
            @input="hasChanged = true"
            outlined
            dense
            v-model="dummyFarmer.postal_code"
          ></v-text-field>
        </div>

        <!-- PERSONNEL -->

        <div class="field">
          <div class="field-title title">
            Combien de personnes travaillent sur l'exploitation à temps plein ?
            <span
              class="mandatory"
            >- obligatoire</span>
          </div>
          <div class="field-helper">Comptez-vous et vos associés, salariés et alternants</div>
          <v-text-field
            hide-details="auto"
            :rules="[validators.notEmpty]"
            @input="hasChanged = true"
            outlined
            dense
            v-model="dummyFarmer.personnel"
          ></v-text-field>
        </div>

        <!-- SURFACE -->
        <div>
          <div class="field parent-field">
            <div class="field-title title">
              La surface de votre exploitation (en ha.)
              <span class="mandatory">- obligatoire</span>
            </div>
            <v-text-field
              hide-details="auto"
              :rules="[validators.notEmpty]"
              @input="hasChanged = true"
              outlined
              dense
              v-model="dummyFarmer.surface"
            ></v-text-field>
          </div>

          <!-- SURFACE CULTURES -->

          <div class="field child-field">
            <div class="field-title subtitle-2">La surface en cultures (en ha.)</div>
            <v-text-field
              hide-details="auto"
              @input="hasChanged = true"
              outlined
              dense
              v-model="dummyFarmer.surface_cultures"
            ></v-text-field>
          </div>

          <!-- SURFACE MEADOWS -->

          <div class="field child-field">
            <div
              class="field-title subtitle-2"
            >La surface en prairie et cultures fourragères (en ha.)</div>
            <v-text-field
              hide-details="auto"
              @input="hasChanged = true"
              outlined
              dense
              v-model="dummyFarmer.surface_meadows"
            ></v-text-field>
          </div>
        </div>
        <!-- LIVESTOCK TYPES -->

        <div class="field">
          <div class="field-title title">Si vous avez de l'élevage, quel type d'élevage avez-vous ?</div>
          <v-checkbox
            @click.native="hasChanged = true"
            v-model="dummyFarmer.livestock_types"
            label="Bovin"
            value="Bovin"
          ></v-checkbox>
          <v-checkbox
            @click.native="hasChanged = true"
            v-model="dummyFarmer.livestock_types"
            label="Ovin"
            value="Ovin"
          ></v-checkbox>
          <v-checkbox
            @click.native="hasChanged = true"
            v-model="dummyFarmer.livestock_types"
            label="Caprin"
            value="Caprin"
          ></v-checkbox>
          <v-checkbox
            @click.native="hasChanged = true"
            v-model="dummyFarmer.livestock_types"
            label="Avicole"
            value="Avicole"
          ></v-checkbox>
          <v-checkbox
            @click.native="hasChanged = true"
            v-model="dummyFarmer.livestock_types"
            label="Porcin"
            value="Porcin"
          ></v-checkbox>
          <v-checkbox
            @click.native="hasChanged = true"
            v-model="dummyFarmer.livestock_types"
            label="Autre"
            value="Autre"
          ></v-checkbox>
        </div>

        <!-- LIVESTOCK NUMBER -->

        <div class="field">
          <div class="field-title title">Si vous avez de l'élevage, combien de bêtes avez-vous ?</div>
          <v-text-field
            hide-details="auto"
            @input="hasChanged = true"
            outlined
            dense
            v-model="dummyFarmer.livestock_number"
          ></v-text-field>
        </div>

        <!-- CULTURES -->

        <div class="field">
          <div class="field-title title">
            Quelles cultures avez-vous sur l'exploitation ?
            <span class="mandatory">- obligatoire</span>
          </div>
          <div class="field-helper">Lister les cultures et les espèces fourragères</div>
          <v-textarea
            hide-details="auto"
            rows="3"
            @input="hasChanged = true"
            auto-grow
            outlined
            dense
            v-model="dummyFarmer.cultures"
            :rules="[validators.notEmpty]"
          ></v-textarea>
        </div>

        <!-- SOIL TYPE -->

        <div class="field">
          <div class="field-title title">
            Quels types de sols sont présents sur l'exploitation ?
            <span class="mandatory">- obligatoire</span>
          </div>
          <v-textarea
            hide-details="auto"
            rows="3"
            @input="hasChanged = true"
            auto-grow
            outlined
            dense
            :rules="[validators.notEmpty]"
            v-model="dummyFarmer.soil_type"
          ></v-textarea>
        </div>

        <!-- OUTPUT -->

        <div class="field">
          <div
            class="field-title title"
          >Quel est rendement moyen en blé tendre de l'exploitation (en quintaux / ha)</div>
          <v-text-field
            hide-details="auto"
            @input="hasChanged = true"
            outlined
            dense
            v-model="dummyFarmer.output"
          ></v-text-field>
        </div>

        <!-- DESCRIPTION -->

        <div class="field">
          <div class="field-title title">
            Pouvez-vous décrire votre exploitation ?
            <span class="mandatory">- obligatoire</span>
          </div>
          <div
            class="field-helper"
          >Son histoire, son fonctionnement, ses particularités, la philosophie et le type d'agriculture pratiquée...</div>
          <v-textarea
            hide-details="auto"
            rows="5"
            @input="hasChanged = true"
            auto-grow
            outlined
            :rules="[validators.notEmpty]"
            dense
            v-model="dummyFarmer.description"
          ></v-textarea>
        </div>

        <!-- SPECIFICITIES -->

        <div class="field">
          <div
            class="field-title title"
          >Si il y en a, quelles sont les spécificités de l'exploitation ?</div>
          <div
            class="field-helper"
          >Irrigation, drainage, zone protégée, captage d'eau, parcellaire...</div>
          <v-textarea
            hide-details="auto"
            rows="5"
            @input="hasChanged = true"
            auto-grow
            outlined
            dense
            v-model="dummyFarmer.specificities"
          ></v-textarea>
        </div>

        <!-- AGRICULTURE TYPES -->

        <div class="field">
          <div
            class="field-title title"
          >Choisissez les termes qui correspondent à l'agriculture que vous pratiquez</div>
          <div class="field-helper">Vous pouvez en sélectionner plusieurs</div>
          <v-checkbox
            hide-details
            @click.native="hasChanged = true"
            v-model="dummyFarmer.agriculture_types"
            label="Agriculture Biologique"
            value="Agriculture Biologique"
          ></v-checkbox>
          <v-checkbox
            hide-details
            @click.native="hasChanged = true"
            v-model="dummyFarmer.agriculture_types"
            label="Agriculture de Conservation des Sols"
            value="Agriculture de Conservation des Sols"
          ></v-checkbox>
          <v-checkbox
            hide-details
            @click.native="hasChanged = true"
            v-model="dummyFarmer.agriculture_types"
            label="Techniques Culturales Simplifiées"
            value="Techniques Culturales Simplifiées"
          ></v-checkbox>
          <v-checkbox
            hide-details
            @click.native="hasChanged = true"
            v-model="dummyFarmer.agriculture_types"
            label="Labour occasionnel"
            value="Labour occasionnel"
          ></v-checkbox>
          <v-checkbox
            hide-details
            @click.native="hasChanged = true"
            v-model="dummyFarmer.agriculture_types"
            label="Agroforesterie"
            value="Agroforesterie"
          ></v-checkbox>
          <v-checkbox
            hide-details
            @click.native="hasChanged = true"
            v-model="dummyFarmer.agriculture_types"
            label="Conventionnel"
            value="Conventionnel"
          ></v-checkbox>
          <v-checkbox
            hide-details
            @click.native="hasChanged = true"
            v-model="dummyFarmer.agriculture_types"
            label="Cahier des charges industriel"
            value="Cahier des charges industriel"
          ></v-checkbox>
          <v-checkbox
            hide-details
            @click.native="hasChanged = true"
            v-model="dummyFarmer.agriculture_types"
            label="Label qualité"
            value="Label qualité"
          ></v-checkbox>
          <v-checkbox
            hide-details
            @click.native="hasChanged = true"
            v-model="dummyFarmer.agriculture_types"
            label="Label environnemental (HVE)"
            value="Label environnemental (HVE)"
          ></v-checkbox>
          <v-checkbox
            hide-details
            @click.native="hasChanged = true"
            v-model="dummyFarmer.agriculture_types"
            label="Autre"
            value="Autre"
          ></v-checkbox>
        </div>

        <!-- LINKS -->

        <div class="field">
          <div class="field-title title">Liens</div>
          <div
            class="field-helper"
            style="margin-bottom: 10px;"
          >Si vous le souhaitez, vous pouvez ajouter des liens vers votre site, vos profils de réseaux sociaux, ou autre</div>
          <v-text-field
            hide-details="auto"
            :rules="[validators.isUrl]"
            @input="hasChanged = true"
            @blur="appendHttp(index)"
            v-for="(link, index) in dummyFarmer.links"
            :key="index"
            outlined
            dense
            placeholder="https://..."
            style="max-width: 600px;"
            v-model="dummyFarmer.links[index]"
          >
            <template v-slot:prepend>
              <v-btn fab x-small style="margin-top: -3px;" @click="deleteLink(index)">
                <v-icon color="red">mdi-trash-can-outline</v-icon>
              </v-btn>
            </template>
          </v-text-field>
          <v-btn class="text-none" @click="addLink()">
            <v-icon small style="margin-right: 5px;">mdi-link-variant-plus</v-icon>Ajoutez un lien
          </v-btn>
        </div>

        <!-- PHOTOS -->

        <div class="field">
          <div class="field-title title">Photos de votre exploitation</div>
          <div class="field-helper">Vous pouvez en ajouter plusieurs</div>
          <ImagesField :imageArray.sync="dummyFarmer.images" @change="hasChanged = true" />
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
import ImagesField from "@/components/ImagesField.vue"

export default {
  name: "FarmEditor",
  components: { Title, Loader, ImagesField },
  metaInfo() {
    return {
      title: "Peps - Mettez à jour les données de votre exploitation",
      meta: [
        {
          description:
            "Modifiez le descriptif de votre exploitation, les données associées et la philosophie",
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
        production: [],
        surface_meadows: [],
        groups: [],
        agriculture_types: [],
        images: [],
        links: [],
      },
      toolbarOnTop: false,
      initialToolbarTop: 0,
      hasChanged: false,
      formIsValid: true,
      showDateModal: false,
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
    installationYear() {
      if (!this.dummyFarmer.installation_date) return ""

      const dateElements = this.dummyFarmer.installation_date.split("-")
      if (dateElements.length != 3) return ""

      return dateElements[0]
    },
    hasProductions() {
      const errorMessage = "Vous devez en selectionner au moins une production"
      if (!this.dummyFarmer || !this.dummyFarmer.production) return errorMessage
      return this.dummyFarmer.production.length > 0 || errorMessage
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
      }
    },
    closeOverlay() {
      const success = this.updateSucceeded
      this.$store.dispatch("resetFarmerEditLoadingStatus")
      if (success)
        this.$router.push({
          name: "Profile",
        })
    },
    cancelEdit() {
      this.$router.go(-1)
    },
    resetdummyFarmer() {
      if (this.farmer) {
        this.dummyFarmer = JSON.parse(JSON.stringify(this.farmer))
        this.dummyFarmer.images = this.dummyFarmer.images || []
      }
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
    deleteImage(index) {
      this.dummyFarmer.images.splice(index, 1)
      this.hasChanged = true
    },
    addLink() {
      this.dummyFarmer.links = this.dummyFarmer.links || []
      this.dummyFarmer.links.push("")
      this.hasChanged = true
    },
    appendHttp(index) {
      if (!this.dummyFarmer.links[index]) return
      if (this.dummyFarmer.links[index].indexOf("http") !== 0)
        this.dummyFarmer.links.splice(
          index,
          1,
          `http://${this.dummyFarmer.links[index]}`
        )
    },
    deleteLink(index) {
      this.dummyFarmer.links.splice(index, 1)
      this.hasChanged = true
    },
    onDatePickerChange(date) {
      this.dummyFarmer.installation_date = date
      this.hasChanged = true
    },
    onInstallationYearChange(year) {
      year = year.trim()
      this.dummyFarmer.installation_date = `${year}-01-01`
      this.hasChanged = true
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
  },
  beforeMount() {
    this.resetdummyFarmer()
  },
  mounted() {
    this.initialToolbarTop =
      this.$el.querySelector("#button-toolbar").offsetTop || 0
  },
  created() {
    window.addEventListener("beforeunload", this.handleUnload)
    window.addEventListener("scroll", this.onScroll)
  },
  beforeDestroy() {
    window.removeEventListener("beforeunload", this.handleUnload)
    window.removeEventListener("scroll", this.onScroll)
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
