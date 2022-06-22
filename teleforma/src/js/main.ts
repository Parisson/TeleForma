import "./compatibility"
import Vue from "vue"
import Chat from "./components/Chat.vue"
import Notifications from "./components/Notifications.vue"

import axios from "axios";
// default axios config
axios.defaults.xsrfHeaderName = "X-CSRFTOKEN";
axios.defaults.xsrfCookieName = "csrftoken";
axios.defaults.withCredentials = true

Vue.config.productionTip = false

if (document.getElementById("chat")) {
  new Vue({
    render: (h) => h(Chat)
  }).$mount("#chat")
}


if (document.getElementById("notifications")) {
  new Vue({
    render: (h) => h(Notifications)
  }).$mount("#notifications")
}
