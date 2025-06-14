<template>
  <div class="dashboard" :class="{ 'dark-mode': $store.state.darkMode }">
    <aside class="sidebar">
      <div class="user-section">
        <img src="@/assets/logo_GSI.png" alt="Logo GSI" class="logo" />
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
              to="/dashboard/home"
              class="menu-item"
              :class="{ active: hoveredItem === 'Inicio' }"
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
              :class="{ active: hoveredItem === 'Factores' }"
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
              :class="{ active: hoveredItem === 'Cumplimiento' }"
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
          :class="{ active: hoveredItem === 'Usuarios' }"
          @mouseover="hover('Usuarios')"
          @mouseleave="unhover"
        >
          <i class="mdi mdi-account-group-outline icon"></i>
          <span>Gestión de Usuarios</span>
        </router-link>
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
              <input
                type="checkbox"
                :checked="$store.state.darkMode"
                @change="$store.dispatch('toggleDarkMode')"
              />
              <span class="slider"></span>
            </div>
          </label>
        </div>
      </div>
    </aside>
    <main class="main-content">
      <router-view></router-view>
    </main>
  </div>
</template>

<script lang="ts">
import Vue from 'vue'
import { Component } from 'vue-property-decorator'

@Component({
  name: 'DashboardHomeView'
})
export default class DashboardHomeView extends Vue {
  hoveredItem: string | null = null;

  created (): void {
    this.$store.dispatch('initDarkMode')
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
}
</script>

<style scoped src="../styles/dashboard.css"></style>
