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

        <v-btn class="text-none" :disabled="!hasChanged" color="primary">
          <v-icon>mdi-content-save</v-icon>Sauvegarder les changements
        </v-btn>
      </v-toolbar>

      <div class="field">
        <div class="field-title title">Titre de l'expérimentation</div>
        <div
          class="field-helper subtitle-2 grey--text"
        >Court et explicite, il doit donner l'idée générale</div>
        <v-text-field
          :rules="[validators.textNotEmpty]"
          @input="hasChanged = true"
          outlined
          dense
          v-model="dummyExperiment.name"
        ></v-text-field>
      </div>

      <div class="field">
        <div class="field-title title">De quel type d'expérimentation s'agit-il ?</div>
        <v-radio-group @change="hasChanged = true" v-model="dummyExperiment.xp_type" :mandatory="false">
          <v-radio label="Changement important de l'exploitation" value="Changement important de l'exploitation"></v-radio>
          <v-radio label="Amélioration de l'existant" value="Amélioration de l'existant"></v-radio>
        </v-radio-group>
      </div>

      <div class="field">
        <div
          class="field-title title"
        >Dans quels objectifs plus global de l'exploitation cela s'inscrit ?</div>
        <v-textarea
          :rules="[validators.textNotEmpty]"
          rows="1"
          @input="hasChanged = true"
          auto-grow
          outlined
          dense
          v-model="dummyExperiment.objectives"
        ></v-textarea>
      </div>

      <div class="field">
        <div class="field-title title">L'expérimentation est-elle en cours aujourd'hui ?</div>
        <div
          class="field-helper subtitle-2 grey--text"
        >Si l'expérimentation a été intégrée à l'exploitation et est améliorée à la marge, dites Non</div>
        <v-radio-group @change="hasChanged = true" v-model="dummyExperiment.ongoing" :mandatory="false">
          <v-radio label="Oui" :value="true"></v-radio>
          <v-radio label="Non" :value="false"></v-radio>
        </v-radio-group>
      </div>

      <div class="field">
        <div
          class="field-title title"
        >Quels investissements ont été nécessaires pour cette expérimentation ?</div>
        <div class="field-helper subtitle-2 grey--text">En temps, en argent, en machines...</div>
        <v-textarea
          :rules="[validators.textNotEmpty]"
          rows="1"
          @input="hasChanged = true"
          auto-grow
          outlined
          dense
          v-model="dummyExperiment.investment"
        ></v-textarea>
      </div>

      <div class="field">
        <div
          class="field-title title"
        >Quel matériel avez-vous utilisé pour mener cette expérimentation ?</div>
        <div class="field-helper subtitle-2 grey--text">Vous pouvez ici être assez spécifique</div>
        <v-textarea
          rows="1"
          @input="hasChanged = true"
          auto-grow
          outlined
          dense
          v-model="dummyExperiment.equipment"
        ></v-textarea>
      </div>




      <div class="field">
        <div class="field-title title">Pouvez-vous décrire l'expérimentation ?</div>
        <div
          class="field-helper subtitle-2 grey--text"
        >Dites comment cela s'est déroulé, ce que vous avez observé, les choses que vous avez apprises...</div>
        <v-textarea
          :rules="[validators.textNotEmpty]"
          rows="1"
          @input="hasChanged = true"
          auto-grow
          outlined
          dense
          v-model="dummyExperiment.description"
        ></v-textarea>
      </div>
      <!-- <div class="field">
        <div class="field-title title">Combien d'ha cela représente ?</div>
        <v-textarea
          @change="hasChanged = true"
          rows="1"
          auto-grow
          outlined
          dense
          v-model="dummyExperiment.surface"
        ></v-textarea>
      </div> -->

      <div class="field">
        <div class="field-title title">Avez-vous mis en place un témoin ?</div>
        <div
          class="field-helper subtitle-2 grey--text"
        >C'est à dire une surface similaire qui permet de valider les résultats obtenus 
Si ce n'est pas pertinent, dites Non</div>
        <v-radio-group @change="hasChanged = true" v-model="dummyExperiment.control_presence" :mandatory="false">
          <v-radio label="Oui" :value="true"></v-radio>
          <v-radio label="Non" :value="false"></v-radio>
        </v-radio-group>
      </div>

      <div class="field">
        <div class="field-title title">Quels sont les résultats de cette expérimentation ?</div>
        <v-radio-group @change="hasChanged = true" v-model="dummyExperiment.results" :mandatory="false">
          <v-radio label="XP qui fonctionne, elle est intégrée à l'exploitation" value="XP qui fonctionne, elle est intégrée à l'exploitation"></v-radio>
          <v-radio label="XP prometteuse, en cours d'amélioration" value="XP prometteuse, en cours d'amélioration"></v-radio>
          <v-radio label="XP abandonnée, les résultats ne sont pas satisfaisants" value="XP abandonnée, les résultats ne sont pas satisfaisants"></v-radio>
          <v-radio label="XP en suspens, les conditions ne sont plus réunies" value="XP en suspens, les conditions ne sont plus réunies"></v-radio>
          <v-radio label="XP qui commence, les premiers résultats sont à venir" value="XP qui commence, les premiers résultats sont à venir"></v-radio>
        </v-radio-group>
      </div>


      <div class="field">
        <div class="field-title title">Pouvez-vous détailler les résultats ?</div>
        <div
          class="field-helper subtitle-2 grey--text"
        >Vous pouvez ici donner des chiffres, détailler les résultats des différents tests que vous avez fait si ça a été le cas...</div>
        <v-textarea
          rows="1"
          @input="hasChanged = true"
          auto-grow
          outlined
          dense
          v-model="dummyExperiment.results_details"
        ></v-textarea>
      </div>

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
        <v-btn @click="close()" class="close-overlay" fab dark small color="grey lighten-5">
          <v-icon color="red darken-3">mdi-close</v-icon>
        </v-btn>
        <v-card :style="'max-width: 600px;'" class="overflow-y-auto">
          <v-card-text style="padding: 30px; color: #333;">
            <span v-if="updateSucceeded">
              <v-icon style="margin-top: -3px; margin-right: 5px;">mdi-check-circle</v-icon>Votre expérimentation a bien été mise à jour !
            </span>
            <span v-else>
              <v-icon style="margin-top: -3px; margin-right: 5px;">mdi-emoticon-sad-outline</v-icon>Oops ! On a pas pu mettre à jour l'expérimentation. Veuillez essayer plus tard.
            </span>
          </v-card-text>
          <div style="padding: 10px; text-align: right">
            <v-btn
              class="text-none body-1 practice-buttons"
              color="primary"
              @click="resetLoadingStatus()"
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
  name: "ExperimentEditor",
  components: { Title, Loader },
  props: {
    experimentName: {
      type: String,
      default: null
    }
  },
  data() {
    return {
      dummyExperiment: {},
      hasChanged: false
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
    loggedUser() {
      return this.$store.state.loggedUser
    },
    farmer() {
      if (!this.loggedUser || !this.loggedUser.farmer_external_id) return null
      return this.$store.getters.farmerWithExternalId(
        this.loggedUser.farmer_external_id
      )
    },
    experiment() {
      if (!this.farmer || !this.experimentName) return
      return this.farmer.experiments.find(x => x.name === this.experimentName)
    },
    breadcrumbs() {
      return [
        {
          text: "Carte des expérimentations",
          disabled: false,
          href: "/#/map"
        },
        {
          text: "Mon compte",
          disabled: false,
          href: "/#/compte"
        },
        {
          text: this.experiment.name,
          disabled: true
        }
      ]
    }
  },
  methods: {
    updateExperiment() {
      const payload = utils.getObjectDiff(this.experiment, this.dummyExperiment)
      if (this.experiment) {
        this.$store.dispatch("patchExperiment", {
          experiment: this.experiment,
          changes: payload
        })
      } else {
        // Create new experiment
      }
    },
    resetLoadingStatus() {
      this.$store.dispatch("resetExperimentEditLoadingStatus")
    },
    cancelEdit() {
      this.$router.go(-1)
    },
    resetDummyExperiment() {
      if (this.experiment)
        this.dummyExperiment = Object.assign(
          this.dummyExperiment,
          this.experiment
        )
      else if (this.experimentName) window.alert("XP not found") //  TODO: Change this
    }
  },
  beforeMount() {
    this.resetDummyExperiment()
  }
}
</script>

<style scoped>
.field {
  margin-bottom: 30px;
}
.field-helper {
  margin-bottom: 5px;
}
</style>

<style>
/* #xp-edit .v-text-field--outlined fieldset {
  border-color: #c8c8c8;
} */
</style>
