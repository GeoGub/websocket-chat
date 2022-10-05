<template>
  <v-form>
    <v-container>
      <v-row>
        <v-col
          cols="12"
          md="4"
        >
          <v-text-field
            :counter="10"
            label="Login"
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
          :counter="10"
          label="Password"
          required
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
      @click="validate"
    >
      Login
    </v-btn>
        </v-col>
      </v-row>
    </v-container>
  </v-form>
</template>

<script>
  export default {
    data: () => ({
      valid: true,
    }),
    methods: {
      validate() {
        console.log("Login")
      },
    },
  }
</script>