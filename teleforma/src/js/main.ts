import "./compatibility"
import Vue from "vue"
import Chat from "./components/Chat.vue"
import Notification from "./components/Notification.vue"

Vue.config.productionTip = false

if (document.getElementById("chat")) {
  new Vue({
    render: (h) => h(Chat)
  }).$mount("#chat")
}


if (document.getElementById("notification")) {
  new Vue({
    render: (h) => h(Notification)
  }).$mount("#notification")
}
