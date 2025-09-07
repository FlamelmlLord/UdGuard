<template>
  <div class="dashboard" :class="themeClasses">
    <aside class="sidebar" :class="themeClasses">
      <div class="user-section">
        <img src="@/assets/logo_GSI.png" alt="Logo GSI" class="logo" />
      </div>
      <div class="search-section">
        <div class="search-box">
          <i class="mdi mdi-magnify search-icon"></i>
          <input 
            type="text" 
            placeholder="Buscar..." 
            class="search-input"
            :class="themeClasses" 
          />
        </div>
      </div>
      <nav class="menu">
        <ul>
          <li>
            <router-link
              to="/dashboard/home"
              class="menu-item"
              :class="{ 
                active: hoveredItem === 'Inicio',
                ...themeClasses 
              }"
              @mouseover="hover('Inicio')"
              @mouseleave="unhover"
            >
              <i class="mdi mdi-home-outline icon"></i>
              <span>Inicio</span>
            </router-link>
          </li>
          <li>
            <router-link
              to="/dashboard/facts"
              class="menu-item"
              :class="{ 
                active: hoveredItem === 'Factores',
                ...themeClasses 
              }"
              @mouseover="hover('Factores')"
              @mouseleave="unhover"
            >
              <i class="mdi mdi-chart-pie icon"></i>
              <span>Factores</span>
            </router-link>
          </li>
          <li>
            <router-link
              to="/dashboard/Cumplimiento"
              class="menu-item"
              :class="{ 
                active: hoveredItem === 'Cumplimiento',
                ...themeClasses 
              }"
              @mouseover="hover('Cumplimiento')"
              @mouseleave="unhover"
            >
              <i class="mdi mdi-checkbox-marked-circle-outline icon"></i>
              <span>Cumplimiento</span>
            </router-link>
          </li>
        </ul>
      </nav>
      <div class="user-management">
        <router-link
          to="/dashboard/users"
          class="menu-item"
          :class="{ 
            active: hoveredItem === 'Usuarios',
            ...themeClasses 
          }"
          @mouseover="hover('Usuarios')"
          @mouseleave="unhover"
        >
          <i class="mdi mdi-account-group-outline icon"></i>
          <span>Gestión de Usuarios</span>
        </router-link>
      </div>
      <div class="bottom-section">
        <button class="logout-button btn-secondary" :class="themeClasses" @click="logout">
          <i class="mdi mdi-logout-variant"></i>
          Cerrar sesión
        </button>
        <div class="theme-toggle">
          <label class="theme-switch" :class="themeClasses">
            <i class="mdi mdi-weather-night icon"></i>
            <span>Modo Oscuro</span>
            <div class="switch" :class="themeClasses">
              <input
                type="checkbox"
                :checked="isDarkMode"
                @change="toggleDarkMode"
              />
              <span class="slider" :class="themeClasses"></span>
            </div>
          </label>
        </div>
      </div>
    </aside>
    <main class="main-content" :class="themeClasses">
      <router-view :key="$route.fullPath" :class="themeClasses">
      </router-view>
    </main>
  </div>
</template>

<script lang="ts">
import Vue from 'vue'
import { Component, Mixins } from 'vue-property-decorator'
import DarkModeMixin from '@/mixins/DarkModeMixin'

@Component({
  name: 'DashboardHomeView'
})
export default class DashboardHomeView extends Mixins(DarkModeMixin) {
  hoveredItem: string | null = null

  created (): void {
    this.$store.dispatch('initDarkMode')
  }

  mounted (): void {
    super.mounted() // Call parent mounted from mixin
    this.initializeTheme()
  }

  initializeTheme (): void {
    // Force theme application on route changes
    this.$router.afterEach(() => {
      this.$nextTick(() => {
        this.ensureDarkModeConsistency()
      })
    })
  }

  toggleDarkMode (): void {
    this.$store.dispatch('toggleDarkMode')
  }

  hover (item: string): void {
    this.hoveredItem = item
  }

  unhover (): void {
    this.hoveredItem = null
  }

  async logout (): Promise<void> {
    try {
      localStorage.removeItem('token')
      localStorage.removeItem('user')
      await this.$router.push('/login')
    } catch (error) {
      console.error('Error al cerrar sesión:', error)
    }
  }

  // Override del método del mixin para lógica específica
  onDarkModeChanged (isDark: boolean): void {
    // Lógica específica del dashboard cuando cambia el dark mode
    console.log(`Dashboard theme changed to: ${isDark ? 'dark' : 'light'}`)
  }
}
</script>

<style scoped src="../styles/dashboard.css"></style>