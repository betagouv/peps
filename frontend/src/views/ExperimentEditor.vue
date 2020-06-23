<template>
  <div id="xp-edit">
    <Loader v-if="updateInProgress" title="Juste un instant..." :loading="updateInProgress" />
    <Title :breadcrumbs="breadcrumbs" />

    <v-container class="constrained">
      <v-toolbar elevation="0">
        <v-toolbar-title class="primary--text"></v-toolbar-title>
        <v-spacer></v-spacer>
        <v-btn style="margin-right: 10px;" @click="cancelEdit" class="text-none">
          <v-icon>mdi-arrow-left</v-icon>Annuler
        </v-btn>

        <v-btn class="text-none" :disabled="!hasChanged" color="primary" @click="updateExperiment">
          <v-icon>mdi-content-save</v-icon>Sauvegarder les changements
        </v-btn>
      </v-toolbar>

      <v-form ref="form" v-model="formIsValid">
        <!-- NAME -->
        <div class="field">
          <div class="field-title title">Titre de l'expérience <span class="mandatory">- obligatoire</span></div>
          <div class="field-helper">Court et explicite, il doit donner l'idée générale</div>
          <v-text-field
            hide-details="auto"
            :rules="[validators.notEmpty, validators.maxCharsXPName]"
            @input="hasChanged = true"
            outlined
            dense
            counter
            maxlength="70"
            v-model="dummyExperiment.name"
          ></v-text-field>
        </div>

        <!-- XP_TYPE -->
        <div class="field">
          <div class="field-title title">De quel type d'expérience s'agit-il ? <span class="mandatory">- obligatoire</span></div>
          <v-radio-group
            @change="hasChanged = true"
            v-model="dummyExperiment.xp_type"
            :mandatory="false"
            :rules="[validators.notEmpty]"
          >
            <v-radio
              label="Changement important de l'exploitation"
              value="Changement important de l'exploitation"
            ></v-radio>
            <v-radio label="Amélioration de l'existant" value="Amélioration de l'existant"></v-radio>
          </v-radio-group>
        </div>

        <!-- OBJECTIVES -->
        <div class="field">
          <div
            class="field-title title"
          >Dans quels objectifs plus global de l'exploitation cela s'inscrit ? <span class="mandatory">- obligatoire</span></div>
          <div
            class="field-helper"
          >Diversifier les sources de revenus, réduire l'utilisation d'herbicides, améliorer le structure du sol...</div>
          <v-textarea
            hide-details="auto"
            :rules="[validators.notEmpty]"
            rows="4"
            @input="hasChanged = true"
            auto-grow
            outlined
            dense
            v-model="dummyExperiment.objectives"
          ></v-textarea>
        </div>

        <!-- TAGS -->
        <div class="field">
          <div
            class="field-title title"
          >Ajoutez les labels qui vous semblent pertinents pour ce retour d'expérience</div>
          <div class="field-helper">Vous pouvez en sélectionner plusieurs</div>
          <v-checkbox
            @click.native="hasChanged = true"
            v-model="dummyExperiment.tags"
            label="Maladies"
            value="Maladies"
          ></v-checkbox>
          <v-checkbox
            @click.native="hasChanged = true"
            v-model="dummyExperiment.tags"
            label="Insectes et ravageurs"
            value="Insectes et ravageurs"
          ></v-checkbox>
          <v-checkbox
            @click.native="hasChanged = true"
            v-model="dummyExperiment.tags"
            label="Adventices"
            value="Adventices"
          ></v-checkbox>
          <v-checkbox
            @click.native="hasChanged = true"
            v-model="dummyExperiment.tags"
            label="Environnement & biodiversité"
            value="Environnement & biodiversité"
          ></v-checkbox>
          <v-checkbox
            @click.native="hasChanged = true"
            v-model="dummyExperiment.tags"
            label="Diversification"
            value="Diversification"
          ></v-checkbox>
          <v-checkbox
            @click.native="hasChanged = true"
            v-model="dummyExperiment.tags"
            label="Autonomie fourragère"
            value="Autonomie fourragère"
          ></v-checkbox>
          <v-checkbox
            @click.native="hasChanged = true"
            v-model="dummyExperiment.tags"
            label="Productivité"
            value="Productivité"
          ></v-checkbox>
          <v-checkbox
            @click.native="hasChanged = true"
            v-model="dummyExperiment.tags"
            label="Organisation du travail"
            value="Organisation du travail"
          ></v-checkbox>
          <v-checkbox
            @click.native="hasChanged = true"
            v-model="dummyExperiment.tags"
            label="Réduction des charges"
            value="Réduction des charges"
          ></v-checkbox>
          <v-checkbox
            @click.native="hasChanged = true"
            v-model="dummyExperiment.tags"
            label="Autre"
            value="Autre"
          ></v-checkbox>
        </div>

        <!-- ONGOING -->
        <div class="field">
          <div class="field-title title">L'expérience est-elle en cours aujourd'hui ? <span class="mandatory">- obligatoire</span></div>
          <div
            class="field-helper"
          >Si l'expérience a été intégrée à l'exploitation et est améliorée à la marge, dites Non</div>
          <v-radio-group
            @change="hasChanged = true"
            v-model="dummyExperiment.ongoing"
            :mandatory="false"
            :rules="[validators.notEmpty]"
          >
            <v-radio label="Oui" :value="true"></v-radio>
            <v-radio label="Non" :value="false"></v-radio>
          </v-radio-group>
        </div>

        <!-- INVESTMENT -->
        <div class="field">
          <div
            class="field-title title"
          >Quels investissements ont été nécessaires pour cette expérience ? <span class="mandatory">- obligatoire</span></div>
          <div class="field-helper">En temps, en argent, en machines...</div>
          <v-textarea
            hide-details="auto"
            :rules="[validators.notEmpty]"
            rows="1"
            @input="hasChanged = true"
            auto-grow
            outlined
            dense
            v-model="dummyExperiment.investment"
          ></v-textarea>
        </div>

        <!-- EQUIPMENT -->
        <div class="field">
          <div
            class="field-title title"
          >Quel matériel avez-vous utilisé pour mener cette expérience ?</div>
          <div class="field-helper">Vous pouvez ici être assez spécifique</div>
          <v-textarea
            hide-details="auto"
            rows="1"
            @input="hasChanged = true"
            auto-grow
            outlined
            dense
            v-model="dummyExperiment.equipment"
          ></v-textarea>
        </div>

        <!-- DESCRIPTION -->
        <div class="field">
          <div class="field-title title">Pouvez-vous décrire l'expérience ? <span class="mandatory">- obligatoire</span></div>
          <div
            class="field-helper"
          >Dites comment cela s'est déroulé, ce que vous avez observé, les choses que vous avez apprises...</div>
          <v-textarea
            hide-details="auto"
            :rules="[validators.notEmpty]"
            rows="4"
            @input="hasChanged = true"
            auto-grow
            outlined
            dense
            v-model="dummyExperiment.description"
          ></v-textarea>
        </div>

        <!-- SURFACE TYPE -->
        <div class="field">
          <div class="field-title title">Sur quelle surface portait l'expérience ?</div>
          <div
            class="field-helper"
          >"Toutes les surfaces" correspond à toutes les surfaces de l'exploitation</div>
          <v-checkbox
            @click.native="hasChanged = true"
            v-model="dummyExperiment.surface_type"
            label="Toutes les surfaces"
            value="Toutes les surfaces"
          ></v-checkbox>
          <v-checkbox
            @click.native="hasChanged = true"
            v-model="dummyExperiment.surface_type"
            label="Plusieurs parcelles"
            value="Plusieurs parcelles"
          ></v-checkbox>
          <v-checkbox
            @click.native="hasChanged = true"
            v-model="dummyExperiment.surface_type"
            label="Une parcelle"
            value="Une parcelle"
          ></v-checkbox>
          <v-checkbox
            @click.native="hasChanged = true"
            v-model="dummyExperiment.surface_type"
            label="Des bandes"
            value="Des bandes"
          ></v-checkbox>
          <v-checkbox
            @click.native="hasChanged = true"
            v-model="dummyExperiment.surface_type"
            label="Des carrés"
            value="Des carrés"
          ></v-checkbox>
        </div>

        <!-- SURFACE -->
        <div class="field">
          <div class="field-title title">Combien d'ha cela représente ?</div>
          <v-textarea
            hide-details="auto"
            @change="hasChanged = true"
            rows="1"
            auto-grow
            outlined
            dense
            v-model="dummyExperiment.surface"
          ></v-textarea>
        </div>

        <!-- CONTROL PRESENCE -->
        <div class="field">
          <div class="field-title title">Avez-vous mis en place un témoin ? <span class="mandatory">- obligatoire</span></div>
          <div class="field-helper">
            C'est à dire une surface similaire qui permet de valider les résultats obtenus.
            Si ce n'est pas pertinent, dites Non
          </div>
          <v-radio-group
            :rules="[validators.notEmpty]"
            @change="hasChanged = true"
            v-model="dummyExperiment.control_presence"
            :mandatory="false"
          >
            <v-radio label="Oui" :value="true"></v-radio>
            <v-radio label="Non" :value="false"></v-radio>
          </v-radio-group>
        </div>

        <!-- RESULTS -->
        <div class="field">
          <div class="field-title title">Quel est le statut de cette expérience ? <span class="mandatory">- obligatoire</span></div>
          <v-radio-group
            :rules="[validators.notEmpty]"
            @change="hasChanged = true"
            v-model="dummyExperiment.results"
            :mandatory="false"
          >
            <v-radio
              label="Fonctionne, elle est intégrée à l'exploitation"
              value="XP qui fonctionne, elle est intégrée à l'exploitation"
            ></v-radio>
            <v-radio
              label="Prometteuse, en cours d'amélioration"
              value="XP prometteuse, en cours d'amélioration"
            ></v-radio>
            <v-radio
              label="Abandonnée, les résultats ne sont pas satisfaisants"
              value="XP abandonnée, les résultats ne sont pas satisfaisants"
            ></v-radio>
            <v-radio
              label="En suspens, les conditions ne sont plus réunies"
              value="XP en suspens, les conditions ne sont plus réunies"
            ></v-radio>
            <v-radio
              label="Commence, les premiers résultats sont à venir"
              value="XP qui commence, les premiers résultats sont à venir"
            ></v-radio>
          </v-radio-group>
        </div>

        <!-- RESULTS DETAILS -->
        <div class="field">
          <div class="field-title title">Pouvez-vous détailler les résultats ?</div>
          <div
            class="field-helper"
          >Vous pouvez ici donner des chiffres, détailler l'impact ressenti de cette expérience...</div>
          <v-textarea
            hide-details="auto"
            rows="4"
            @input="hasChanged = true"
            auto-grow
            outlined
            dense
            v-model="dummyExperiment.results_details"
          ></v-textarea>
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
            v-for="(link, index) in dummyExperiment.links"
            :key="index"
            outlined
            dense
            placeholder="https://..."
            style="max-width: 600px;"
            v-model="dummyExperiment.links[index]"
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

        <!-- IMAGES  -->
        <div class="field">
          <div class="field-title title">Images</div>
          <div class="field-helper grey--text">Vous pouvez en ajouter plusieurs</div>
          <ImagesField :imageArray="dummyExperiment.images" @change="hasChanged = true" />
        </div>

        <!-- VIDEOS -->
        <div class="field">
          <div class="field-title title">Vidéos</div>
          <div class="field-helper grey--text">Vous pouvez en ajouter plusieurs</div>
          <VideosField :videoArray="dummyExperiment.videos" @change="hasChanged = true" />
        </div>
      </v-form>

      <v-toolbar elevation="0">
        <v-toolbar-title class="primary--text"></v-toolbar-title>
        <v-spacer></v-spacer>
        <v-btn style="margin-right: 10px;" @click="cancelEdit" class="text-none">
          <v-icon>mdi-arrow-left</v-icon>Annuler
        </v-btn>

        <v-btn class="text-none" :disabled="!hasChanged" color="primary" @click="updateExperiment">
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
              <span v-if="experimentUrlComponent">Votre retour d'expérience a bien été mise à jour !</span>
              <span
                v-else
              >Votre retour d'expérience a bien été créée ! Notre équipe la mettra en ligne bientôt.</span>
            </span>
            <span v-else>
              <v-icon style="margin-top: -3px; margin-right: 5px;">mdi-emoticon-sad-outline</v-icon>Oops ! On n'a pas pu mettre à jour le retour d'expérience. Veuillez essayer plus tard.
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
import ImagesField from '@/components/ImagesField.vue'
import VideosField from '@/components/VideosField.vue'

export default {
  name: "ExperimentEditor",
  components: { Title, Loader, ImagesField, VideosField },
  props: {
    experimentUrlComponent: {
      type: String,
      default: null
    }
  },
  data() {
    return {
      dummyExperiment: {
        tags: [],
        surface_type: [],
        links: []
      },
      hasChanged: false,
      formIsValid: true
    }
  },
  computed: {
    updateInProgress() {
      return (
        this.$store.state.experimentEditLoadingStatus ==
        Constants.LoadingStatus.LOADING
      )
    },
    updateSucceeded() {
      return (
        this.$store.state.experimentEditLoadingStatus ===
        Constants.LoadingStatus.SUCCESS
      )
    },
    updateFailed() {
      return (
        this.$store.state.experimentEditLoadingStatus ===
        Constants.LoadingStatus.ERROR
      )
    },
    validators() {
      return validators
    },
    loggedFarmer() {
      const farmer = this.$store.getters.farmerWithId(
        this.$store.state.loggedUser.farmer_id
      )
      return farmer
    },
    experiment() {
      if (!this.loggedFarmer || !this.experimentUrlComponent) return undefined
      return this.$store.getters.experimentWithUrlComponent(
        this.loggedFarmer,
        this.experimentUrlComponent
      )
    },
    breadcrumbs() {
      return [
        {
          text: "Carte de retours d'expérience",
          disabled: false,
          href: "/map"
        },
        {
          text: "Mon compte",
          disabled: false,
          href: "/compte"
        },
        {
          text: this.experiment ? this.experiment.name : "Nouvelle expérience",
          disabled: true
        }
      ]
    }
  },
  methods: {
    updateExperiment() {
      this.$refs.form.validate()

      if (!this.formIsValid) {
        window.scrollTo(0, 0)
        window.alert("Merci de vérifier les champs en rouge et réessayer")
        return
      }

      if (this.experiment) {
        const payload = utils.getObjectDiff(
          this.experiment,
          this.dummyExperiment
        )

        this.$store.dispatch("patchExperiment", {
          experiment: this.experiment,
          changes: payload
        })
      } else {
        this.$store.dispatch("createExperiment", {
          payload: this.dummyExperiment,
          farmer: this.loggedFarmer
        })
      }
    },
    closeOverlay() {
      const success = this.updateSucceeded
      this.$store.dispatch("resetExperimentEditLoadingStatus")
      if (success)
        this.$router.push({
          name: "Profile"
        })
      else this.resetMediaFields()
    },
    cancelEdit() {
      this.$router.go(-1)
    },
    resetDummyExperiment() {
      if (this.experiment) {
        this.dummyExperiment = JSON.parse(JSON.stringify(this.experiment))
        this.dummyExperiment.images = this.dummyExperiment.images || []
        this.dummyExperiment.links = this.dummyExperiment.links || []
      }
    },
    resetMediaFields() {
      this.dummyExperiment.images = this.experiment
        ? JSON.parse(JSON.stringify(this.experiment.images))
        : []
      this.dummyExperiment.videos = this.experiment
        ? JSON.parse(JSON.stringify(this.experiment.videos))
        : []
    },
    addImages(e) {
      if (!e) return
      const files = e.target.files
      this.hasChanged = true

      for (let i = 0; i < files.length; i++) {
        const file = files[i]
        utils.toBase64(file, base64 => {
          this.dummyExperiment.images.push({
            image: base64,
            label: ""
          })
        })
      }
    },
    deleteImage(index) {
      this.dummyExperiment.images.splice(index, 1)
      this.hasChanged = true
    },
    deleteVideo(index) {
      this.dummyExperiment.videos.splice(index, 1)
      this.hasChanged = true
    },
    addLink() {
      this.dummyExperiment.links = this.dummyExperiment.links || []
      this.dummyExperiment.links.push("")
      this.hasChanged = true
    },
    appendHttp(index) {
      if (!this.dummyExperiment.links[index]) return
      if (this.dummyExperiment.links[index].indexOf("http") !== 0)
        this.dummyExperiment.links.splice(
          index,
          1,
          `http://${this.dummyExperiment.links[index]}`
        )
    },
    deleteLink(index) {
      this.dummyExperiment.links.splice(index, 1)
      this.hasChanged = true
    }
  },
  beforeMount() {
    this.resetDummyExperiment()
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
