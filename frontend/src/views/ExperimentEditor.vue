<template>
  <div id="xp-edit">
    <Loader v-if="updateInProgress" title="Juste un instant..." :loading="updateInProgress" />
    <Title :breadcrumbs="breadcrumbs" />

    <v-container class="constrained">
      <v-sheet
        rounded
        class="pa-2 caption"
        v-if="dummyExperiment.state === 'En attente de validation'"
        color="blue-grey lighten-5"
      >Ce retour d'expérience est en attente de validation. Vous pouvez toujours apporter des modifications.</v-sheet>
      <v-app-bar
        style="margin-left: auto; margin-right: auto;"
        max-width="1000"
        color="white"
        :elevation="toolbarOnTop ? 2 : 0"
        :fixed="toolbarOnTop"
        id="button-toolbar"
      >
        <v-toolbar-title style="flex-flow: wrap;" class="primary--text"></v-toolbar-title>
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
          class="text-none"
          :small="$vuetify.breakpoint.name === 'xs'"
          v-if="dummyExperiment.state === 'Brouillon'"
          @click="updateDraftExperiment(false)"
          style="margin-right: 10px;"
        >
          <v-icon :small="$vuetify.breakpoint.name === 'xs'">mdi-content-save</v-icon>
          <span v-if="$vuetify.breakpoint.name === 'xs'">Sauvegarder</span>
          <span v-else>Sauvegarder le brouillon</span>
        </v-btn>

        <v-btn
          class="text-none"
          :small="$vuetify.breakpoint.name === 'xs'"
          v-if="dummyExperiment.state === 'Brouillon'"
          color="primary"
          @click="submitExperiment(true)"
        >
          <v-icon :small="$vuetify.breakpoint.name === 'xs'">mdi-check-decagram</v-icon>Valider
        </v-btn>

        <v-btn
          class="text-none"
          :small="$vuetify.breakpoint.name === 'xs'"
          color="primary"
          v-if="dummyExperiment.state !== 'Brouillon'"
          @click="updateExperiment(false)"
        >
          <v-icon :small="$vuetify.breakpoint.name === 'xs'">mdi-content-save</v-icon>Sauvegarder
        </v-btn>
      </v-app-bar>

      <v-form ref="form" v-model="formIsValid">
        <!-- NAME -->
        <div class="field">
          <div class="field-title title">
            Titre de l'expérience
            <span class="mandatory">- obligatoire</span>
          </div>
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
          <div class="field-title title">
            De quel type d'expérience s'agit-il ?
            <span class="mandatory">- obligatoire</span>
          </div>
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
          <div class="field-title title">
            Dans quels objectifs plus global de l'exploitation cela s'inscrit ?
            <span
              class="mandatory"
            >- obligatoire</span>
          </div>
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
          >Sélectionnez jusqu'a 3 étiquettes qui vous semblent les plus pertinents</div>
          <div
            class="field-helper"
          >Elles permettent de catégoriser par thèmes les retours d'expérience</div>
          <v-radio-group
            v-model="dummyExperiment.tags"
            :rules="[validators.maxSelected(3)]"
            hide-details="auto"
            style="margin-top: 5px; margin-bottom: 5px;"
          ></v-radio-group>
          <v-checkbox
            @click.native="hasChanged = true"
            v-model="dummyExperiment.tags"
            label="Maladies"
            value="Maladies"
            hide-details
            :rules="[validators.maxSelected(3)]"
          ></v-checkbox>
          <v-checkbox
            @click.native="hasChanged = true"
            v-model="dummyExperiment.tags"
            label="Insectes et ravageurs"
            value="Insectes et ravageurs"
            hide-details
            :rules="[validators.maxSelected(3)]"
          ></v-checkbox>
          <v-checkbox
            @click.native="hasChanged = true"
            v-model="dummyExperiment.tags"
            label="Adventices"
            value="Adventices"
            hide-details
            :rules="[validators.maxSelected(3)]"
          ></v-checkbox>
          <v-checkbox
            @click.native="hasChanged = true"
            v-model="dummyExperiment.tags"
            label="Environnement & biodiversité"
            value="Environnement & biodiversité"
            hide-details
            :rules="[validators.maxSelected(3)]"
          ></v-checkbox>
          <v-checkbox
            @click.native="hasChanged = true"
            v-model="dummyExperiment.tags"
            label="Diversification"
            value="Diversification"
            hide-details
            :rules="[validators.maxSelected(3)]"
          ></v-checkbox>
          <v-checkbox
            @click.native="hasChanged = true"
            v-model="dummyExperiment.tags"
            label="Autonomie"
            value="Autonomie"
            hide-details
            :rules="[validators.maxSelected(3)]"
          ></v-checkbox>
          <v-checkbox
            @click.native="hasChanged = true"
            v-model="dummyExperiment.tags"
            label="Productivité"
            value="Productivité"
            hide-details
            :rules="[validators.maxSelected(3)]"
          ></v-checkbox>
          <v-checkbox
            @click.native="hasChanged = true"
            v-model="dummyExperiment.tags"
            label="Organisation du travail"
            value="Organisation du travail"
            hide-details
            :rules="[validators.maxSelected(3)]"
          ></v-checkbox>
          <v-checkbox
            @click.native="hasChanged = true"
            v-model="dummyExperiment.tags"
            label="Réduction des charges"
            value="Réduction des charges"
            hide-details
            :rules="[validators.maxSelected(3)]"
          ></v-checkbox>
          <v-checkbox
            @click.native="hasChanged = true"
            v-model="dummyExperiment.tags"
            label="Autre"
            value="Autre"
            hide-details
            :rules="[validators.maxSelected(3)]"
          ></v-checkbox>
        </div>

        <!-- ONGOING -->
        <div class="field">
          <div class="field-title title">L'expérience est-elle en cours aujourd'hui ?</div>
          <div
            class="field-helper"
          >Si l'expérience a été intégrée à l'exploitation et est améliorée à la marge, dites Non</div>
          <v-radio-group
            @change="hasChanged = true"
            v-model="dummyExperiment.ongoing"
            :mandatory="false"
          >
            <v-radio label="Oui" :value="true"></v-radio>
            <v-radio label="Non" :value="false"></v-radio>
          </v-radio-group>
        </div>

        <!-- INVESTMENT -->
        <div class="field">
          <div
            class="field-title title"
          >Quels investissements ont été nécessaires pour cette expérience ?</div>
          <div class="field-helper">En temps, en argent, en machines...</div>
          <v-textarea
            hide-details="auto"
            rows="1"
            @input="hasChanged = true"
            auto-grow
            outlined
            dense
            v-model="dummyExperiment.investment"
          ></v-textarea>
        </div>

        <!-- CULTURES -->
        <div class="field">
          <div class="field-title title">Quelles cultures sont impliquées dans cette exprérience ?</div>
          <div
            class="field-helper"
          >Elles permettent de catégoriser par cultures les retours d'expérience</div>
          <v-autocomplete
            @input="hasChanged = true"
            v-model="dummyExperiment.cultures"
            :items="cultures"
            outlined
            chips
            multiple
            deletable-chips
            small-chips
            hide-details="auto"
            dense
          ></v-autocomplete>
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
          <div class="field-title title">
            Pouvez-vous décrire l'expérience ?
            <span class="mandatory">- obligatoire</span>
          </div>
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
          <div class="field-title title">
            Sur quelle surface portait l'expérience ?
            <span class="mandatory">- obligatoire</span>
          </div>
          <div
            class="field-helper"
          >"Toutes les surfaces" correspond à toutes les surfaces de l'exploitation</div>
          <v-checkbox
            @click.native="hasChanged = true"
            v-model="dummyExperiment.surface_type"
            label="Toutes les surfaces"
            value="Toutes les surfaces"
            hide-details
            :rules="[hasSurfaceType]"
          ></v-checkbox>
          <v-checkbox
            @click.native="hasChanged = true"
            v-model="dummyExperiment.surface_type"
            label="Plusieurs parcelles"
            value="Plusieurs parcelles"
            hide-details
            :rules="[hasSurfaceType]"
          ></v-checkbox>
          <v-checkbox
            @click.native="hasChanged = true"
            v-model="dummyExperiment.surface_type"
            label="Une parcelle"
            value="Une parcelle"
            hide-details
            :rules="[hasSurfaceType]"
          ></v-checkbox>
          <v-checkbox
            @click.native="hasChanged = true"
            v-model="dummyExperiment.surface_type"
            label="Des bandes"
            value="Des bandes"
            hide-details
            :rules="[hasSurfaceType]"
          ></v-checkbox>
          <v-checkbox
            @click.native="hasChanged = true"
            v-model="dummyExperiment.surface_type"
            label="Des carrés"
            value="Des carrés"
            :rules="[hasSurfaceType]"
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
          <div class="field-title title">
            Avez-vous mis en place un témoin ?
            <span class="mandatory">- obligatoire</span>
          </div>
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
          <div class="field-title title">
            Quel est le statut de cette expérience ?
            <span class="mandatory">- obligatoire</span>
          </div>
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
              <span v-else>Votre retour d'expérience a bien été créée !</span>
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
import ImagesField from "@/components/ImagesField.vue"
import VideosField from "@/components/VideosField.vue"

export default {
  name: "ExperimentEditor",
  components: { Title, Loader, ImagesField, VideosField },
  metaInfo() {
    const title = this.experiment
      ? "Peps - Modifier mon retour d'expérience"
      : "Peps - Partager un retour d'expérience"
    const description = this.experiment
      ? `Mettez à jour les données du retour d'expérience ${this.experiment.name}`
      : "Remplissez ces informations et partagez un retour d'expérience sur Peps"
    return {
      title: title,
      meta: [
        {
          description: description,
        },
      ],
    }
  },
  props: {
    experimentUrlComponent: {
      type: String,
      default: null,
    },
  },
  data() {
    return {
      dummyExperiment: {
        tags: [],
        surface_type: [],
        links: [],
        images: [],
        videos: [],
        state: "Brouillon",
      },
      toolbarOnTop: false,
      initialToolbarTop: 0,
      hasChanged: false,
      formIsValid: true,
      cultures: [
        {
          header: "Cultures",
        },
        {
          text: "Avoine",
          value: "Avoine",
        },
        {
          text: "Betterave fourragère",
          value: "Betterave fourragère",
        },
        {
          text: "Betterave sucrière",
          value: "Betterave sucrière",
        },
        {
          text: "Blé dur",
          value: "Blé dur",
        },
        {
          text: "Blé tendre d'hiver",
          value: "Blé tendre d'hiver",
        },
        {
          text: "Blé tendre de printemps",
          value: "Blé tendre de printemps",
        },
        {
          text: "Chanvre",
          value: "Chanvre",
        },
        {
          text: "Chia",
          value: "Chia",
        },
        {
          text: "Colza",
          value: "Colza",
        },
        {
          text: "Lentilles",
          value: "Lentilles",
        },
        {
          text: "Lin",
          value: "Lin",
        },
        {
          text: "Lupin blanc",
          value: "Lupin blanc",
        },
        {
          text: "Luzerne",
          value: "Luzerne",
        },
        {
          text: "Epeautre",
          value: "Epeautre",
        },
        {
          text: "Fétuque",
          value: "Fétuque",
        },
        {
          text: "Féverole",
          value: "Féverole",
        },
        {
          text: "Maïs grain",
          value: "Maïs grain",
        },
        {
          text: "Maïs ensilage",
          value: "Maïs ensilage",
        },
        {
          text: "Millet",
          value: "Millet",
        },
        {
          text: "Moutarde",
          value: "Moutarde",
        },
        {
          text: "Oeillette ou pavot",
          value: "Oeillette ou pavot",
        },
        {
          text: "Orge d’hiver",
          value: "Orge d’hiver",
        },
        {
          text: "Orge de printemps",
          value: "Orge de printemps",
        },
        {
          text: "Pois chiche",
          value: "Pois chiche",
        },
        {
          text: "Pois d'hiver",
          value: "Pois d'hiver",
        },
        {
          text: "Pois de printemps",
          value: "Pois de printemps",
        },
        {
          text: "Pomme de terre",
          value: "Pomme de terre",
        },
        {
          text: "Quinoa",
          value: "Quinoa",
        },
        {
          text: "Riz",
          value: "Riz",
        },
        {
          text: "Sarrasin",
          value: "Sarrasin",
        },
        {
          text: "Seigle",
          value: "Seigle",
        },
        {
          text: "Soja",
          value: "Soja",
        },
        {
          text: "Sorgho",
          value: "Sorgho",
        },
        {
          text: "Tournesol",
          value: "Tournesol",
        },
        {
          text: "Triticale",
          value: "Triticale",
        },
        {
          header: "Fourrages",
        },
        {
          text: "Graminées fourragères",
          value: "Graminées fourragères",
        },
        {
          text: "Légumineuses fourragères",
          value: "Légumineuses fourragères",
        },
        {
          text: "Protéagineux fourragers",
          value: "Protéagineux fourragers",
        },
        {
          text: "Prairies",
          value: "Prairies",
        },
        {
          header: "Autre",
        },
        {
          text: "Pas de culture",
          value: "Pas de culture",
        },
        {
          text: "Toutes les cultures",
          value: "Toutes les cultures",
        },
      ],
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
          text: this.experiment ? this.experiment.name : "Nouvelle expérience",
          disabled: true,
        },
      ]
    },
    hasSurfaceType() {
      const errorMessage = "Vous devez en selectionner au moins une surface"
      if (!this.dummyExperiment || !this.dummyExperiment.surface_type)
        return errorMessage
      return this.dummyExperiment.surface_type.length > 0 || errorMessage
    },
  },
  methods: {
    validateSubmission() {
      this.$refs.form.validate()

      if (!this.formIsValid) {
        window.scrollTo(0, 0)
        window.alert("Merci de vérifier les champs en rouge et réessayer")
      }

      return this.formIsValid
    },
    updateDraftExperiment() {
      if (!this.dummyExperiment.name) {
        window.scrollTo(0, 0)
        window.alert("Merci de renseigner le nom du retour d'expérience")
        return
      }

      this.dummyExperiment.state = "Brouillon"
      this.sendUpdateRequest()
    },
    submitExperiment() {
      if (!this.validateSubmission()) return

      this.dummyExperiment.state = "En attente de validation"
      this.sendUpdateRequest()
    },
    updateExperiment() {
      if (!this.validateSubmission()) return

      this.sendUpdateRequest()
    },
    sendUpdateRequest() {
      if (this.experiment) {
        const payload = utils.getObjectDiff(
          this.experiment,
          this.dummyExperiment
        )

        this.$store.dispatch("patchExperiment", {
          experiment: this.experiment,
          changes: payload,
        })
      } else {
        this.$store.dispatch("createExperiment", {
          payload: this.dummyExperiment,
          farmer: this.loggedFarmer,
        })
      }
    },
    closeOverlay() {
      const success = this.updateSucceeded
      this.$store.dispatch("resetExperimentEditLoadingStatus")
      if (success)
        this.$router.push({
          name: "Profile",
        })
    },
    cancelEdit() {
      this.$router.go(-1)
    },
    resetDummyExperiment() {
      if (this.experiment) {
        this.dummyExperiment = JSON.parse(JSON.stringify(this.experiment))
        this.dummyExperiment.images = this.dummyExperiment.images || []
        this.dummyExperiment.videos = this.dummyExperiment.videos || []
        this.dummyExperiment.links = this.dummyExperiment.links || []
        this.dummyExperiment.state = this.dummyExperiment.state || "Brouillon"
      }
    },
    addImages(e) {
      if (!e) return
      const files = e.target.files
      this.hasChanged = true

      for (let i = 0; i < files.length; i++) {
        const file = files[i]
        utils.toBase64(file, (base64) => {
          this.dummyExperiment.images.push({
            image: base64,
            label: "",
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
    },
    onScroll() {
      this.toolbarOnTop = window.scrollY > this.initialToolbarTop
    },
  },
  beforeMount() {
    this.resetDummyExperiment()
  },
  mounted() {
    this.initialToolbarTop =
      this.$el.querySelector("#button-toolbar").offsetTop || 0
  },
  created() {
    window.addEventListener("scroll", this.onScroll)
  },
  beforeDestroy() {
    window.removeEventListener("scroll", this.onScroll)
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
