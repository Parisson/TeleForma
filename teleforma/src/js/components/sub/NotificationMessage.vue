<template>
  <li @click="onClick()" @click.middle="onMiddleClick()">
    <span :class="{ 'unviewed': !viewed, text: true }">{{ id }} - {{ content }} - {{ viewed }}</span>
    <span class="date">{{ relativeCreationDate }} </span>
  </li>
</template>

<script lang="ts">
import { Component, Vue } from "vue-property-decorator"
import { formatRelative } from "date-fns"
import { fr } from "date-fns/locale"
import axios from "axios"

// Define the props by using Vue's canonical way.
const NotificationMessageProps = Vue.extend({
  props: {
    id: Number,
    content: String,
    url: String,
    viewed: Boolean,
    creationDate: String
  }
})

@Component
export default class NotificationMessage extends NotificationMessageProps {

  async setAsViewed() {
    if (this.$props.viewed === false) {
      await axios.post("/notification", { id: this.$props.id, viewed: true })
    }
  }

  async onClick() {
    this.setAsViewed()
    if (this.$props.url) window.location.href = this.$props.url
  }

  async onMiddleClick() {
    this.setAsViewed()
    if (this.$props.url) window.open(this.$props.url, '_blank');
  }

  get relativeCreationDate() {
    return formatRelative(new Date(this.$props.creationDate), new Date(), { locale: fr })
  }
}
</script>

<style scoped>
li {
  list-style: none;
  display: block;
  align-items: center;
  margin: 0;
  border-radius: 0;
  padding: 10px;
  cursor: pointer;
  overflow: hidden;
}
li:hover {
  background-color: #ccf2cf;
}
li:not(:last-child) {
  border-bottom: 1px solid lightblue;
}

.unviewed {
  font-weight: bold;
}
.date {
    float: right;
    color: lightslategrey;
    font-size: 0.9em;
    font-style: italic;
}
</style>
