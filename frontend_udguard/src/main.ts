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
new Vue({
  router,
  store,
  vuetify,
  render: h => h(App)
}).$mount('#app')
