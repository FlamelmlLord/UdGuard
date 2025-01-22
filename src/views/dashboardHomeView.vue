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
              <a href="#" class="menu-item" :class="{ active: hoveredItem === 'Inicio' }"
                 @mouseover="hover('Inicio')" @mouseleave="unhover">
                <i class="mdi mdi-home-outline icon"></i>
                <span>Inicio</span>
              </a>
            </li>
            <li>
              <a href="#" class="menu-item" :class="{ active: hoveredItem === 'Factores' }"
                 @mouseover="hover('Factores')" @mouseleave="unhover">
                <i class="mdi mdi-chart-pie icon"></i>
                <span>Factores</span>
              </a>
            </li>
            <li>
              <a href="#" class="menu-item" :class="{ active: hoveredItem === 'Cumplimiento' }"
                 @mouseover="hover('Cumplimiento')" @mouseleave="unhover">
                <i class="mdi mdi-checkbox-marked-circle-outline icon"></i>
                <span>Cumplimiento</span>
              </a>
            </li>
            <li>
              <a href="#" class="menu-item" :class="{ active: hoveredItem === 'Documentos' }"
                 @mouseover="hover('Documentos')" @mouseleave="unhover">
                <i class="mdi mdi-file-document-outline icon"></i>
                <span>Documentos</span>
              </a>
            </li>
          </ul>
        </nav>
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
        <h1>BIENVENIDO AL GESTOR DE INFORMACION Y DOCUMENTOS</h1>
        <div class="content-area">
          <!-- Contenido principal -->
        </div>
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
    // Recuperar el estado del modo oscuro al cargar
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
      // Guardar preferencia en localStorage
      localStorage.setItem('darkMode', this.isDarkMode)
    },
    applyDarkMode (isDark) {
      document.body.classList.toggle('dark-mode', isDark)
    },
    async logout () {
      try {
        // Aquí puedes agregar la lógica para limpiar el estado de la aplicación
        localStorage.removeItem('token') // Si usas token
        localStorage.removeItem('user') // Si guardas datos del usuario

        // Redirigir al login
        await this.router.push('/login')
      } catch (error) {
        console.error('Error al cerrar sesión:', error)
      }
    }
  }
}
</script>

  <style scoped>
.dashboard {
  display: flex;
  height: 100vh;
  background-color: var(--background);
}

.sidebar {
  width: 250px;
  background-color: white;
  display: flex;
  flex-direction: column;
  padding: 1.5rem;
  box-shadow: 2px 0 5px rgba(0, 0, 0, 0.1);
}

.search-section {
  margin: 1.5rem 0;
}

.search-box {
  position: relative;
  width: 100%;
}

.search-input {
  width: 100%;
  padding: 8px 32px;
  border: 1px solid #E0E0E0;
  border-radius: 4px;
  font-size: 0.9rem;
}

.search-icon {
  position: absolute;
  left: 8px;
  top: 50%;
  transform: translateY(-50%);
  color: #666;
}

.user-section {
  text-align: center;
  margin-bottom: 1rem;
}

.logo {
  max-width: 80%;
  height: auto;
}

.menu {
  flex: 1;
  margin: 1rem 0;
}

.menu ul {
  list-style: none;
  padding: 0;
  margin: 0;
}

.menu-item {
  display: flex;
  align-items: center;
  padding: 0.8rem 1rem;
  color: #0D2B44;
  text-decoration: none;
  border-radius: 4px;
  margin-bottom: 0.5rem;
  transition: all 0.3s ease;
}

.menu-item:hover,
.menu-item.active {
  background-color: #46AFEA;
  color: white;
}

.icon {
  margin-right: 0.8rem;
  font-size: 1.4rem;
}

.bottom-section {
  margin-top: auto;
}

.logout-button {
  width: 100%;
  background: transparent;
  border: 1px solid #0D2B44;
  color: #0D2B44;
  border-radius: 4px;
  padding: 0.5rem;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
  transition: all 0.3s ease;
}

.logout-button:hover {
  background-color: #46AFEA;
  border-color: #46AFEA;
  color: white;
}

.theme-toggle {
  margin-top: 1rem;
}

.theme-switch {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  cursor: pointer;
  color: #0D2B44;
}

.switch {
  position: relative;
  display: inline-block;
  width: 40px;
  height: 20px;
  margin-left: auto;
}

.switch input {
  opacity: 0;
  width: 0;
  height: 0;
}

.slider {
  position: absolute;
  cursor: pointer;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: #ccc;
  transition: .4s;
  border-radius: 20px;
}

.slider:before {
  position: absolute;
  content: "";
  height: 16px;
  width: 16px;
  left: 2px;
  bottom: 2px;
  background-color: white;
  transition: .4s;
  border-radius: 50%;
}

input:checked + .slider {
  background-color: #46AFEA;
}

input:checked + .slider:before {
  transform: translateX(20px);
}

.main-content {
  flex: 1;
  padding: 2rem;
  background-color: #E2F1FC;
}

.content-area {
  background-color: #FFFFFF;
  border-radius: 8px;
  padding: 2rem;
  height: calc(100% - 60px);
  margin-top: 1rem;
}

h1 {
  color: #0D2B44;
  font-size: 1.5rem;
  margin: 0;
}

.dark-mode .sidebar {
  background-color: #2D2D2D;
}

.dark-mode .menu-item {
  color: white;
}

.dark-mode .logout-button {
  border-color: white;
  color: white;
}

.dark-mode h1 {
  color: white;
}

.dark-mode .theme-switch {
  color: white;
}

  .dashboard.dark-mode .main-content {
    background-color: #1E1E1E;
  }

  .dashboard.dark-mode .content-area {
    background-color: #2D2D2D;
    color: white;
  }

  .dashboard.dark-mode .search-input {
    background-color: #2D2D2D;
    border-color: #3D3D3D;
    color: white;
  }

  .dashboard.dark-mode .search-icon {
    color: #888;
  }

  .dashboard.dark-mode h1 {
    color: white;
  }

  .main-content {
    flex: 1;
    padding: 2rem;
    background-color: #E2F1FC;
    transition: background-color 0.3s ease;
  }

  .content-area {
    background-color: #FFFFFF;
    border-radius: 8px;
    padding: 2rem;
    height: calc(100% - 60px);
    margin-top: 1rem;
    transition: background-color 0.3s ease, color 0.3s ease;
  }

  .dashboard * {
    transition: background-color 0.3s ease, color 0.3s ease, border-color 0.3s ease;
  }

  </style>
