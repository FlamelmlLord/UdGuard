// store/index.ts - Versión mejorada
import Vue from 'vue'
import Vuex from 'vuex'

Vue.use(Vuex)

interface RootState {
  darkMode: boolean
}

export default new Vuex.Store<RootState>({
  state: {
    darkMode: false
  },
  mutations: {
    SET_DARK_MODE(state, value: boolean) {
      state.darkMode = value
      localStorage.setItem('darkMode', JSON.stringify(value))
      
      // Aplicar clase al document.documentElement en lugar de body
      document.documentElement.classList.toggle('dark-mode', value)
      document.body.classList.toggle('dark-mode', value)
      
      // Emit evento global para componentes que lo necesiten
      Vue.prototype.$eventBus.$emit('dark-mode-changed', value)
    }
  },
  actions: {
    toggleDarkMode({ commit, state }) {
      commit('SET_DARK_MODE', !state.darkMode)
    },
    initDarkMode({ commit }) {
      const savedDarkMode = localStorage.getItem('darkMode')
      if (savedDarkMode) {
        const isDark = JSON.parse(savedDarkMode)
        commit('SET_DARK_MODE', isDark)
      } else {
        // Detectar preferencia del sistema si no hay configuración guardada
        const prefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches
        commit('SET_DARK_MODE', prefersDark)
      }
    }
  },
  getters: {
    isDarkMode: (state) => state.darkMode
  }
})

// Agregar event bus global si no existe
if (!Vue.prototype.$eventBus) {
  Vue.prototype.$eventBus = new Vue()
}