<template>
  <v-form>
    <v-container>
      <v-row>
        <v-col
          cols="12"
          md="4"
        >
          <v-text-field
          v-model="username"
            :counter="10"
            label="Username"
            required
          ></v-text-field>
        </v-col>
      </v-row>
      <v-row>
        <v-col
        cols="12"
        md="4"
      >
      <v-text-field
      v-model="password"
      :append-icon="show1 ? 'mdi-eye' : 'mdi-eye-off'"
      :type="show1 ? 'text' : 'password'"
      hint="At least 8 characters"
      @click:append="show1 = !show1"
    ></v-text-field>
      </v-col>
      </v-row>
      <v-row>
        <v-col
        cols="12"
        md="4"
      >
      <v-btn
      :disabled="!valid"
      color="success"
      class="mr-4"
      @click="login"
    >
      Login
    </v-btn>
        </v-col>
      </v-row>
    </v-container>
  </v-form>
  <v-btn
  :disabled="!valid"
  color="success"
  class="mr-4"
  @click="get_me"
>
  Me
</v-btn>
</template>

<script>
  import axios from 'axios'
  export default {
    setup() {
      if (this.$store.state.user!==null) {
        this.$router.push('/im')
      }
    },
    data: () => ({
      show1: false,
      show2: true,
      valid: true,
      username: '',
      password: '',
    }),
    methods: {
      login() {
        console.log(this.$store.state.user)
        axios.post('http://127.0.0.1:8000/auth/login', {
          username: this.username,
          password: this.password
        }, {withCredentials: true})
        .then(response => {
          this.get_me()
        })
      },
      get_me() {
        axios.get('http://127.0.0.1:8000/auth/me', {withCredentials: true})
        .then(res => {
          this.$store.state.user = res.data
          this.$router.push('/im')
        })
      }
    },
  }
</script>