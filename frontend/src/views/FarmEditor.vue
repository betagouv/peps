<template>
  <div id="farmer-edit">
    <Loader v-if="updateInProgress" title="Juste un instant..." :loading="updateInProgress" />
    <Title :breadcrumbs="breadcrumbs" />

    <v-container class="constrained">
      <v-toolbar elevation="0">
        <v-toolbar-title class="primary--text"></v-toolbar-title>
        <v-spacer></v-spacer>
        <v-btn style="margin-right: 10px;" @click="cancelEdit" class="text-none">
          <v-icon>mdi-arrow-left</v-icon>Annuler
        </v-btn>

        <v-btn class="text-none" :disabled="!hasChanged" color="primary" @click="updateFarmer">
          <v-icon>mdi-content-save</v-icon>Sauvegarder les changements
        </v-btn>
      </v-toolbar>

      <v-form ref="form" v-model="formIsValid">
        <!-- PRODUCTIONS -->
        <div class="field">
          <div class="field-title title">Quelles productions sont présentes sur l'exploitation ?</div>
          <div class="field-helper grey--text">Vous pouvez en sélectionner plusieurs</div>
          <v-checkbox
            @click.native="hasChanged = true"
            v-model="dummyFarmer.production"
            label="Grandes cultures"
            value="Grandes cultures"
          ></v-checkbox>
          <v-checkbox
            @click.native="hasChanged = true"
            v-model="dummyFarmer.production"
            label="Cultures industrielles"
            value="Cultures industrielles"
          ></v-checkbox>
          <v-checkbox
            @click.native="hasChanged = true"
            v-model="dummyFarmer.production"
            label="Élevage allaitant"
            value="Élevage allaitant"
          ></v-checkbox>
          <v-checkbox
            @click.native="hasChanged = true"
            v-model="dummyFarmer.production"
            label="Élevage laitier"
            value="Élevage laitier"
          ></v-checkbox>
          <v-checkbox
            @click.native="hasChanged = true"
            v-model="dummyFarmer.production"
            label="Élevage engraissement"
            value="Élevage engraissement"
          ></v-checkbox>
          <v-checkbox
            @click.native="hasChanged = true"
            v-model="dummyFarmer.production"
            label="Élevage poule"
            value="Élevage poule"
          ></v-checkbox>
          <v-checkbox
            @click.native="hasChanged = true"
            v-model="dummyFarmer.production"
            label="Cultures légumières"
            value="Cultures légumières"
          ></v-checkbox>
          <v-checkbox
            @click.native="hasChanged = true"
            v-model="dummyFarmer.production"
            label="Vigne"
            value="Vigne"
          ></v-checkbox>
          <v-checkbox
            @click.native="hasChanged = true"
            v-model="dummyFarmer.production"
            label="Autre"
            value="Autre"
          ></v-checkbox>
        </div>

        <!-- INSTALLATION DATE -->

        <div class="field">
          <div class="field-title title">Quand vous êtes-vous installé sur l'exploitation ?</div>

          <v-menu
            ref="menu"
            v-model="showDateModal"
            :close-on-content-click="false"
            transition="scale-transition"
            offset-y
            min-width="290px"
          >
            <template v-slot:activator="{ on }">
              <v-text-field
                hide-details="auto"
                :value="formattedInstallationDate"
                label="Date d'installation"
                prepend-icon="mdi-calendar-blank-outline"
                readonly
                v-on="on"
              ></v-text-field>
            </template>
            <v-date-picker @change="onDatePickerChange" no-title scrollable>
              <v-spacer></v-spacer>
              <v-btn text color="primary" @click="showDateModal = false">OK</v-btn>
            </v-date-picker>
          </v-menu>
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
            <span class="mandatory">- obligatoire</span>
          </div>
          <div class="field-helper grey--text">Comptez-vous et vos associés, salariés et alternants</div>
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
            <div class="field-title subtitle-2">
              La surface en cultures (en ha.)
              <span class="mandatory">- obligatoire</span>
            </div>
            <v-text-field
              hide-details="auto"
              :rules="[validators.notEmpty]"
              @input="hasChanged = true"
              outlined
              dense
              v-model="dummyFarmer.surface_cultures"
            ></v-text-field>
          </div>

          <!-- SURFACE MEADOWS -->

          <div class="field child-field">
            <div class="field-title subtitle-2">
              La surface en prairie et cultures fourragères (en ha.)
              <span class="mandatory">- obligatoire</span>
            </div>
            <v-text-field
              hide-details="auto"
              :rules="[validators.notEmpty]"
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
          <div class="field-title title">Quelles cultures avez-vous sur l'exploitation ?</div>
          <div class="field-helper grey--text">Lister les cultures et les espèces fourragères</div>
          <v-textarea
            hide-details="auto"
            rows="3"
            @input="hasChanged = true"
            auto-grow
            outlined
            dense
            v-model="dummyFarmer.cultures"
          ></v-textarea>
        </div>

        <!-- SOIL TYPE -->

        <div class="field">
          <div class="field-title title">Quels types de sols sont présents sur l'exploitation ?</div>
          <v-textarea
            hide-details="auto"
            rows="3"
            @input="hasChanged = true"
            auto-grow
            outlined
            dense
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
          <div class="field-title title">Pouvez-vous décrire votre exploitation ?</div>
          <div
            class="field-helper grey--text"
          >Son histoire, son fonctionnement, ses particularités, la philosophie et le type d'agriculture pratiquée...</div>
          <v-textarea
            hide-details="auto"
            rows="5"
            @input="hasChanged = true"
            auto-grow
            outlined
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
            class="field-helper grey--text"
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
          <div class="field-helper grey--text">Vous pouvez en sélectionner plusieurs</div>
          <v-checkbox
            @click.native="hasChanged = true"
            v-model="dummyFarmer.agriculture_types"
            label="Agriculture Biologique"
            value="Agriculture Biologique"
          ></v-checkbox>
          <v-checkbox
            @click.native="hasChanged = true"
            v-model="dummyFarmer.agriculture_types"
            label="Agriculture de Conservation des Sols"
            value="Agriculture de Conservation des Sols"
          ></v-checkbox>
          <v-checkbox
            @click.native="hasChanged = true"
            v-model="dummyFarmer.agriculture_types"
            label="Techniques Culturales Simplifiées"
            value="Techniques Culturales Simplifiées"
          ></v-checkbox>
          <v-checkbox
            @click.native="hasChanged = true"
            v-model="dummyFarmer.agriculture_types"
            label="Labour occasionnel"
            value="Labour occasionnel"
          ></v-checkbox>
          <v-checkbox
            @click.native="hasChanged = true"
            v-model="dummyFarmer.agriculture_types"
            label="Agroforesterie"
            value="Agroforesterie"
          ></v-checkbox>
          <v-checkbox
            @click.native="hasChanged = true"
            v-model="dummyFarmer.agriculture_types"
            label="Conventionnel"
            value="Conventionnel"
          ></v-checkbox>
          <v-checkbox
            @click.native="hasChanged = true"
            v-model="dummyFarmer.agriculture_types"
            label="Cahier des charges industriel"
            value="Cahier des charges industriel"
          ></v-checkbox>
          <v-checkbox
            @click.native="hasChanged = true"
            v-model="dummyFarmer.agriculture_types"
            label="Label qualité"
            value="Label qualité"
          ></v-checkbox>
          <v-checkbox
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
            class="field-helper grey--text"
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
          <div class="field-helper grey--text">Vous pouvez en ajouter plusieurs</div>
          <ImagesField :imageArray="dummyFarmer.images" @change="hasChanged = true" />
        </div>
      </v-form>

      <v-toolbar elevation="0">
        <v-toolbar-title class="primary--text"></v-toolbar-title>
        <v-spacer></v-spacer>
        <v-btn style="margin-right: 10px;" @click="cancelEdit" class="text-none">
          <v-icon>mdi-arrow-left</v-icon>Annuler
        </v-btn>

        <v-btn class="text-none" :disabled="!hasChanged" color="primary" @click="updateFarmer">
          <v-icon>mdi-content-save</v-icon>Sauvegarder les changements
        </v-btn>
      </v-toolbar>
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
  props: {
    farmerUrlComponent: {
      type: String,
      default: null
    }
  },
  data() {
    return {
      dummyFarmer: {
        production: [],
        surface_meadows: [],
        groups: [],
        agriculture_types: [],
        links: []
      },
      hasChanged: false,
      formIsValid: true,
      showDateModal: false
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
          text: "Carte de retours d'expérience",
          disabled: false,
          href: "/#/map"
        },
        {
          text: "Mon compte",
          disabled: false,
          href: "/#/compte"
        },
        {
          text: this.farmer ? this.farmer.name : "Nouveau profil",
          disabled: true
        }
      ]
    },
    formattedInstallationDate() {
      if (!this.dummyFarmer.installation_date) return ""

      const dateElements = this.dummyFarmer.installation_date.split("-")
      if (dateElements.length != 3) return ""

      const year = dateElements[0]
      const month = dateElements[1]
      const day = dateElements[2]

      const months = {
        "01": "janvier",
        "02": "février",
        "03": "mars",
        "04": "avril",
        "05": "mai",
        "06": "juin",
        "07": "juillet",
        "08": "août",
        "09": "septembre",
        "10": "octobre",
        "11": "novembre",
        "12": "décembre"
      }

      return `${day} ${months[month]}, ${year}`
    }
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
          changes: payload
        })
      }
    },
    closeOverlay() {
      const success = this.updateSucceeded
      this.$store.dispatch("resetFarmerEditLoadingStatus")
      if (success)
        this.$router.push({
          name: "Profile"
        })
      else this.resetMediaFields()
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
    resetMediaFields() {
      this.dummyFarmer.images = this.farmer
        ? JSON.parse(JSON.stringify(this.farmer.images))
        : []
    },
    changeProfileImage(file) {
      this.hasChanged = true
      if (!file) {
        this.dummyFarmer.profile_image = undefined
        return
      }
      utils.toBase64(file, base64 => {
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
    handleUnload(e) {
      if (this.hasChanged) {
        e.preventDefault()
        e.returnValue = ""
      } else {
        delete e["returnValue"]
      }
    }
  },
  watch: {
    updateSucceeded(newValue) {
      if (newValue) this.hasChanged = false
    },
    updateFailed(newValue) {
      if (newValue) this.hasChanged = false
    }
  },
  beforeMount() {
    this.resetdummyFarmer()
  },
  mounted() {
    window.addEventListener("beforeunload", this.handleUnload)
  },
  beforeDestroy() {
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
  }
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
