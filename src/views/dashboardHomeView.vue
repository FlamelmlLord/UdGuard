<template>
  <div class="dashboard" :class="{ 'dark-mode': isDarkMode }">
    <aside class="sidebar">
      <div class="user-section">
        <img src="/path/to/logo_GSI.png" alt="Logo GSI" class="logo" />
      </div>
      <div class="search-section">
        <div class="search-box">
          <i class="mdi mdi-magnify search-icon"></i>
          <input type="text" placeholder="Buscar..." class="search-input" />
        </div>
      </div>
      <nav class="menu">
        <ul>
          <li>
            <router-link
              to="/dashboard"
              class="menu-item"
              :class="{ active: hoveredItem === 'Inicio' }"
              @mouseover="hover('Inicio')"
              @mouseleave="unhover">
              <i class="mdi mdi-home-outline icon"></i>
              <span>Inicio</span>
            </router-link>
          </li>
          <li>
            <router-link
              to="/dashboard/docs"
              class="menu-item"
              :class="{ active: hoveredItem === 'Documentos' }"
              @mouseover="hover('Documentos')"
              @mouseleave="unhover">
              <i class="mdi mdi-file-document-outline icon"></i>
              <span>Documentos</span>
            </router-link>
          </li>
          <li>
            <router-link
              to="/dashboard/facts"
              class="menu-item"
              :class="{ active: hoveredItem === 'Factores' }"
              @mouseover="hover('Factores')"
              @mouseleave="unhover">
              <i class="mdi mdi-chart-pie icon"></i>
              <span>Factores</span>
            </router-link>
          </li>
          <li>
            <a href="#" class="menu-item" :class="{ active: hoveredItem === 'Cumplimiento' }"
               @mouseover="hover('Cumplimiento')" @mouseleave="unhover">
              <i class="mdi mdi-checkbox-marked-circle-outline icon"></i>
              <span>Cumplimiento</span>
            </a>
          </li>
        </ul>
      </nav>
      <div class="user-management">
        <a href="#" class="menu-item" :class="{ active: hoveredItem === 'Usuarios' }"
           @mouseover="hover('Usuarios')" @mouseleave="unhover">
          <i class="mdi mdi-account-group-outline icon"></i>
          <span>Gestión de Usuarios</span>
        </a>
      </div>

      <div class="bottom-section">
        <button class="logout-button" @click="logout">
          <i class="mdi mdi-logout-variant"></i>
          Cerrar sesión
        </button>
        <div class="theme-toggle">
          <label class="theme-switch">
            <i class="mdi mdi-weather-night icon"></i>
            <span>Modo Oscuro</span>
            <div class="switch">
              <input type="checkbox" v-model="isDarkMode" @change="toggleTheme">
              <span class="slider"></span>
            </div>
          </label>
        </div>
      </div>
    </aside>
    <main class="main-content">
      <!-- Aquí se renderizan las vistas dinámicas -->
      <router-view />
    </main>
  </div>
</template>

<script>
import { useRouter } from 'vue-router'

export default {
  name: 'HomeDashboardView',
  data () {
    return {
      hoveredItem: null,
      isDarkMode: false
    }
  },
  setup () {
    const router = useRouter()
    return { router }
  },
  created () {
    const darkMode = localStorage.getItem('darkMode')
    if (darkMode) {
      this.isDarkMode = JSON.parse(darkMode)
      this.applyDarkMode(this.isDarkMode)
    }
  },
  methods: {
    hover (item) {
      this.hoveredItem = item
    },
    unhover () {
      this.hoveredItem = null
    },
    toggleTheme () {
      this.applyDarkMode(this.isDarkMode)
      localStorage.setItem('darkMode', this.isDarkMode)
    },
    applyDarkMode (isDark) {
      document.body.classList.toggle('dark-mode', isDark)
    },
    async logout () {
      try {
        localStorage.removeItem('token')
        localStorage.removeItem('user')
        await this.router.push('/login')
      } catch (error) {
        console.error('Error al cerrar sesión:', error)
      }
    }
  }
}
</script>

<style scoped src="../styles/dashboard.css"></style>
