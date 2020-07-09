<template>
  <div ref="root" v-resize="onResize" class="messages-data-table">
    <Title :breadcrumbs="breadcrumbs" />
    <v-container style="height: 100%;">
      <v-row style="height: 100%;">
        <v-col cols="3" style="border-right: 1px solid #EEE; height: 100%; overflow-y: auto; padding-right: 0;">

          <v-list dense>
            <v-list-item
              v-for="conversation in conversations"
              :key="conversation.correspondent.id"
              @click="goToConversation(conversation)"
              :class="{active: activeCorrespondent && activeCorrespondent.id === conversation.correspondent.id}"
            >
              <v-list-item-avatar color="grey">
                <v-img
                  :src="conversation.correspondent.profile_image"
                  v-if="conversation.correspondent.profile_image"
                ></v-img>
                <v-icon v-else>mdi-account</v-icon>
              </v-list-item-avatar>
              <v-list-item-content class="d-none d-sm-flex">
                <v-list-item-title style="padding-left: 0px;">{{ conversation.correspondent.name }}</v-list-item-title>
              </v-list-item-content>
            </v-list-item>
          </v-list>
        </v-col>

        <v-col cols="9" style="padding-top: 0;">
          <MessageEditor :messages="shownMessages" :activeCorrespondent="activeCorrespondent" v-if="activeCorrespondent" />
        </v-col>
      </v-row>
    </v-container>
  </div>
</template>

<script>
import Title from "@/components/Title.vue"
import MessageEditor from "@/components/MessageEditor.vue"
import utils from "@/utils"
import Constants from '@/constants'

export default {
  name: "Messages",
  components: { Title, MessageEditor },
  props: {
    farmerUrlComponent: {
      type: String
    }
  },
  data() {
    return {
      activeCorrespondent: null,
      breadcrumbs: [
        {
          text: "Accueil",
          disabled: false,
          to: { name: "Map" }
        },
        {
          text: "Mon compte",
          disabled: false,
          to: { name: "Profile" }
        },
        {
          text: "Messages",
          disabled: true
        }
      ]
    }
  },
  computed: {
    headers() {
      const largeHeaders = [
        { text: "", value: "new", sortable: false, width: 40 },
        { text: "De", value: "sender.name", width: "15%" },
        { text: "Sujet", value: "subject" },
        { text: "Message", value: "body" },
        { text: "Date", value: "sent_at", width: 130 }
      ]
      const midHeaders = [
        { text: "", value: "new", sortable: false, width: 40 },
        { text: "De", value: "sender.name", width: "20%" },
        { text: "Sujet", value: "subject" },
        { text: "Date", value: "sent_at", width: 130 }
      ]
      const smallHeaders = [
        { text: "De", value: "sender.name", width: "30%" },
        { text: "Sujet", value: "subject" }
      ]
      switch (this.$vuetify.breakpoint.name) {
        case "xs":
          return smallHeaders
        case "sm":
        case "md":
          return midHeaders
        default:
          return largeHeaders
      }
    },
    messages() {
      /*
      * The messages are returned in chronological order
      */
      const storeMessages = this.$store.state.messages || []
      return [...storeMessages].sort((a, b)=> a.sent_at < b.sent_at)
    },
    conversations() {
      /*
      * These conversations are a data structure in the form of:
      * array [
      *  { 
      *     correspondent: { id: <id>, name: <name>, farm_name: <farm_name> },
      *     messages: [<messages in inverse chronological order>]
      *  },
      *  {...},
      *  {...}
      * ]
      * The list will be sorted the conversations that contain the most recent messages
      * on top.
      */
      let conversations = []
      if (!this.loggedFarmerId) return []
      for (let i = 0; i < this.messages.length; i++) {
        const message = this.messages[i]
        const correspondent =
          message.sender.id === this.loggedFarmerId
            ? message.recipient
            : message.sender
        const element = conversations.find(
          x => x.correspondent.id === correspondent.id
        )
        if (element) element.messages.unshift(message)
        else
          conversations.push({ correspondent: correspondent, messages: [message] })
      }

      // Lastly, if we have a farmerUrlComponent designing a farmer for whom we have not 
      // communicated, we add this to the very top of the array with an empty messages array.
      // This is for the case of the first message to someone
      if (this.farmerUrlComponent) {
        const farmer = this.$store.getters.farmerWithUrlComponent(this.farmerUrlComponent)
        const element = conversations.find(
          x => x.correspondent.id === farmer.id
        )
        if (!element) {
          conversations.unshift({
            correspondent: {
              id: farmer.id,
              name: farmer.name,
              farm_name: farmer.farm_name,
              profile_image: farmer.profile_image
            },
            messages: []
          })
        }
      }

      return conversations
    },
    shownMessages() {
      if (!this.activeCorrespondent)
        return []
      return this.conversations.find(x => x.correspondent.id === this.activeCorrespondent.id).messages
    },
    loggedFarmerId() {
      return this.$store.state.loggedUser.farmer_id
    },
    loading() {
      return this.$store.state.messagesLoadingStatus === Constants.LoadingStatus.LOADING
    }
  },
  methods: {
    toReadableDate(date) {
      return utils.toReadableDate(date)
    },
    goToConversation(conversation) {
      const farmer = this.$store.getters.farmerWithId(conversation.correspondent.id)
      const urlComponent = this.$store.getters.farmerUrlComponent(farmer)
      this.$router.push({
        name: 'Messages',
        params: {
          farmerUrlComponent: urlComponent
        }
      }).catch(() => {})
    },
    onResize() {
      const navBarHeight = 64
      const titleHeight = 60
      this.$refs.root.style.height = `${window.innerHeight - navBarHeight - titleHeight}px`
    },
    autoSelectConversation() {
      /*
      * Depending on multiple factors, this method will select one of the conversations by default
      */

      // If there are no conversations, no action will be taken
      if (this.loading)
        return

      if (this.farmerUrlComponent) {

        // If the farmer specified in the URL does not exist, we fallback to the first conversation
        const farmer = this.$store.getters.farmerWithUrlComponent(this.farmerUrlComponent)
        if (!farmer && this.conversations.length > 0) {
          this.goToConversation(this.conversations[0])
          return
        }

        // If we have no conversations with the farmer specified in the URL, we fallback to the first conversation as well
        const conversation = this.conversations.find(x => x.correspondent.id === farmer.id)
        if (!conversation && this.conversations.length > 0) {
          this.goToConversation(this.conversations[0])
          return
        }

        // Otherwise, we will go to the conversation with the farmer specified in the URL
        this.activeCorrespondent = conversation.correspondent

      } else if(this.conversations.length > 0) {
        // If there was no farmer specified in the URL, we default to the first conversation
        this.goToConversation(this.conversations[0])
      }
    }
  },
  beforeCreate() {
    this.$store.dispatch("fetchMessages")
  },
  mounted() {
    if (!this.activeCorrespondent)
      this.autoSelectConversation()
  },
  watch: {
    conversations() {
      // When conversations change, we need to select one if there is no active correspondent selected
      if (!this.activeCorrespondent)
        this.autoSelectConversation()
    },
    $route(to) {
      // We need to manually update our parameters in case of a route change:
      // https://router.vuejs.org/guide/essentials/dynamic-matching.html#reacting-to-params-changes
      this.farmerUrlComponent = to.params.farmerUrlComponent
      this.autoSelectConversation()
    }
  }
}
</script>

<style scoped>
.selected {
  background: #008763;
}
.v-list-item.active {
	border-left: 4px solid #008763;
	background: #E0F4EE;
}
</style>
<style>
.messages-data-table .v-data-table table {
  table-layout: fixed;
}
.messages-data-table td.text-start {
  text-overflow: ellipsis;
  overflow: hidden;
  white-space: nowrap;
  width: 50px;
  cursor: pointer;
}
</style>