import 'vuetify/styles' // Global CSS has to be imported
import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import { createVuetify } from 'vuetify'
import { loadFonts } from './plugins/webfontloader'
import * as components from 'vuetify/components'
import * as directives from 'vuetify/directives'
import '@mdi/font/css/materialdesignicons.css'
import { store } from './stores'

loadFonts()
const vuetify = createVuetify({
  components,
  directives,
  ssr: true,
  icons: {
    iconfont: 'mdi', // default - only for display purposes
  },
})
createApp(App)
  .use(router)
  .use(vuetify)
  .use(store)
  .mount('#app')
