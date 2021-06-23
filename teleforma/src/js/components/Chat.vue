<template>
  <chat-window
    :current-user-id="currentUserId"
    :rooms-loaded="rooms.length > 0"
    :messages-loaded="messagesLoaded"
    :single-room="true"
    :rooms="rooms"
    :show-files="false"
    :show-emojis="true"
    :show-reaction-emojis="false"
    :show-audio="false"
    :messages="messages"
    :message-actions="[]"
    :link-options="{ disabled: false, target: '_blank' }"
    :text-messages="{
      ROOMS_EMPTY: 'Aucune conversation',
      ROOM_EMPTY: 'Aucune conversation sélectionnée',
      NEW_MESSAGES: 'Nouveaux messages',
      MESSAGE_DELETED: 'Ce message a été supprimé',
      MESSAGES_EMPTY: 'Aucun message',
      CONVERSATION_STARTED: 'La conversation a commencée le :',
      TYPE_MESSAGE: 'Tapez votre message',
      SEARCH: 'Rechercher',
      IS_ONLINE: 'est en ligne',
      LAST_SEEN: 'dernière connexion ',
      IS_TYPING: 'est en train de taper...'
    }"
    @send-message="sendMessage"
  />
</template>

<script lang="ts">
import { Component, Vue } from "vue-property-decorator"
import ChatWindow, { Message, Messages, Rooms } from "vue-advanced-chat"
import axios from "axios"

import "vue-advanced-chat/dist/vue-advanced-chat.css"

@Component({
  components: {
    ChatWindow
  }
})
export default class Chat extends Vue {
  socket: WebSocket | null = null
  rooms: Rooms = [
    {
      roomId: "global",
      roomName: "",
      users: []
    }
  ]
  messagesLoaded = false
  messages: Messages = []
  currentUserId: number | null = null

  created() {
    // get room info
    let roomInfoStr: string | null = ""
    const roomInfoElm = document.getElementById("room-info")
    if (roomInfoElm) roomInfoStr = roomInfoElm.textContent
    let roomInfo: any = null
    if (roomInfoStr) roomInfo = JSON.parse(roomInfoStr)
    else throw "No room info provided"

    this.rooms = [
      {
        roomId: roomInfo.room_name,
        roomName: roomInfo.room_title,
        // add fake users to make sure username are displayed in the chat (if less than two, name are not displayed)
        users: [
          {
            _id: 1,
            username: "Fake user 1",
            avatar: "assets/imgs/doe.png",
            status: {
              state: "online",
              lastChanged: "today, 14:30"
            }
          },
          {
            _id: 2,
            username: "Fake user 2",
            avatar: "assets/imgs/snow.png",
            status: {
              state: "online",
              lastChanged: "14 July, 20:00"
            }
          },
          {
            _id: 3,
            username: "Fake user 3",
            avatar: "assets/imgs/snow.png",
            status: {
              state: "online",
              lastChanged: "14 July, 20:00"
            }
          }
        ]
      }
    ]
    this.connect(roomInfo.room_name)
    this.currentUserId = roomInfo.user_id
  }

  connect(roomName: string) {
    // connect to socket
    let protocol = "wss"
    if (window.location.protocol != "https:")
      protocol = "ws"
    this.socket = new WebSocket(protocol + "://" + window.location.host + "/ws/chat/" + roomName + "/")
    this.fetchMessages()

    this.socket.onclose = () => {
      console.error("Chat socket closed unexpectedly")
      // retry to connect
      setTimeout(() => {
        this.connect(roomName)
      }, 10000)
    }
  }

  async mounted() {
    await this.fetchMessages()
  }

  async fetchMessages() {
    const roomId = this.rooms[0].roomId
    this.messagesLoaded = false
    try {
      const response = await axios.get("/chat/messages", {
        params: {
          room_name: roomId
        }
      })
      this.messages = response.data
      this.messagesLoaded = true
    } catch (error) {
      console.error(error)
    }
    this.socket!.onmessage = (e) => {
      const data = JSON.parse(e.data) as Message
      this.messages = [...this.messages, data]
    }
  }

  sendMessage({ content }: { content: Message }) {
    this.socket!.send(
      JSON.stringify({
        message: content
      })
    )
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