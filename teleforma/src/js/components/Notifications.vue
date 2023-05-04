<template>
  <div id="notifications" @focus="open" @focusout="close" tabindex="0">
    <div class="bell">
      <img src="/static/teleforma/images/bell.svg" alt="Notifications" title="Notifications" class="bell-image" />
      <span v-if="numberOfUnread > 0" class="bell-count">{{ numberOfUnread }}</span>
    </div>
    <div v-if="opened" class="notifications-list">
      <!-- <h1 v-if="currentUserId">{{ currentUserId }}</h1>
      <h1 v-else>Pas d'utilisateur</h1> -->
      <ul>
        <NotificationMessage
          v-for="message in messages"
          :key="message._id"
          :id="message._id"
          :content="message.content"
          :url="message.url"
          :viewed="message.viewed"
          :creation-date="message.created"
        ></NotificationMessage>
      </ul>
    </div>
  </div>
</template>

<script lang="ts">
import { Component, Vue } from "vue-property-decorator"
import NotificationMessage from "./sub/NotificationMessage.vue"

@Component({
  components: {
    NotificationMessage
  }
})
export default class Notifications extends Vue {
  socket: WebSocket | null = null
  messagesLoaded = false
  messages: any[] = []
  currentUserId: number | null = null
  opened = false

  created() {
    // get room info
    const userId = document.getElementById("user_id")
    if (!userId) return
    // this.connect(`notifications_${userId}`)
    this.currentUserId = parseInt(userId.getAttribute("value")!, 10)
    this.connect()
  }

  connect() {
    // connect to socket
    let protocol = "wss"
    if (window.location.protocol != "https:") protocol = "ws"
    this.socket = new WebSocket(
      protocol + "://" + window.location.host + "/ws/notification/" + this.currentUserId + "/"
    )
    this.fetchMessages()

    this.socket.onclose = () => {
      console.log("Chat socket closed")
    }
  }

  async fetchMessages() {
    this.socket!.onmessage = (e) => {
      const data = JSON.parse(e.data)
      const type = data.type
      // debugger;
      // do not load messages in case of socket reconnect
      if (type === "initial" && this.messagesLoaded) return

      const newMessages = data.messages

      // check if a message with the same id already exists
      // it means the message have been updated (probably the "viewed" state)
      let existing = null
      if (type === "new" && newMessages.length === 1) {
        existing = this.messages.findIndex((message) => message._id === newMessages[0]._id)
      }
      
      // if it exists, then we update it instead of appending a new one
      if (existing !== null && existing !== -1){
        this.messages = [...this.messages.slice(0, existing), newMessages[0], ...this.messages.slice(existing + 1)]
      }
      else
        this.messages = [...newMessages, ...this.messages]
      if (type === "initial") this.messagesLoaded = true
    }
  }

  open() {
    this.opened = true
  }
  close() {
    this.opened = false
  }

  get numberOfUnread() {
    return this.messages.filter(message => !message.viewed).length
  }
}
</script>

<style scoped>
#notifications {
  position: absolute;
  top: 0px;
  right: 5px;
  text-align: left;
}
.bell {
  width: 40px;
  height: 40px;
  position: relative;
  cursor: pointer;
}
.bell-count {
  position: absolute;
  width: 20px;
  height: 20px;
  top: 5px;
  right: 0px;
  display: flex;
  justify-content: center;
  align-items: center;
  color: white;
  border-radius: 10px;
  background-color: red;
}

.notifications-list {
  position: absolute;
  background-color: white;
  z-index: 100;
  right: 10px;
  width: 400px;
  max-height: calc(100vh - 300px);
  max-width: calc(100vw - 50px);
  border: 1px solid lightblue;
  border-radius: 3px;
  overflow-y: scroll;
}

ul {
  margin: 0;
  padding: 0;
  box-shadow: 5px 5px 5px grey;
}
</style>
