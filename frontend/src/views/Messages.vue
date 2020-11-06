<template>
  <div ref="root" v-resize="onResize" class="messages-data-table" v-if="!messagesLoading && !newCorrespondentLoading && !!loggedFarmerId">
    <Title :breadcrumbs="breadcrumbs" />
    <v-container style="height: 100%; padding-top: 5px; padding-bottom: 0;">
      <v-row style="height: 100%; border: 1px solid #EEE;">
        <v-col
          cols="2"
          sm="3"
          style="border-right: 1px solid #EEE; height: 100%; overflow-y: auto; padding: 0; background: #f9f9f9;"
        >
          <v-list dense v-if="conversations.length > 0" style="padding: 0;">
            <v-list-item
              v-for="conversation in conversations"
              :key="conversation.correspondent.id"
              @click="goToConversation(conversation)"
              :style="`padding-right:0; ${$vuetify.breakpoint.name === 'xs' ? 'padding-left: 5px; ' : ''}border-bottom: 1px solid #EEE;`"
              :class="{active: activeCorrespondent && activeCorrespondent.id === conversation.correspondent.id}"
            >
              <v-badge
                v-if="$vuetify.breakpoint.name === 'xs' && unreadMessagesNumber(conversation.messages) > 0"
                color="primary"
                overlap
                dot
              ></v-badge>
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
              <v-badge
                class="d-none d-sm-inline"
                color="primary"
                inline
                :content="unreadMessagesNumber(conversation.messages)"
                v-if="unreadMessagesNumber(conversation.messages) > 0"
              ></v-badge>
            </v-list-item>
          </v-list>
        </v-col>

        <v-col cols="10" sm="9" style="padding-top: 0; padding-bottom: 0;">
          <MessageEditor
            :messages="shownMessages"
            :activeCorrespondent="activeCorrespondent"
            v-if="activeCorrespondent && conversations.length > 0"
          />
          <MessagesEmptyView v-else />
        </v-col>
      </v-row>
    </v-container>
  </div>
</template>

<script>
import Vue from 'vue'
import Title from "@/components/Title.vue"
import MessageEditor from "@/components/MessageEditor.vue"
import utils from "@/utils"
import Constants from "@/constants"
import MessagesEmptyView from "@/components/MessagesEmptyView.vue"

export default {
  name: "Messages",
  components: { Title, MessageEditor, MessagesEmptyView },
  props: {
    farmerUrlComponent: {
      type: String
    }
  },
  data() {
    return {
      activeCorrespondent: null,
      newCorrespondent: null,
      breadcrumbs: [
        {
          text: "Accueil",
          disabled: false,
          to: { name: "Landing" }
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
    messages() {
      /*
       * The messages are returned in chronological order
       */
      const storeMessages = this.$store.state.messages || []
      return [...storeMessages].sort((a, b) => {
        if (a.sent_at < b.sent_at)
          return 1
        if (a.sent_at > b.sent_at)
          return -1
        return 0
      })
    },
    conversations() {
      /*
       * These conversations are a data structure in the form of:
       * array [
       *  {
       *     correspondent: { id: <id>, name: <name>, farm_name: <farm_name>, sequence_number: <seq_number>... },
       *     messages: [<messages in inverse chronological order>]
       *  },
       *  {...},
       *  {...}
       * ]
       * The list will be sorted the conversations that contain the most recent messages
       * on top.
       */
      if (!this.loggedFarmerId || this.messagesLoading) return []

      let conversations = []

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
          conversations.push({
            correspondent: correspondent,
            messages: [message]
          })
      }

      // Lastly, if we have a newCorrespondent we add this to the very top
      // of the array with an empty messages array.
      // This is for the case of the first message to someone
      if (this.newCorrespondent) {
        conversations.unshift({
          correspondent: {
            id: this.newCorrespondent.id,
            name: this.newCorrespondent.name,
            farm_name: this.newCorrespondent.farm_name,
            profile_image: this.newCorrespondent.profile_image,
            agriculture_types: this.newCorrespondent.agriculture_types,
            groups: this.newCorrespondent.groups,
            production: this.newCorrespondent.production,
            sequence_number: this.newCorrespondent.sequence_number,
            url_slug: this.newCorrespondent.url_slug
          },
          messages: []
        })
      }

      return conversations
    },
    shownMessages() {
      if (!this.activeCorrespondent) return []
      return this.conversations.find(
        x => x.correspondent.id === this.activeCorrespondent.id
      ).messages
    },
    loggedFarmerId() {
      if (this.$store.state.loggedUser)
        return this.$store.state.loggedUser.farmer_id
      return null
    },
    messagesLoading() {
      return (
        this.$store.state.messagesLoadingStatus ===
        Constants.LoadingStatus.LOADING || 
        this.$store.state.messagesLoadingStatus ===
        Constants.LoadingStatus.IDLE
      )
    },
    newCorrespondentLoading() {
      return this.$store.state.farmersLoadingStatus ===
        Constants.LoadingStatus.LOADING
    }
  },
  methods: {
    toReadableDate(date) {
      return utils.toReadableDate(date)
    },
    goToConversation(conversation) {
      const urlComponent = conversation.correspondent.url_slug
      this.$router
        .push({
          name: "Messages",
          params: {
            farmerUrlComponent: urlComponent
          }
        })
        .catch(() => {})
    },
    onResize() {
      const navBarHeight = 64
      const titleHeight = this.$vuetify.breakpoint.name === 'xs' ? 40 : 60
      this.$refs.root.style.height = `${window.innerHeight -
        navBarHeight -
        titleHeight}px`
    },
    autoSelectConversation() {
      // If there are no messages there is nothing to select
      if (this.messagesLoading || this.conversations.length === 0)
        return

      // If we have messages from the farmer specified in the URL, we select them.
      // Otherwise we select the first conversation
      const conversation = this.farmerUrlComponent ? this.conversations.find(
        x => x.correspondent.url_slug === this.farmerUrlComponent
      ) : null
      if (conversation) {
        this.goToConversation(conversation)
        this.activeCorrespondent = conversation.correspondent
      } else {
        this.goToConversation(this.conversations[0])
      }
    },
    unreadMessagesNumber(messages) {
      if (!this.loggedFarmerId) return 0
      return messages.filter(
        x => x.recipient.id === this.loggedFarmerId && x.new
      ).length
    },
    fetchNewCorrespondentIfNeeded() {
      if (this.messagesLoading)
        return

      // We need to look for the new correspondent if we have a url_slug in the URL that is not present in any
      // existing messages.
      if (!this.farmerUrlComponent || this.messages.find(x => x.sender.url_slug === this.farmerUrlComponent || x.recipient.url_slug === this.farmerUrlComponent)) {
        this.newCorrespondent = null
        return
      }

      const farmer = this.$store.getters.farmerWithUrlComponent(this.farmerUrlComponent)
      if (farmer)
        this.newCorrespondent = farmer

      let sequenceNumber
      try {
        sequenceNumber = this.farmerUrlComponent.split('--')[1]
      } catch (error) {
        return
      }

      this.$store.commit('SET_FARMERS_LOADING', Constants.LoadingStatus.LOADING)
      Vue.http.get(`/api/v1/farmers/${sequenceNumber}`).then(response => {
        this.$store.commit('SET_FARMERS_LOADING', Constants.LoadingStatus.SUCCESS)
        this.$store.commit('ADD_FARMER', response.body)
        this.newCorrespondent = response.body
      }).catch(() => {
        this.$store.commit('SET_FARMERS_LOADING', Constants.LoadingStatus.IDLE)
      })
    },
},
  mounted() {
    this.fetchNewCorrespondentIfNeeded()
    if (!this.activeCorrespondent && this.loggedFarmerId) this.autoSelectConversation()
  },
  watch: {
    messages() {
      this.fetchNewCorrespondentIfNeeded()
    },
    conversations() {
      // When conversations change, we need to select one if there is no active correspondent selected
      if (!this.activeCorrespondent) this.autoSelectConversation()
    },
    $route(to) {
      // We need to manually update our parameters in case of a route change:
      // https://router.vuejs.org/guide/essentials/dynamic-matching.html#reacting-to-params-changes
      this.$emit('update:farmerUrlComponent', to.params.farmerUrlComponent)
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
  background: #e0f4ee;
}
.v-badge--dot {
  margin-top: -30px;
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