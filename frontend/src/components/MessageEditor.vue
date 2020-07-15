<template>
  <div ref="root" class="flex-column d-flex" v-resize="onResize">
    <div class="title">Conversation avec {{activeCorrespondent.name}}</div>
    <div v-if="activeCorrespondent.farm_name" class="caption">{{activeCorrespondent.farm_name}}</div>
    <v-divider style="margin-bottom: 10px"></v-divider>
    <div ref="messageContainer" class="flex-grow-1" style="overflow-y: auto;">
      <div v-for="(message, index) in messages" :key="index">
        <v-card
          outlined
          style="margin-bottom: 10px; width: 90%"
          :class="{'is-receiver': !userIsSender(message)}"
          :color="userIsSender(message) ? '#EEE' : '#E0F4EE'"
        >
          <v-card-text class="pa-2 body-2 black--text">{{message.body}}</v-card-text>
          <v-card-subtitle
            style="padding-top: 0 !important;"
            class="caption pa-2"
          >{{toReadableDate(message.sent_at)}}</v-card-subtitle>
        </v-card>
      </div>
    </div>

    <v-divider style="margin-bottom: 10px"></v-divider>

    <div class>
      <v-textarea
        rows="3"
        outlined
        placeholder="Écrivez votre message ici..."
        hide-details="auto"
        validate-on-blur
        class="ma-2"
        v-model="messageText"
      ></v-textarea>
      <v-toolbar dense flat>
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

export default {
  name: "MessageEditor",
  data() {
    return {
      messageText: ''
    }
  },
  props: {
    messages: {
      type: Array,
      required: true
    },
    activeCorrespondent: {
      type: Object,
      required: true
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
      const margin = 150
      this.$refs.root.style.height = `${window.innerHeight - margin}px`
      this.$refs.root.style.maxHeight = `${window.innerHeight - margin}px`
    },
    sendMessage() {
      const body = this.messageText
      const correspondent = this.activeCorrespondent.id
      this.$store.dispatch("createMessage", { body, recipient: correspondent })
      this.messageText = ''
    },
    markAsRead() {
      const unreadMessages = this.messages.filter(x => x.new && !this.userIsSender(x))
      if (unreadMessages.length > 0)
        this.$store.dispatch("markAsRead", {messages: unreadMessages})
    }
  },
  mounted() {
    const elem = this.$refs.messageContainer
    elem.scrollTop = elem.scrollHeight
  },
  updated() {
    const elem = this.$refs.messageContainer
    elem.scrollTop = elem.scrollHeight
    this.markAsRead()
  }
}
</script>
<style scoped>
.is-receiver {
  margin-left: 10%;
}
</style>