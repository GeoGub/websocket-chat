<template>
  <div>
      
  </div>
</template>

<script>
    import axios from 'axios'
    export default {
      setup() {
        axios.get('http://127.0.0.1:8000/users', {withCredentials: true}).then(res => {
          console.log(res)
        })
      }
    }
</script>