<template>
  <v-container fluid>
    <v-list
      height="80vh"
      width="80vw"
      ref='list'
    >
      <template v-for="(message, index) in messages">
        <v-divider
        ></v-divider>
        <v-list-item
        >
        <v-list-item-title v-text="message.senderId">
        </v-list-item-title>
        <v-list-item-subtitle v-text="message.message"></v-list-item-subtitle>
        </v-list-item>
      </template>
    </v-list>
    <v-row>
      <v-col
        cols="6"
      >
        <v-textarea
        solo
        name="input-7-4"
        rows="2"
        no-resize
        v-model="this.value"
        ></v-textarea>
      </v-col>
      <v-col>
        <v-btn
        v-on:click="send_message"
        >
          Send
        </v-btn>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
  import axios from 'axios';

  export default {
    async created() {
      this.ws = new WebSocket('ws://localhost:8000/websocket/ws');
      await axios.get('http://localhost:8000/messages')
        .then(res => {
          this.messages = res.data.items.reverse()
        })
        console.log(this.messages)
        this.ws.onmessage = this.onMessage
    },
    data: () => ({
      ws: null,
      messages: [],
      value: '',
      list: null,
    }),
    methods: {
      onMessage(event) {
        console.log(event.data)
        this.messages.push(JSON.parse(event.data))
        console.log(this.messages)
      },
      send_message() {
        let data = {
          message: this.value,
          senderId: 1
        }
        this.ws.send(JSON.stringify(data))
        this.value = ''
        
      }
    }
  }
</script>