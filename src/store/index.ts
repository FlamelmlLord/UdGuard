import Vue from 'vue'
import Vuex from 'vuex'

Vue.use(Vuex)

export default new Vuex.Store({
  state: {
    darkMode: false
  },
  mutations: {
    SET_DARK_MODE (state, value) {
      state.darkMode = value
      localStorage.setItem('darkMode', JSON.stringify(value))
      document.body.classList.toggle('dark-mode', value)
    }
  },
  actions: {
    toggleDarkMode ({ commit, state }) {
      commit('SET_DARK_MODE', !state.darkMode)
    },
    initDarkMode ({ commit }) {
      const savedDarkMode = localStorage.getItem('darkMode')
      if (savedDarkMode) {
        commit('SET_DARK_MODE', JSON.parse(savedDarkMode))
      }
    }
  }
})
