/* eslint-disable */
import Vue from 'vue'
import App from './App.vue'
import router from './router'
import store from './store'
import vuetify from './plugins/vuetify'
import VueSweetalert2 from 'vue-sweetalert2'
import axios from './plugins/Axios'
import 'sweetalert2/dist/sweetalert2.min.css'
import '@mdi/font/css/materialdesignicons.css'
import '@/styles/dark_mode.css'
import '@/styles/auth.css'
import '@/styles/dashboard.css'
import '@/styles/dashboard_facts.css'

Vue.config.productionTip = false
Vue.use(VueSweetalert2)
Vue.prototype.$axios = axios

// Configurar Event Bus global para comunicación entre componentes
Vue.prototype.$eventBus = new Vue()

// Declaración de tipos para TypeScript
declare module 'vue/types/vue' {
  interface Vue {
    $eventBus: Vue
  }
}

// Inicializar dark mode antes de montar la aplicación
const savedDarkMode = localStorage.getItem('darkMode')
if (savedDarkMode) {
  const isDark = JSON.parse(savedDarkMode)
  document.documentElement.classList.toggle('dark-mode', isDark)
  document.body.classList.toggle('dark-mode', isDark)
} else {
  // Detectar preferencia del sistema
  const prefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches
  document.documentElement.classList.toggle('dark-mode', prefersDark)
  document.body.classList.toggle('dark-mode', prefersDark)
}

new Vue({
  router,
  store,
  vuetify,
  render: h => h(App),
  created() {
    // Inicializar dark mode en el store al crear la app
    this.$store.dispatch('initDarkMode')
    
    // Listener global para cambios de tema del sistema
    window.matchMedia('(prefers-color-scheme: dark)').addEventListener('change', (e) => {
      if (!localStorage.getItem('darkMode')) {
        // Solo aplicar preferencia del sistema si el usuario no ha configurado manualmente
        this.$store.commit('SET_DARK_MODE', e.matches)
      }
    })
  }
}).$mount('#app')