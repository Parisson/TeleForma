import Vue from "vue"
import Chat from "./components/Chat.vue"

Vue.config.productionTip = false

new Vue({
  render: (h) => h(Chat)
}).$mount("#chat")
