import "./compatibility"
import Vue from "vue"
import Chat from "./components/Chat.vue"

Vue.config.productionTip = false

if (document.getElementById("chat")) {
  new Vue({
    render: (h) => h(Chat)
  }).$mount("#chat")
}
