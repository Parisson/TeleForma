<template>
  Notification
</template>

<script lang="ts">
import { Component, Vue } from "vue-property-decorator"

@Component({
})
export default class Notification extends Vue {
  socket: WebSocket | null = null
  messagesLoaded = false
  messages: Messages = []
  currentUserId: number | null = null

  created() {
    // get room info
    const userId = document.getElementById("user_id")
    this.connect(roomInfo.room_name)
    this.currentUserId = userId
  }

  connect(roomName: string) {
    // connect to socket
    let protocol = "wss"
    if (window.location.protocol != "https:") protocol = "ws"
    this.socket = new WebSocket(protocol + "://" + window.location.host + "/ws/notification/" + this.currentUserId + "/")
    this.fetchMessages()

    this.socket.onclose = () => {
      console.log("Chat socket closed")
    }
  }

  async fetchMessages() {
    this.socket!.onmessage = (e) => {
      const data = JSON.parse(e.data)
      const type = data.type
      // do not load messages in case of socket reconnect
      if (type == "initial" && this.messagesLoaded) return
      const newMessages = data.messages as Message[]
      this.messages = [...this.messages, ...newMessages]
      if (type == "initial") this.messagesLoaded = true
    }
  }
}
</script>

<style>
.vac-message-wrapper .vac-offset-current {
  margin-left: 15%;
}
.vac-message-wrapper .vac-message-box {
  max-width: 80%;
}
</style>
