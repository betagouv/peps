<template>
  <div ref="root" class="flex-column d-flex" v-resize="onResize">
    <OverlayMessage
      :visible="messageFailed"
      title="Oups ! Une erreur est survenue"
      body="Veuillez réessayer plus tard"
      :showCloseButton="true"
      @done="resetLoadingError"
    />
    <div style="box-shadow: 0px 5px 2px -3px #39393933;z-index: 2; padding-bottom: 3px;">
      <div :class="mobileView ? 'subtitle-2' : 'title'">
        <span class="d-none d-sm-inline">Conversation avec</span>
        {{activeCorrespondent.name}}
      </div>
      <div v-if="activeCorrespondent.farm_name" class="caption">{{activeCorrespondent.farm_name}}</div>
      
    </div>
    <v-divider style="margin-bottom: 0px"></v-divider>
    
    <div ref="messageContainer" class="flex-grow-1" style="overflow-y: auto; padding-top:10px;">
      <div v-for="(message, index) in messages" :key="index">
        <v-card
          outlined
          style="margin-bottom: 10px; width: 90%"
          :class="{'user-message': userIsSender(message)}"
          :color="userIsSender(message) ? '#E0F4EE' : '#EEE'"
        >
          <v-card-text :class="`pa-2 secondary--text ${mobileView ? 'caption' : 'body-2'}`">{{message.body}}</v-card-text>
          <v-card-subtitle
            style="padding-top: 0 !important; padding-bottom: 5px !important;"
            class="caption pa-2 grey--text d-none d-sm-block"
          >{{toReadableDate(message.sent_at)}}</v-card-subtitle>
        </v-card>
      </div>
    </div>

    <v-divider style="margin-bottom: 10px"></v-divider>

    <div class="d-flex d-sm-block align-center">
      <v-textarea
        :rows="mobileView ? 1 : 3"
        outlined
        :placeholder="mobileView ? 'Écrivez ici...' : 'Écrivez votre message ici...'"
        hide-details="auto"
        validate-on-blur
        :class="mobileView ? 'ma-0 caption' : 'ma-2'"
        v-model="messageText"
      ></v-textarea>
      <v-btn fab style="margin-left: 5px;" small class="d-sm-none" :disabled="messageText.length === 0" @click="sendMessage">
        <v-icon small color="primary">mdi-send</v-icon>
      </v-btn>

      <v-toolbar dense flat class="d-none d-sm-block">
        <v-spacer></v-spacer>

        <v-btn
          color="primary"
          class="text-none"
          :disabled="messageText.length === 0"
          @click="sendMessage"
        >
          <v-icon style="margin-right: 5px;">mdi-send</v-icon>Envoyer
        </v-btn>
      </v-toolbar>
    </div>
  </div>
</template>

<script>
import utils from "@/utils"
import Constants from "@/constants"
import OverlayMessage from "@/components/OverlayMessage.vue"

export default {
  name: "MessageEditor",
  components: {
    OverlayMessage,
  },
  data() {
    return {
      messageText: "",
    }
  },
  metaInfo() {
    return {
      title: "Peps - Messages",
      meta: [{ description: "" }],
    }
  },
  props: {
    messages: {
      type: Array,
      required: true,
    },
    activeCorrespondent: {
      type: Object,
      required: true,
    },
  },
  computed: {
    messageFailed() {
      return (
        this.$store.state.messagesLoadingStatus ===
        Constants.LoadingStatus.ERROR
      )
    },
    mobileView() {
      return this.$vuetify.breakpoint.name === 'xs'
    }
  },
  methods: {
    toReadableDate(date) {
      return utils.toReadableDate(date)
    },
    userIsSender(message) {
      return message.sender.id === this.$store.state.loggedUser.farmer_id
    },
    onResize() {
      const margin = this.$vuetify.breakpoint.name === "xs" ? 110 : 150
      this.$refs.root.style.height = `${window.innerHeight - margin}px`
      this.$refs.root.style.maxHeight = `${window.innerHeight - margin}px`
    },
    sendMessage() {
      const body = this.messageText
      const correspondent = this.activeCorrespondent.id
      this.$store.dispatch("createMessage", { body, recipient: correspondent })
      this.messageText = ""
    },
    markAsRead() {
      const unreadMessages = this.messages.filter(
        (x) => x.new && !this.userIsSender(x)
      )
      if (unreadMessages.length > 0)
        this.$store.dispatch("markAsRead", { messages: unreadMessages })
    },
    resetLoadingError() {
      this.$store.dispatch("resetMessagesLoadingStatus")
    },
  },
  mounted() {
    const elem = this.$refs.messageContainer
    elem.scrollTop = elem.scrollHeight
    this.markAsRead()
  },
  updated() {
    const elem = this.$refs.messageContainer
    elem.scrollTop = elem.scrollHeight
    this.markAsRead()
  },
}
</script>
<style scoped>
.user-message {
  margin-left: 10%;
}
</style>